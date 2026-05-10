"""
ScholarStream Chat Service — V5 (Gemma Native)
Redirects all chat traffic to the Gemma 4 ReAct Agent.
Gemini has been completely removed to comply with the Gemma 4 Good hackathon.
"""
import structlog
from app.services.gemma_chat_service import gemma_chat_service

logger = structlog.get_logger()

# Direct export of the Gemma service
# This maintains the 'chat_service' name for existing imports but ensures 0% Gemini usage.
chat_service = gemma_chat_service

logger.info("Chat Service: GEMMA NATIVE REDIRECT ACTIVE")
