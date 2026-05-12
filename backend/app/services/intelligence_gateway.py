"""
ScholarStream Intelligence Gateway (V5) — Gemma Native
The Unified Entry Point for all AI Operations.
Strictly routes all requests to Gemma 4 via Vertex AI MaaS.
Gemini has been completely removed to ensure hackathon compliance.
"""
import structlog
from typing import Dict, Any, Optional, List
from app.config import settings
from app.services.ai_service import ai_service
from app.services.gemma_service import gemma_service
from app.models import ScrapedScholarship, UserProfile, AIEnrichmentResponse
from app.utils.json_utils import robust_json_loads

logger = structlog.get_logger()

class IntelligenceGateway:
    """
    Unified Gateway for Gemma 4.
    Acts as the single point of intelligence for extraction, matching, and reasoning.
    """

    def __init__(self):
        logger.info("Intelligence Gateway: GEMMA NATIVE MODE ACTIVE")

    async def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """General purpose content generation via Gemma 4."""
        try:
            response = await gemma_service.generate_content_async(
                prompt, system_instruction=system_instruction
            )
            if not response or "choices" not in response:
                logger.warning("Gemma response empty or malformed")
                return ""
            
            raw_content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not raw_content:
                return ""

            data = robust_json_loads(raw_content)
            if data is None:
                logger.warning("Gemma content: Failed to parse JSON response")
                return raw_content
                
            return raw_content
        except Exception as e:
            logger.error("Gemma content generation failed", error=str(e))
            return ""

    async def enrich_scholarship(self, scholarship: ScrapedScholarship, user_profile: UserProfile) -> Optional[AIEnrichmentResponse]:
        """Deep enrichment of a scraped opportunity via GemmaAIService."""
        return await ai_service.enrich_scholarship(scholarship, user_profile)

    async def analyze_query_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze student query intent via Gemma 4."""
        return await ai_service.analyze_query_intent(user_query)

# Global instance
intelligence_gateway = IntelligenceGateway()
