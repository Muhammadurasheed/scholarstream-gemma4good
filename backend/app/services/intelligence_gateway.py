"""
ScholarStream Intelligence Gateway (V5)
The Unified Entry Point for all AI Operations.
Routes requests between Gemini (Performance) and Gemma 4 (Privacy/Offline).
"""
import structlog
from typing import Dict, Any, Optional, List
from app.config import settings
from app.services.ai_service import ai_service
from app.services.gemma_service import gemma_service
from app.models import ScrapedScholarship, UserProfile, AIEnrichmentResponse

logger = structlog.get_logger()

class IntelligenceGateway:
    """
    Principal-grade Gateway that abstracts the underlying LLM.
    Ensures the system remains 'Engine-Agnostic'.
    """

    def __init__(self):
        self.engine = "gemma" if settings.gemma_engine_enabled else "gemini"
        logger.info("Intelligence Gateway Online", primary_engine=self.engine)

    async def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """General purpose content generation"""
        if self.engine == "gemma":
            response = await gemma_service.generate_content_async(prompt, system_instruction=system_instruction)
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return await ai_service.generate_content_async(prompt)

    async def enrich_scholarship(self, scholarship: ScrapedScholarship, user_profile: UserProfile) -> Optional[AIEnrichmentResponse]:
        """Deep enrichment of a scraped opportunity"""
        # ai_service already has internal routing logic, but we standardize it here
        return await ai_service.enrich_scholarship(scholarship, user_profile)

    async def analyze_query_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze student query for urgency and intent"""
        if self.engine == "gemma":
            return await gemma_service.analyze_query_intent(user_query)
        else:
            return await ai_service.analyze_query_intent(user_query)

# Global instance
intelligence_gateway = IntelligenceGateway()
