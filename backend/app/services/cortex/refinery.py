
import structlog
import json
import asyncio
from datetime import datetime
from typing import Optional, List

from app.services.cortex.reader_llm import reader_llm
from app.models import OpportunitySchema
from app.config import settings
from app.database import db

logger = structlog.get_logger()

class RefineryService:
    """
    The Refinery: Turns Raw Data into Verified Intelligence.
    Consumes: cortex.raw.html.v1
    Produces: opportunity.enriched.v1
    """

    # Keywords that indicate a page LIKELY contains opportunities
    OPPORTUNITY_SIGNALS = [
        "apply", "deadline", "submit", "register", "prize", "award",
        "scholarship", "fellowship", "grant", "hackathon", "bounty",
        "competition", "challenge", "program", "opportunity", "fund",
        "stipend", "internship", "residency", "call for", "open to",
        "eligible", "application", "registration", "sponsor",
    ]

    # URL patterns that are almost certainly NOT opportunity pages
    BLOCKED_URL_PATTERNS = [
        "/article/", "/blog/", "/news/", "/press/", "/about/",
        ".pdf", "/wiki/", "/paper/", "/publication/",
        "pmc.ncbi.nlm", "arxiv.org", "researchgate.net",
        "medium.com", "wikipedia.org", "stackoverflow.com",
    ]

    async def process_raw_event(self, key: str, value: dict):
        """
        Process a single raw event from the stream.
        V3: Added content quality gate to save Gemma tokens.
        """
        url = value.get("url")
        raw_html = value.get("html")
        source = value.get("source")
        agent_type = value.get("agent_type", "Unknown")
        
        logger.info("Refinery V3: Processing Raw Event", url=url, source=source, agent=agent_type)
        
        # ========================================================
        # CONTENT QUALITY GATE: Don't waste Gemma on garbage pages
        # ========================================================
        
        # Gate 1: Empty HTML
        if not raw_html:
            logger.warning("Empty HTML in raw event", url=url)
            return

        # Gate 2: Blocked URL patterns (research papers, blogs, etc.)
        url_lower = (url or "").lower()
        if any(pattern in url_lower for pattern in self.BLOCKED_URL_PATTERNS):
            logger.info("Refinery: URL blocked by pattern filter", url=url[:60])
            return

        # Gate 3: Content too thin (but allow Tavily content which may be shorter)
        is_tavily = "tavily" in (agent_type or "").lower() or "tavily" in (source or "").lower()
        min_length = 200 if is_tavily else 1500
        
        if len(raw_html) < min_length:
            logger.info("Refinery: Content too thin, skipping", url=url[:60], length=len(raw_html))
            return

        # Gate 4: Opportunity signal check — does this page mention ANY opportunity keywords?
        content_lower = raw_html[:20000].lower()
        signal_count = sum(1 for sig in self.OPPORTUNITY_SIGNALS if sig in content_lower)
        
        if signal_count < 2:
            logger.info("Refinery: Insufficient opportunity signals", url=url[:60], signals=signal_count)
            return

        logger.info("Refinery: Content passed quality gate", url=url[:60], signals=signal_count)

        # ========================================================
        # EXTRACTION: Send to Reader LLM for structured extraction
        # ========================================================
        
        # V2: Extract MULTIPLE opportunities from list pages
        opportunities: List[OpportunitySchema] = await reader_llm.parse_multiple(raw_html, url, max_items=50)
        
        if not opportunities:
            logger.warning("No opportunities extracted", url=url)
            return
        
        logger.info(f"Extracted {len(opportunities)} opportunities from {url[:50]}")
        
        # 2. Process each opportunity in parallel for FAANG-grade speed
        tasks = [self._process_single_opportunity(opportunity) for opportunity in opportunities]
        results = await asyncio.gather(*tasks)
        processed_count = sum(1 for r in results if r is True)
        
        logger.info(f"Refinery Complete: {processed_count}/{len(opportunities)} opportunities processed from {url[:40]}")

    async def _process_single_opportunity(self, opportunity: OpportunitySchema) -> bool:
        """Helper to process a single opportunity and return success/failure"""
        try:
            # 2.1 Strict Expiration Gate
            if self._is_expired(opportunity.deadline_timestamp):
                logger.debug("Dropped Expired", title=opportunity.title[:30] if opportunity.title else "N/A")
                return False

            # 2.2 Geo-Tagging
            opportunity.geo_tags = self._enrich_geo_tags(opportunity)
            
            # 2.3 Type-Tagging
            opportunity.type_tags = self._enrich_type_tags(opportunity)
            
            # 2.4 Deep Verification (Principal Grade)
            # Ensure the name is not junk and URL is likely valid
            if not opportunity.name or len(opportunity.name) < 3:
                return False
            
            # 2.5 Source Intelligence (Categorize for Discovery Depth)
            opportunity.source_tier = self._detect_source_tier(opportunity.source_url)
                
            # Mark as verified
            opportunity.last_verified = datetime.now().isoformat()

            # 3. Publish to Verified Stream
            await self._publish_verified(opportunity)
            return True
            
        except Exception as e:
            logger.error("Failed to process opportunity", error=str(e))
            return False

    def _detect_source_tier(self, url: str) -> str:
        """
        Principal-Grade Source Intelligence.
        Categorizes sources by 'Discovery Depth'.
        """
        url_lower = url.lower()
        
        # TIER 1: Aggregators (Low Discovery Depth, but high volume)
        aggregators = ["devpost.com", "mlh.io", "dorahacks.io", "kaggle.com", "devfolio.co", "hackquest.io", "taikai.network"]
        if any(h in url_lower for h in aggregators):
            return "Aggregator"
            
        # TIER 2: Atomic Sources (High Discovery Depth - The "Hidden" Signal)
        if ".edu" in url_lower or ".gov" in url_lower:
            return "Atomic Source"
            
        # TIER 3: Community/Niche (Reddit, LinkedIn, Foundations)
        if any(h in url_lower for h in ["reddit.com", "linkedin.com", "x.com", ".org", "foundation", "blog"]):
            return "Niche Signal"
            
        return "Standard"

    def _is_expired(self, deadline_ts: int) -> bool:
        """Strict Expiration Logic"""
        if not deadline_ts: return False # Keep if unknown, flag later
        now_ts = int(datetime.now().timestamp())
        return deadline_ts < now_ts

    def _enrich_geo_tags(self, opp: OpportunitySchema) -> List[str]:
        """Auto-detect Global vs Local"""
        tags = set(opp.geo_tags)
        text = (opp.description + " " + str(opp.eligibility_text)).lower()
        
        # Global Indicators
        if any(w in text for w in ["remote", "online", "global", "international", "worldwide"]):
            tags.add("Global")
            
        # Regional Indicators (Example: Nigeria)
        if any(w in text for w in ["nigeria", "lagos", "abuja", "africa"]):
            tags.add("Nigeria")
            
        # Defaults
        if not tags:
            tags.add("Global") # Default to Global if unsure
            
        return list(tags)

    def _enrich_type_tags(self, opp: OpportunitySchema) -> List[str]:
        tags = set(opp.type_tags)
        text = (opp.title + " " + opp.description).lower()
        
        if "hackathon" in text: tags.add("Hackathon")
        if "grant" in text: tags.add("Grant")
        if "scholarship" in text: tags.add("Scholarship")
        if "bounty" in text: tags.add("Bounty")
        
        return list(tags)

    async def handle_raw_html_event(self, payload: dict):
        """
        Event Handler for 'cortex.raw.html' events.
        NOTE: MemoryBroker passes the unwrapped payload directly (not the full event envelope).
        The payload contains: url, title, html, crawled_at, source, intent, agent_type, mission_id
        """
        key = payload.get("url", "unknown")
        await self.process_raw_event(key, payload)

    async def _publish_verified(self, opp: OpportunitySchema):
        """Publish verified opportunity to the Event Bus"""
        # Publish to Event Bus
        from app.main import broker
        from app.config import settings
        
        try:
            await broker.publish(
                topic=settings.topic_enriched_opportunity,
                key=opp.id,
                payload=opp.model_dump()
            )
            logger.info("Verified Opportunity Published to EventBroker", title=opp.title)
        except Exception as e:
            logger.error("EventBroker Publish Failed", error=str(e))
            # Fallback to direct DB save if broker fails (though MemoryBroker shouldn't fail)
            await self._persist_fallback(opp)

    async def _persist_fallback(self, opp: OpportunitySchema):
        """Direct-to-Database Fallback"""
        try:
            await db.save_scholarship(opp)
            logger.info("Fallback: Saved to DB directly", title=opp.title)
        except Exception as e:
            logger.error("Fallback Save Failed", error=str(e))

refinery_service = RefineryService()
