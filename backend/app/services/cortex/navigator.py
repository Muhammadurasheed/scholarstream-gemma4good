
import asyncio
import structlog
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.crawler_service import crawler_service
from app.services.tavily_service import tavily_service
from app.services.discovery_pulse import discovery_pulse
import random
import string
import time

logger = structlog.get_logger()

# ============================================================
# CURATED OPPORTUNITY PLATFORMS (Phase 1: High-Signal, Direct Crawl)
# These are KNOWN listing pages where opportunities are guaranteed.
# Organized by category for DNA-driven selection.
# ============================================================
PLATFORM_REGISTRY = {
    "tech_hackathons": [
        "https://mlh.io/seasons/2026/events",
        "https://devfolio.co/hackathons",
        "https://lablab.ai/event",
        "https://www.hackquest.io/hackathons",
        "https://taikai.network/hackathons",
    ],
    "bounties_web3": [
        "https://immunefi.com/explore",
        "https://earn.superteam.fun/bounties/",
        "https://dorahacks.io/grant",
    ],
    "scholarships_global": [
        "https://bold.org/scholarships/",
        "https://www.fastweb.com/college-scholarships",
        "https://www.niche.com/colleges/scholarships/",
    ],
    "competitions": [
        "https://www.kaggle.com/competitions",
    ],
    "medical_health": [
        "https://www.niaid.nih.gov/grants-contracts/training-fellowships",
        "https://www.hhmi.org/programs/gilliam-fellowships",
    ],
    "creative_arts": [
        "https://www.nyfa.org/awards-grants/",
    ],
}

# DNA keyword → platform category mapping
DNA_PLATFORM_MAP = {
    "tech": ["tech_hackathons", "bounties_web3", "competitions", "scholarships_global"],
    "computer": ["tech_hackathons", "bounties_web3", "competitions", "scholarships_global"],
    "software": ["tech_hackathons", "bounties_web3", "competitions", "scholarships_global"],
    "ai": ["tech_hackathons", "competitions", "scholarships_global"],
    "blockchain": ["bounties_web3", "tech_hackathons"],
    "web3": ["bounties_web3", "tech_hackathons"],
    "cybersecurity": ["bounties_web3", "tech_hackathons", "competitions"],
    "data": ["competitions", "tech_hackathons", "scholarships_global"],
    "medical": ["medical_health", "scholarships_global"],
    "medicine": ["medical_health", "scholarships_global"],
    "nursing": ["medical_health", "scholarships_global"],
    "health": ["medical_health", "scholarships_global"],
    "biology": ["medical_health", "scholarships_global"],
    "art": ["creative_arts", "scholarships_global"],
    "design": ["creative_arts", "tech_hackathons", "scholarships_global"],
    "music": ["creative_arts", "scholarships_global"],
    "law": ["scholarships_global"],
    "business": ["scholarships_global", "tech_hackathons"],
    "finance": ["scholarships_global", "bounties_web3"],
    "engineering": ["tech_hackathons", "competitions", "scholarships_global"],
}


def _resolve_platforms_for_profile(user_profile: Dict[str, Any]) -> List[str]:
    """
    Given a user profile, resolve which platform URLs to crawl.
    Returns a deduplicated, ordered list of URLs from PLATFORM_REGISTRY.
    """
    major = (user_profile.get("major") or "").lower()
    interests = [i.lower() for i in (user_profile.get("interests") or [])]
    combined_signals = f"{major} {' '.join(interests)}"
    
    selected_categories = set()
    
    for keyword, categories in DNA_PLATFORM_MAP.items():
        if keyword in combined_signals:
            selected_categories.update(categories)
    
    # Always include global scholarships
    selected_categories.add("scholarships_global")
    
    # Resolve categories to URLs
    urls = []
    for cat in selected_categories:
        urls.extend(PLATFORM_REGISTRY.get(cat, []))
    
    # Deduplicate while preserving order
    return list(dict.fromkeys(urls))


class Sentinel:
    """
    Proactive Background Worker (Cortex V3 — Revived).
    Phase 1: DNA-driven crawl of CURATED platforms (guaranteed opportunity pages).
    Phase 2: AI-powered Tavily search with domain constraints.
    NO MORE blind 60-URL patrol. Every URL we hit is justified by user DNA.
    """

    async def aggregate_patrol(self):
        """
        [CORTEX V3] DNA-Driven Aggregate Patrol.
        Only activates for patrolling users. If no users → no crawl (saves resources).
        """
        mission_id = "aggregate_patrol_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        try:
            # 1. Fetch DNA Signals from active user base
            from app.database import db
            active_users = await db.get_patrolling_users()
            
            if not active_users:
                logger.info("No patrolling users found. Skipping aggregate patrol (no wasted crawls).")
                await discovery_pulse.announce_mission(
                    mission_id, "No active users with patrol enabled — Standing by", "completed"
                )
                return

            await discovery_pulse.announce_mission(mission_id, f"Aggregating DNA for {len(active_users)} patrolling users...", "active")
            
            # 2. Build a merged profile from all active users
            merged_profile = {"major": "", "interests": [], "country": ""}
            majors = set()
            all_interests = set()
            for u in active_users:
                profile = u.get('profile', {})
                if profile.get('major'): majors.add(profile['major'])
                for interest in profile.get('interests', []): all_interests.add(interest)
            
            # Use first user's major as primary, merge interests
            merged_profile["major"] = list(majors)[0] if majors else "General Studies"
            merged_profile["interests"] = list(all_interests)[:10]
            
            await discovery_pulse.announce_mission(
                mission_id, 
                f"Active Signals: {len(majors)} Majors / {len(all_interests)} Interests", 
                "active"
            )
            
            # 3. Phase 1: Crawl DNA-resolved platforms
            platform_urls = _resolve_platforms_for_profile(merged_profile)
            logger.info("Aggregate patrol: DNA-resolved platforms", count=len(platform_urls))
            
            for url in platform_urls[:12]:  # Max 12 platforms per patrol
                domain = url.split('//')[-1].split('/')[0]
                await discovery_pulse.announce_mission(mission_id, f"DNA-Targeted Hunt: {domain}", "active")
                await crawler_service.crawl_and_stream([url], intent="aggregate_patrol", mission_id=mission_id)
                await asyncio.sleep(5)

            discovery_pulse.complete_mission(mission_id, found_count=len(platform_urls))
            logger.info("Aggregate DNA patrol complete", target_count=len(platform_urls), mission_id=mission_id)

        except Exception as e:
            logger.error("Aggregate patrol failed", error=str(e))
            discovery_pulse.complete_mission(mission_id, found_count=0)

    async def deep_scout_patrol(self, user_profile):
        """
        Cortex V3 Deep Scout — TWO-PHASE Intelligence Engine.
        
        Phase 1: Crawl curated platform pages resolved from user DNA (fast, reliable).
        Phase 2: Tavily AI search with opportunity-focused queries (broader, AI-powered).
        
        Both phases feed the EventBroker → Refinery → WebSocket pipeline.
        """
        mission_id = "deep_scout_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

        # Extract profile data
        user_id = user_profile.get("id") or user_profile.get("uid")
        is_demo = user_id == "demo_guest_user"

        # Support nested 'profile' key (Firestore format)
        profile_data = user_profile.get("profile", user_profile) if isinstance(user_profile, dict) else user_profile
        major = profile_data.get("major", "Computer Science")
        country = profile_data.get("country", "Nigeria")
        interests = profile_data.get("interests", ["AI", "Blockchain"])
        academic_status = profile_data.get("academic_status", "Undergraduate")
        
        if is_demo:
             await discovery_pulse.announce_mission(mission_id, "Judge Mode Activated: Deploying Ultra-Priority Drones", "active")

        scanned = 0

        try:
            # =========================================================
            # PHASE 1: Curated Platform Crawl (DNA-Resolved)
            # Fast, reliable — guaranteed to hit real opportunity pages.
            # =========================================================
            await discovery_pulse.announce_mission(
                mission_id, "[PHASE 1] Analyzing Digital DNA — Selecting target platforms...", "active"
            )

            platform_urls = _resolve_platforms_for_profile(profile_data)
            logger.info("Deep Scout Phase 1: DNA-resolved platforms", count=len(platform_urls), user_id=user_id)

            # Crawl top 8 most relevant platforms
            for i, url in enumerate(platform_urls[:8]):
                domain = url.split('//')[-1].split('/')[0]
                await discovery_pulse.announce_mission(
                    mission_id, f"[PHASE 1] Deploying drone to {domain}", "active"
                )
                await crawler_service.crawl_and_stream([url], intent="deep_scout_phase1", mission_id=mission_id)
                scanned += 1
                await asyncio.sleep(3)

            # =========================================================
            # PHASE 2: AI-Powered Tavily Discovery (DNA-Targeted Queries)
            # Broader search with opportunity-focused constraints.
            # =========================================================
            await discovery_pulse.announce_mission(
                mission_id, "[PHASE 2] Generating AI-powered search strategy...", "active"
            )

            # Get Gemma's hunt strategy
            from app.services.gemma_service import gemma_service
            try:
                strategy = await gemma_service.generate_hunt_strategy({
                    "major": major,
                    "interests": interests,
                    "country": country,
                    "academic_status": academic_status,
                })
                thought = strategy.get("thought", f"Searching for {major} opportunities globally.")
                search_queries = strategy.get("search_queries", [])
            except Exception as gemma_err:
                logger.warning("Deep Scout: Strategy generation failed, using DNA Fallback", error=str(gemma_err))
                thought = f"Using DNA-driven fallback for {major} in {country}."
                major_lower = major.lower().replace(" ", "+")
                top_interest = (interests[0] if interests else "technology").lower()
                search_queries = [
                    f"{major} scholarships for {country} students 2025 2026 apply now",
                    f"{top_interest} hackathons 2025 2026 registration open",
                    f"fully funded {major} fellowships {country} deadline",
                    f"{major} grants for students apply {country}",
                ]
            
            await discovery_pulse.announce_mission(
                mission_id, f"[PHASE 2] DNA Analysis Complete", "active", 
                payload={"thought": thought}
            )
            logger.info("Deep Scout: Strategy generated", thought=thought, queries=search_queries[:3])
            await asyncio.sleep(1)

            # Execute Tavily searches with domain constraints
            from app.main import broker
            from app.config import settings

            for i, query in enumerate(search_queries[:4]):  # Max 4 queries
                try:
                    label = f"[SEARCH-{i+1:02d}] AI-Scout: {query[:50]}..."
                    await discovery_pulse.announce_mission(
                        mission_id, label, "active", 
                        payload={"thought": f"Searching the web: {query}"}
                    )
                    
                    # Use Tavily with domain constraints (blocks research/blog sites)
                    results = await tavily_service.search_opportunities(query, max_results=5)
                    
                    for j, result in enumerate(results):
                        scanned += 1
                        res_url = result.get("url", "")
                        res_title = result.get("title", "Unknown")[:60]
                        
                        await discovery_pulse.announce_mission(
                            mission_id, f"[FOUND-{scanned:02d}] {res_title}", "active"
                        )
                        
                        # Transmit to Refinery via EventBroker
                        payload = {
                            "url": res_url,
                            "title": result.get("title"),
                            "html": result.get("raw_content") or result.get("content"),
                            "crawled_at": time.time(),
                            "source": "Tavily AI",
                            "intent": "deep_scout_phase2",
                            "agent_type": "Tavily-Scout-V2",
                            "mission_id": mission_id
                        }
                        
                        await broker.publish(
                            topic=settings.topic_raw_html,
                            key=res_url,
                            payload=payload
                        )
                        
                    await asyncio.sleep(2)
                except Exception as search_err:
                    logger.error("Tavily search iteration failed", error=str(search_err))
                    discovery_pulse.report_challenge(mission_id, f"Search failure: {str(search_err)[:50]}")

            discovery_pulse.complete_mission(mission_id, found_count=scanned)
            logger.info("Deep Scout patrol complete", scanned=scanned, mission_id=mission_id)
            
            # === ZERO-DB GENESIS: Mark first hunt complete ===
            if user_id and scanned > 0:
                try:
                    from app.database import db
                    await db.mark_first_hunt_complete(user_id)
                    logger.info("First hunt complete flag set", user_id=user_id, drones_deployed=scanned)
                except Exception as flag_err:
                    logger.warning("Could not set first_hunt_complete flag", error=str(flag_err))

        except Exception as e:
            err_msg = str(e) or type(e).__name__ or "UnknownError"
            logger.error("Deep Scout mission failed", error=err_msg, mission_id=mission_id)
            discovery_pulse.complete_mission(mission_id, found_count=0)

    async def heavy_hunt(self, platforms: List[str] = None):
        """
        Manual high-intensity hunt for specific platforms.
        V2: Uses PLATFORM_REGISTRY instead of blind hardcoded TARGETS.
        """
        mission_id = "heavy_hunt_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        logger.info("Sentinel deploying HEAVY HUNT mission", platforms=platforms, mission_id=mission_id)
        
        await discovery_pulse.announce_mission(mission_id, "Heavy Hunt Mission Deployed", "active")
        
        # Collect all platform URLs
        all_urls = []
        for category_urls in PLATFORM_REGISTRY.values():
            all_urls.extend(category_urls)
        all_urls = list(dict.fromkeys(all_urls))  # Deduplicate
        
        # Filter by platform name if specified
        if platforms:
            all_urls = [t for t in all_urls if any(p.lower() in t.lower() for p in platforms)]
            
        for url in all_urls:
            try:
                domain = url.split('//')[-1].split('/')[0]
                await discovery_pulse.announce_mission(mission_id, f"Scanning {domain}", "active")
                await crawler_service.crawl_and_stream([url], intent="heavy_hunt", mission_id=mission_id)
            except Exception as e:
                logger.error("Heavy Hunt drone failure", url=url, error=str(e))
                
        discovery_pulse.complete_mission(mission_id, found_count=len(all_urls))
        logger.info("Heavy Hunt mission complete", mission_id=mission_id)


class Scout:
    """
    Reactive On-Demand Worker.
    Triggered by Chat requests to perform targeted searches via Hunter Drones.
    """
    
    async def execute_mission(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a targeted search mission via Tavily AI.
        """
        mission_id = "scout_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        logger.info("Scout dispatching Tavily drone", mission=query, mission_id=mission_id)
        
        await discovery_pulse.announce_mission(mission_id, f"Executing Targeted AI Hunt: {query}", "active", payload={"thought": f"I am using Tavily AI to find exact matches for '{query}'."})
        
        try:
            # 1. Execute Tavily Search with domain constraints
            results = await tavily_service.search_opportunities(query, max_results=10)
            
            # 2. Process results
            found_data = []
            from app.main import broker
            from app.config import settings
            
            for result in results:
                url = result.get("url")
                title = result.get("title")
                
                payload = {
                    "url": url,
                    "title": title,
                    "html": result.get("raw_content") or result.get("content"),
                    "crawled_at": time.time(),
                    "source": "Tavily Scout",
                    "intent": "scout_search",
                    "agent_type": "Tavily-Scout-V2",
                    "mission_id": mission_id
                }
                
                await broker.publish(
                    topic=settings.topic_raw_html,
                    key=url,
                    payload=payload
                )
                found_data.append({"url": url, "title": title})
            
            discovery_pulse.complete_mission(mission_id, found_count=len(found_data))
            return found_data
            
        except Exception as e:
            logger.error("Scout Tavily mission failed", error=str(e))
            discovery_pulse.report_challenge(mission_id, f"Scout failure: {str(e)[:50]}")
            return []

# Global Instances
sentinel = Sentinel()
scout = Scout()
