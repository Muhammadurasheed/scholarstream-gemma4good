"""
Gemma 4 AI Service (Native Implementation)
Hosts the Scholar-Einstein agent logic using Gemma 4 via Vertex AI Maas.

IMPORTANT AUTH NOTE:
  Vertex AI MaaS endpoints require OAuth2 Bearer token authentication.
  API key (?key=...) auth is NOT supported and causes 429/403 errors.
  We use google.auth.default() (ADC) to get a short-lived Bearer token.
"""
import os
import httpx
import json
import structlog
import asyncio
import certifi
from typing import Dict, List, Optional, Any
from datetime import datetime
import google.auth
import google.auth.transport.requests

from app.config import settings
# CRITICAL: Use the dedicated gemma_rate_limiter (200 RPM), NOT gemini_rate_limiter (30 RPM).
# These two services must never share the same rate limiter instance.
from app.utils.rate_limiter import gemma_rate_limiter
from app.models import (
    ScrapedScholarship,
    UserProfile,
    AIEnrichmentResponse,
    ScholarshipEligibility,
    ScholarshipRequirements
)

logger = structlog.get_logger()

class GemmaAIService:
    """
    Native Gemma 4 integration for ScholarStream.
    Uses Thinking Mode for deep reasoning and System Prompts for personality.
    """
    
    def __init__(self):
        self.project_id = settings.firebase_project_id or "scholarstream-gemma4good"
        # Gemma 4 MaaS models are served via the global endpoint
        self.region = "us-central1"
        self.endpoint = f"https://aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/global/endpoints/openapi/chat/completions"
        self.model_id = "google/gemma-4-26b-a4b-it-maas"
        
        # Tool Map for ReAct execution
        self.tools = []
        
        # Initialize Google Credentials (ADC)
        try:
            # 1. Try GOOGLE_APPLICATION_CREDENTIALS or ADC
            self.creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
            
            # 2. Check if we are using "end user credentials" (the ones that cause Errno 2 on Windows)
            # If so, and we have a serviceAccountKey.json, prioritize the service account.
            from google.oauth2 import service_account
            # Resolve path relative to this file to be bulletproof
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            # actually app/services/gemma_service.py
            # current_dir = app/services
            # current_dir parent = app
            # current_dir parent parent = backend
            backend_dir = os.path.dirname(os.path.dirname(current_dir))
            sa_path = os.path.join(backend_dir, "serviceAccountKey.json")
            
            if os.path.exists(sa_path):
                logger.info("Service Account JSON found. Prioritizing for stable auth.", path=sa_path)
                # CRITICAL FIX: Read project_id directly from the JSON file.
                # service_account.Credentials.from_service_account_file() does NOT
                # expose .project_id — it returns None, breaking the endpoint URL.
                import json as _json
                with open(sa_path, 'r') as _f:
                    _sa_data = _json.load(_f)
                
                _sa_project_id = _sa_data.get('project_id', 'scholarstream-gemma4good')
                self.creds = service_account.Credentials.from_service_account_info(
                    _sa_data,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                # Use the project_id from the JSON, not from the creds object
                self.project_id = _sa_project_id
            else:
                logger.warning("Service Account JSON NOT found. Falling back to default auth.", attempted_path=sa_path, cwd=os.getcwd())
            
            if not self.project_id:
                self.project_id = settings.firebase_project_id or "scholarstream-gemma4good"
            
            # Rebuild endpoint with validated project_id
            self.endpoint = f"https://aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/global/endpoints/openapi/chat/completions"
            
            logger.info("Gemma AI initialized with stable credentials", project_id=self.project_id)
        except Exception as e:
            logger.error("Failed to initialize Gemma AI credentials", error=str(e))
            self.creds = None

    async def get_access_token(self) -> str:
        """Refresh and return the GCP access token (non-blocking)"""
        if not self.creds:
            raise Exception("GCP Credentials not initialized")
            
        if not self.creds.valid:
            try:
                # CRITICAL: creds.refresh() is synchronous and uses urllib3 under the hood.
                # Running it directly in an async function blocks the event loop on Windows.
                # Wrap in run_in_executor to keep the event loop free.
                import functools
                loop = asyncio.get_event_loop()
                auth_req = google.auth.transport.requests.Request()
                await loop.run_in_executor(
                    None, 
                    functools.partial(self.creds.refresh, auth_req)
                )
            except Exception as e:
                error_msg = str(e)
                if "[Errno 2]" in error_msg:
                    logger.error("Gemma Auth: gcloud or credential file missing (Errno 2). Check GOOGLE_APPLICATION_CREDENTIALS or Windows Execution Policy.", error=error_msg)
                else:
                    logger.error("Gemma Auth: Failed to refresh credentials", error=error_msg)
                raise
        
        return self.creds.token

    async def generate_content_async(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        enable_thinking: bool = True,
        tools: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Execute a chat completion against Gemma 4 via Vertex AI Maas.

        AUTH: Uses OAuth2 Bearer token (ADC). Vertex AI MaaS does NOT support
        API key (?key=...) auth — that causes 429/403 errors.
        The get_access_token() method refreshes the short-lived token automatically.
        """
        async def _raw_call() -> Dict:
            # Refresh Bearer token (ADC — Application Default Credentials)
            access_token = await self.get_access_token()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",  # Correct auth for Vertex AI
            }

            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "stream": False,
                "max_tokens": 8192,
                "chat_template_kwargs": {
                    "enable_thinking": enable_thinking
                }
            }

            if tools:
                payload["tools"] = [{"type": "function", "function": t} for t in tools]
                payload["tool_choice"] = "auto"

            async with httpx.AsyncClient(verify=certifi.where(), timeout=240.0) as client:
                try:
                    response = await client.post(self.endpoint, headers=headers, json=payload)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    logger.error(
                        "Gemma API HTTP Error",
                        status_code=e.response.status_code,
                        response=e.response.text,
                        url=str(e.request.url)
                    )
                    raise

        # Use dedicated gemma_rate_limiter (200 RPM), NOT the shared gemini one
        return await gemma_rate_limiter.execute(_raw_call)

    async def analyze_query_intent(self, user_query: str) -> Dict[str, Any]:
        """Deep intent analysis using Gemma's thinking mode"""
        system_prompt = "You are the Scholar-Einstein Intent Analyzer. You detect urgency and hidden student needs."
        
        prompt = f"""
        Analyze this student query: "{user_query}"
        
        TASK:
        1. Detect URGENCY (True/False).
        2. Identify target entities (Location, Degree, Field).
        3. Optimize search terms.

        Return JSON only:
        {{
            "is_urgent": bool,
            "suggested_filters": {{ "priority_level": "URGENT" or "MEDIUM" }},
            "vector_search_query": "optimized string"
        }}
        """
        
        try:
            response_json = await self.generate_content_async(prompt, system_instruction=system_prompt)
            content = response_json["choices"][0]["message"]["content"]
            return self._parse_json_safe(content)
        except Exception as e:
            logger.error("Gemma intent analysis failed", error=str(e))
            return {"is_urgent": False, "filters": {}, "vector_query": user_query}

    async def generate_hunt_strategy(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gemma decides where to hunt based on user DNA — OPPORTUNITY-FOCUSED queries only"""
        major = user_profile.get("major", "General Studies")
        interests = user_profile.get("interests", [])
        country = user_profile.get("country", "")
        academic_status = user_profile.get("academic_status", "Undergraduate")
        
        interests_str = ", ".join(interests[:5]) if interests else "general academics"
        
        prompt = f"""You are ScholarStream's Opportunity Discovery Agent.

YOUR MISSION: Generate search queries to find ACTIVE scholarships, hackathons, grants, 
and fellowships that a student can APPLY TO RIGHT NOW.

STUDENT PROFILE:
- Major: {major}
- Academic Level: {academic_status}
- Interests: {interests_str}
- Country: {country or 'Global'}

CRITICAL RULES:
1. Generate queries that find APPLICATION PAGES — NOT blog posts, research papers, or news articles
2. Include terms like "apply now", "deadline 2025", "deadline 2026", "registration open", "call for applications"
3. Target real opportunity platforms: scholarships.com, bold.org, devpost.com, mlh.io, fastweb.com, etc.
4. Make queries specific to the student's field and country
5. Each query should target a DIFFERENT type of opportunity (scholarship, hackathon, grant, fellowship)

Return JSON only:
{{
    "thought": "Brief reasoning about what opportunities match this student",
    "platforms": ["3-5 specific opportunity websites to check"],
    "search_queries": ["4-5 search queries optimized for finding active opportunities with deadlines"]
}}"""
        
        try:
            response_json = await self.generate_content_async(
                prompt, 
                system_instruction="You are an expert opportunity scout. You ONLY generate queries that find pages where students can apply for scholarships, grants, hackathons, and fellowships. Never generate queries for research papers, blog posts, or news articles.",
                enable_thinking=False
            )
            content = response_json["choices"][0]["message"]["content"]
            result = self._parse_json_safe(content)
            
            # Validate: ensure search_queries exist and are opportunity-focused
            if result and result.get("search_queries"):
                logger.info("Hunt strategy generated", queries=result["search_queries"][:3])
                return result
            
            raise ValueError("Empty or invalid strategy from Gemma")
            
        except Exception as e:
            logger.error("Gemma strategy generation failed, using DNA fallback", error=str(e))
            # High-quality hardcoded fallback that actually finds opportunities
            major_lower = major.lower().replace(" ", "+")
            top_interest = (interests[0] if interests else "technology").lower().replace(" ", "+")
            country_str = country or "international"
            
            return {
                "thought": f"Using DNA-driven fallback: targeting {major} opportunities for {country_str} students",
                "platforms": ["bold.org", "scholarships.com", "devpost.com", "fastweb.com"],
                "search_queries": [
                    f"{major} scholarships for {country_str} students 2025 2026 apply now deadline",
                    f"{top_interest} hackathons 2025 2026 registration open apply",
                    f"fully funded {major} fellowships {country_str} undergraduate graduate deadline",
                    f"{major} grants for students apply deadline {country_str}",
                    f"{top_interest} competitions prizes students 2025 2026 registration"
                ]
            }

    def _parse_json_safe(self, text: str) -> Dict:
        """Helper to clean and parse JSON from Gemma's response"""
        text = text.strip()
        # Handle thinking block if present (Gemma might return <thought>...</thought> if not stripped by Maas)
        if "</thought>" in text:
            text = text.split("</thought>")[-1].strip()
            
        if text.startswith('```json'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Last resort: try to find the first { and last }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                return json.loads(text[start:end+1])
            raise

# Global Gemma service instance
gemma_service = GemmaAIService()
