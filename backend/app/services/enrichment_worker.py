import asyncio
import json
import time
from typing import List, Dict, Any
import structlog

from app.config import settings
from app.infrastructure.memory_broker import broker
from app.services.ai_enrichment_service import ai_enrichment_service
from app.services.discovery_pulse import discovery_pulse

logger = structlog.get_logger()

class EnrichmentWorker:
    """
    AI REQUEST CONSUMER (The "Refinery")
    Consumes RAW HTML from the Internal Broker.
    Extracts structured opportunities using Gemini/Gemma.
    Publishes enriched results back to the mesh.
    """
    
    def __init__(self):
        self.topic_in = "cortex.raw.html.v1"
        self.topic_out = "opportunity.enriched.v1"
        self.running = False
        
    async def start(self):
        """Start the AI processing loop by subscribing to the broker"""
        logger.info("Starting AI Refinery Worker (Memory Mesh mode)...")
        self.running = True
        await broker.subscribe(self.topic_in, self.handle_event)
        logger.info(f"Subscribed to {self.topic_in}")

    async def handle_event(self, payload: Dict[str, Any]):
        """Handle incoming raw HTML event from the broker"""
        try:
            # PROCESS PAYLOAD
            start_time = time.time()
            opportunities = []
            
            url = payload.get("url")
            mission_id = payload.get("mission_id")
            
            # Check for pre-extracted data
            if payload.get("extracted_data"):
                logger.info("Using pre-extracted data (Deep Scraper Bypass)", url=url)
                opportunities = [payload.get("extracted_data")]
            elif payload.get("html"):
                # Extract using AI Enrichment Service (Batch mode with 1 item for simplicity)
                opportunities = await ai_enrichment_service.extract_opportunities_from_html_batch([payload])
            
            duration = time.time() - start_time
            
            if not opportunities:
                logger.warning(f"No opportunities extracted", duration=f"{duration:.2f}s", url=url)
                if mission_id:
                    discovery_pulse.complete_mission(mission_id, found_count=0)
                return
                
            logger.info(f"Discovery Yield: {len(opportunities)} items", duration=f"{duration:.2f}s", url=url)
            if mission_id:
                discovery_pulse.complete_mission(mission_id, found_count=len(opportunities))

            # PUBLISH RESULTS
            for opp in opportunities:
                enriched_message = {
                    'source': "internal-mesh", 
                    'enriched_data': opp,
                    'enriched_at': time.time(),
                    'ai_model': settings.gemini_model,
                    'origin_url': opp.get('url') or url
                }
                
                await broker.publish(
                    topic=self.topic_out,
                    key="ai-refinery",
                    payload=enriched_message
                )
                        
        except Exception as e:
            logger.error("Refinery processing failed", error=str(e))

    def stop(self):
        """Stop the worker gracefully"""
        self.running = False

    def close(self):
        """Close resources"""
        logger.info("Closing AI Refinery Worker")

# Global instance
enrichment_worker = EnrichmentWorker()
