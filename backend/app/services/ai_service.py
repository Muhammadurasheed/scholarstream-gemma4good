"""
Gemma AI Service — Hackathon Native Implementation
Handles AI-powered scholarship enrichment, matching, and intent analysis.
Strictly uses Gemma 4 via Vertex AI MaaS. Gemini has been purged.
"""
import os
from typing import Dict, List, Optional, Any
import json
import asyncio
import structlog
import hashlib
from datetime import datetime, timedelta

try:
    from upstash_redis import Redis
    UPSTASH_AVAILABLE = True
except ImportError:
    UPSTASH_AVAILABLE = False
    Redis = None

from app.config import settings
from app.services.gemma_service import gemma_service
from app.models import (
    ScrapedScholarship,
    UserProfile,
    ScholarshipEligibility,
    ScholarshipRequirements,
    AIEnrichmentResponse
)

logger = structlog.get_logger()

class GemmaAIService:
    """
    Native Gemma 4 AI Service.
    All logic is optimized for Gemma's 27B-IT reasoning capabilities.
    """
    
    def __init__(self):
        logger.info("⚡ GEMMA NATIVE AI SERVICE ACTIVE (Hackathon Mode)")
        
        # Initialize Upstash Redis for caching
        self.redis_client = None
        if UPSTASH_AVAILABLE and settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
            try:
                self.redis_client = Redis(
                    url=settings.upstash_redis_rest_url,
                    token=settings.upstash_redis_rest_token
                )
                logger.info("Upstash Redis initialized for Gemma caching")
            except Exception as e:
                logger.warning(f"Failed to initialize Upstash Redis: {e}. Falling back to in-memory caching.")
        
        self.memory_cache: Dict[str, tuple] = {}

    async def generate_content_async(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Call Gemma 4 directly via Vertex AI MaaS."""
        response = await gemma_service.generate_content_async(prompt, system_instruction=system_instruction)
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")

    async def enrich_scholarship(
        self,
        scholarship: ScrapedScholarship,
        user_profile: UserProfile
    ) -> Optional[AIEnrichmentResponse]:
        """Parse and enrich scholarship data using Gemma 4 reasoning."""
        
        # 1. Check cache first
        cache_key = self._generate_cache_key(scholarship.source_url, user_profile.name)
        cached_enrichment = self._get_cached_enrichment(cache_key)
        if cached_enrichment:
            logger.info("Using cached Gemma enrichment", source=scholarship.source_url)
            return cached_enrichment
        
        try:
            # 2. Build and Execute Gemma Prompt
            prompt = self._build_enrichment_prompt(scholarship, user_profile)
            
            # Using Gemma's thinking mode for deep analysis
            content = await self.generate_content_async(prompt)
            
            # 3. Parse and Validate
            enriched_data = self._parse_ai_response(content)
            
            # 4. Cache the result
            self._cache_enrichment(cache_key, enriched_data)
            
            logger.info("Scholarship enriched natively by Gemma 4", source=scholarship.source_url)
            return enriched_data
            
        except Exception as e:
            logger.error("Gemma enrichment failed", error=str(e), source=scholarship.source_url)
            return None
    
    async def analyze_query_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze student query for urgency and intent using Gemma 4."""
        prompt = f"""
        Analyze this student query: "{user_query}"
        
        Determine:
        1. Is this URGENT? (Deadline < 14 days, fees due, eviction risk, starvation)
        2. What are the key entities? (Location, Role, Domain)
        3. What type of finding is best? (Grant/Bounty = Fast, Scholarship = Slow)

        Return JSON only:
        {{
            "is_urgent": <bool>,
            "suggested_filters": {{
                "priority_level": "URGENT" (if urgent),
                "type_tags": ["Grant", "Bounty"] (if urgent),
                "deadline_days_max": 14 (if urgent)
            }},
            "vector_search_query": <Optimized search string, e.g. "Software grants Nigeria fast funding">
        }}
        """
        
        try:
            content = await self.generate_content_async(prompt)
            return self._parse_json_safe(content)
        except Exception as e:
            logger.error("Gemma intent analysis failed", error=str(e))
            is_urgent = any(w in user_query.lower() for w in ["urgent", "deadline", "fees", "asap"])
            return {
                "is_urgent": is_urgent,
                "filters": {"priority_level": "URGENT"} if is_urgent else {},
                "vector_query": user_query
            }

    def _build_enrichment_prompt(self, scholarship: ScrapedScholarship, user_profile: UserProfile) -> str:
        """Build prompt for Gemma to enrich scholarship data with reasoning."""
        return f"""You are ScholarStream's Cortex V3 Intelligence Engine, powered by Gemma 4. 
Analyze this scholarship against the student's profile and provide a structured matching report.

SCHOLARSHIP DATA:
Name: {scholarship.name}
Organization: {scholarship.organization}
Amount: ${scholarship.amount}
Deadline: {scholarship.deadline}
Description: {scholarship.description}
Eligibility (raw): {scholarship.eligibility_raw or 'Not specified'}

USER PROFILE:
Academic Status: {user_profile.academic_status}
Major: {user_profile.major or 'Not specified'}
GPA: {user_profile.gpa or 'Not specified'}
Interests: {', '.join(user_profile.interests) if user_profile.interests else 'Not specified'}

TASK:
Provide a JSON response with the following structure (respond ONLY with valid JSON):

{{
  "eligibility": {{
    "gpa_min": <float or null>,
    "grades_eligible": [<list: "Undergraduate", "Graduate", etc.>],
    "majors": [<list of eligible majors or null if any>],
    "backgrounds": [<list: "Minority", "Low-income", etc.>]
  }},
  "requirements": {{
    "essay": <true/false>,
    "recommendation_letters": <integer>,
    "transcript": <true/false>,
    "resume": <true/false>
  }},
  "tags": [<3-5 relevant tags>],
  "match_score": <0-100 integer based on profile fit>,
  "match_tier": <"Excellent", "Good", "Fair", or "Poor">,
  "priority_level": <"URGENT", "HIGH", "MEDIUM", or "LOW">,
  "competition_level": <"Low", "Medium", or "High">,
  "estimated_time": <string: e.g. "2 hours">
}}

Respond with ONLY the JSON object, no additional text."""

    def _parse_ai_response(self, response_text: str) -> AIEnrichmentResponse:
        """Parse Gemma response into structured data."""
        try:
            data = self._parse_json_safe(response_text)
            return AIEnrichmentResponse(
                eligibility=ScholarshipEligibility(**data.get('eligibility', {})),
                requirements=ScholarshipRequirements(**data.get('requirements', {})),
                tags=data.get('tags', []),
                match_score=float(data.get('match_score', 50)),
                match_tier=data.get('match_tier', "Fair"),
                priority_level=data.get('priority_level', "MEDIUM"),
                competition_level=data.get('competition_level', "Medium"),
                estimated_time=data.get('estimated_time', "2-3 hours")
            )
        except Exception as e:
            logger.error("Failed to parse Gemma response", error=str(e))
            return AIEnrichmentResponse(
                eligibility=ScholarshipEligibility(),
                requirements=ScholarshipRequirements(),
                tags=[],
                match_score=50.0,
                match_tier="Fair",
                priority_level="MEDIUM",
                competition_level="Medium",
                estimated_time="2-3 hours"
            )

    def _parse_json_safe(self, text: str) -> Dict:
        """Helper to clean and parse JSON from LLM output."""
        text = text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        return json.loads(text.strip())

    def _generate_cache_key(self, source_url: str, user_name: str) -> str:
        key_string = f"{source_url}_{user_name}_gemma4"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_cached_enrichment(self, cache_key: str) -> Optional[AIEnrichmentResponse]:
        if self.redis_client:
            try:
                cached = self.redis_client.get(f"ai_enrichment:{cache_key}")
                if cached:
                    return AIEnrichmentResponse(**json.loads(cached))
            except Exception: pass
        if cache_key in self.memory_cache:
            data, ts = self.memory_cache[cache_key]
            if (datetime.now() - ts).total_seconds() < settings.ai_enrichment_cache_ttl_hours * 3600:
                return data
        return None

    def _cache_enrichment(self, cache_key: str, enrichment: AIEnrichmentResponse):
        if self.redis_client:
            try:
                self.redis_client.set(
                    f"ai_enrichment:{cache_key}",
                    json.dumps(enrichment.model_dump()),
                    ex=int(settings.ai_enrichment_cache_ttl_hours * 3600)
                )
            except Exception: pass
        self.memory_cache[cache_key] = (enrichment, datetime.now())

    async def batch_enrich_scholarships(self, scholarships: List[ScrapedScholarship], user_profile: UserProfile, batch_size: int = 5):
        results = []
        for i in range(0, len(scholarships), batch_size):
            batch = scholarships[i:i + batch_size]
            for scholarship in batch:
                results.append(await self.enrich_scholarship(scholarship, user_profile))
            if i + batch_size < len(scholarships):
                await asyncio.sleep(0.5) # Gemma 4 RPM is high on Vertex MaaS
        return results

# Global AI service instance
ai_service = GemmaAIService()
