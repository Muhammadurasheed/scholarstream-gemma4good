import asyncio
import structlog
import json
from app.infrastructure.memory_broker import broker
from app.services.matching_engine import matching_engine
from app.database import db
from app.models import Scholarship, DeepUserProfile

logger = structlog.get_logger()

class MatchingWorker:
    """
    Consumes: opportunity.enriched.v1 from Internal Broker
    Action: Matches opportunities against Active Users
    Produces: user.notifications.v1 (via Internal Broker)
    """

    def __init__(self):
        self.topic_in = "opportunity.enriched.v1"
        self.topic_out = "user.matches.v1"
        self.running = False
    
    async def start(self):
        """Start the matching worker by subscribing to the broker"""
        logger.info("Matching Worker Started (Memory Mesh mode)")
        self.running = True
        await broker.subscribe(self.topic_in, self.handle_enriched_opportunity)

    async def handle_enriched_opportunity(self, payload: dict):
        """
        Handle an incoming enriched opportunity event.
        """
        try:
            # 1. Parse Opportunity from enriched payload
            # The Refinery sends { 'enriched_data': { ... } }
            opp_data = payload.get('enriched_data', {})
            if not opp_data:
                logger.warning("Matching Worker received empty enriched data")
                return

            opp = Scholarship(**opp_data)
            logger.info("Matching Worker processing", opp_id=opp.id, title=opp.title)
            
            # 2. Fetch Active Users
            users = await db.get_all_users()
            
            matched_count = 0
            
            for user in users:
                deep_profile = self._ensure_deep_profile(user)
                
                # 3. Calculate Score
                score = await matching_engine.calculate_match_score(opp, deep_profile)
                
                # 4. Filter & Notify
                if score >= 50:
                    opp.match_score = score
                    await db.save_user_match(user.id, opp)
                    
                    # Notify via Internal Broker
                    await self._notify_user(user.id, opp)
                    matched_count += 1
            
            logger.info("Matching Complete", opp_id=opp.id, matched_users=matched_count)

        except Exception as e:
            logger.error("Matching Worker failed", error=str(e))

    def _ensure_deep_profile(self, user_data) -> DeepUserProfile:
        """Helper to cast DB user to DeepUserProfile"""
        if isinstance(user_data, DeepUserProfile):
            return user_data
        return DeepUserProfile(**user_data.dict())

    async def _notify_user(self, user_id: str, opp: Scholarship):
        """Publish match to User Notification Stream in Internal Broker"""
        await broker.publish(
            topic=self.topic_out,
            key=user_id,
            payload={
                "type": "new_match",
                "opportunity_id": opp.id,
                "score": opp.match_score,
                "title": opp.title,
                "timestamp": opp.deadline_timestamp
            }
        )

# Global instance
matching_worker = MatchingWorker()
