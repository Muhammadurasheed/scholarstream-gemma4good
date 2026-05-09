
import asyncio
import json
import structlog
from typing import Dict, Any, List

from app.infrastructure.memory_broker import broker
from app.services.ai_enrichment_service import ai_enrichment_service

logger = structlog.get_logger()

class ExtractionWorker:
    """
    Consumes raw HTML from the Internal Broker, uses Gemini to extract opportunities,
    and publishes structured JSON back to the broker.
    """

    def __init__(self):
        self.topic_in = "cortex.raw.html.v1"
        self.topic_out = "cortex.raw.opportunities.v1"
        self.running = False
        
    async def start(self):
        """Start the extraction worker by subscribing to the broker"""
        self.running = True
        logger.info(f"Extraction Worker subscribing to {self.topic_in}")
        await broker.subscribe(self.topic_in, self.handle_raw_html)

    async def handle_raw_html(self, payload: Dict[str, Any]):
        """Handle incoming raw HTML event from the broker"""
        try:
            url = payload.get('url')
            html = payload.get('html')
            
            if not url or not html:
                logger.warning("Invalid message payload", payload_keys=payload.keys())
                return

            logger.info(f"Processing HTML from {url}", size=len(html))

            # 1. Extract Opportunities using Gemini (or Intelligence Gateway)
            extracted_opps = await ai_enrichment_service.extract_opportunities_from_html(html, url)
            
            if not extracted_opps:
                logger.warning(f"No opportunities extracted from {url}")
                return
                
            logger.info(f"Extracted {len(extracted_opps)} opportunities from {url}")

            # 2. Publish to Raw Opportunities Stream
            for opp in extracted_opps:
                # Add metadata
                opp['params'] = {
                    'source_url': url,
                    'extracted_at': payload.get('crawled_at')
                }
                
                await broker.publish(
                    topic=self.topic_out,
                    key=opp.get('url', url),
                    payload=opp
                )
                
            logger.info(f"Published {len(extracted_opps)} opportunities to internal mesh")

        except Exception as e:
            logger.error("Error processing event", error=str(e))

    def stop(self):
        self.running = False

# Global instance
extraction_worker = ExtractionWorker()
