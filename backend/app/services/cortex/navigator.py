
import asyncio
import structlog
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.crawler_service import crawler_service
from app.services.discovery_pulse import discovery_pulse
import random
import string

logger = structlog.get_logger()

class Sentinel:
    """
    Proactive Background Worker (Cortex V2).
    Delegates mission execution to Hunter Drones (UniversalCrawlerService).
    """
    
    """
    COMPREHENSIVE TARGET LIST V2 - All opportunity sources
    These URLs are crawled with Playwright stealth to bypass anti-bot
    EXPANDED: Added more hackathon platforms, bounties, and grants
    """
    TARGETS = [
    # ======== HACKATHONS (Global) ========
    # "https://devpost.com/hackathons", # REMOVED: using DevPostDeepScraper
    "https://mlh.io/seasons/2026/events",
        "https://angelhack.com/events/",
        "https://www.hackquest.io/hackathons",
        "https://devfolio.co/hackathons",
        "https://hackerearth.com/challenges/",
        "https://lablab.ai/event",  # AI Hackathons
        # "https://unstop.com/hackathons",  # Indian ecosystem but global - REMOVED: using UnstopDeepScraper
        "https://hackathon.io/events",  # Hackathon aggregator
        "https://taikai.network/hackathons",
        "https://www.bemyapp.com/events/",
        "https://eventornado.com/",
        "https://gitcoin.co/hackathons",
        
        # ======== BOUNTIES & BUG BOUNTIES ========
        "https://immunefi.com/explore",
        "https://gitcoin.co/grants-stack/explorer",
        "https://hackerone.com/bug-bounty-programs",
        "https://bugcrowd.com/programs",
        "https://intigriti.com/researchers/bug-bounty-programs",
        "https://bountycaster.xyz/",  # Web3 bounties
        "https://earn.superteam.fun/bounties/",  # Solana ecosystem
        "https://replit.com/bounties",
        "https://www.algorand.foundation/bounties",
        "https://dorahacks.io/bugbounty", # DoraHacks Bounties
        "https://dorahacks.io/grant",  # DoraHacks Grants
        
        # ======== WEB3 GRANTS & ECOSYSTEMS ========
        "https://questbook.xyz/",
        "https://grants.gitcoin.co/",
        "https://aave.com/grants/",
        "https://compound.finance/grants",
        "https://ethereum.org/en/community/grants/",
        "https://solana.com/grants",
        "https://near.org/grants/",
        "https://stacks.org/grants",
        
        # ======== COMPETITIONS ========
        "https://www.kaggle.com/competitions",
        "https://codeforces.com/contests",
        "https://topcoder.com/challenges",
        "https://www.codechef.com/contests",
        "https://atcoder.jp/contests",
        "https://leetcode.com/contest/",
        
        # ======== SCHOLARSHIPS (Global Focus) ========
        "https://bold.org/scholarships/",
        "https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory",
        "https://www.fastweb.com/college-scholarships",
        "https://www.niche.com/colleges/scholarships/",
        "https://www.unigo.com/scholarships/all",
        "https://www.goingmerry.com/scholarships",
        "https://www.scholarshipamerica.org/browse-scholarships/",
        "https://www.internationalscholarships.com/",
        
        # ======== INTERNSHIPS (Tech Hubs) ========
        "https://www.internships.com/search/posts?keywords=software%20engineering",
        "https://www.levels.fyi/internships/",
        "https://wellfound.com/role/l/internship/software-engineer",

        # ======== DEEP WEB & SOCIAL (Cortex V3 Core) ========
        "https://www.reddit.com/r/scholarships/",
        "https://www.reddit.com/r/csMajors/",
        "https://www.linkedin.com/jobs/search?keywords=fellowship",
        "https://twitter.com/search?q=tech+fellowship+grant",
    ]

    async def patrol(self):
        """
        Deploy Hunter Drones to patrol targets.
        Uses batched, staggered execution to prevent 429 rate limits.
        """
        mission_id = "patrol_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        logger.info("Sentinel deploying Hunter Drones", target_count=len(self.TARGETS), mission_id=mission_id)
        
        discovery_pulse.announce_mission(mission_id, "Target Selection", "active")
        
        try:
            # Staggered patrol: batch targets to avoid overwhelming Gemma
            BATCH_SIZE = 5
            INTER_BATCH_DELAY = 15  # seconds between batches
            INTRA_BATCH_DELAY = 3   # seconds between URLs in a batch
            
            for i in range(0, len(self.TARGETS), BATCH_SIZE):
                batch = self.TARGETS[i:i + BATCH_SIZE]
                batch_num = (i // BATCH_SIZE) + 1
                total_batches = (len(self.TARGETS) + BATCH_SIZE - 1) // BATCH_SIZE
                
                logger.info(
                    f"Sentinel patrol batch {batch_num}/{total_batches}",
                    urls=[u.split('//')[-1][:40] for u in batch],
                    mission_id=mission_id,
                )
                
                # Crawl batch with staggered starts
                for url in batch:
                    # Announce specific target to the dashboard for granular telemetry
                    domain = url.split('//')[-1].split('/')[0]
                    discovery_pulse.announce_mission(mission_id, f"Scanning {domain}", "active")
                    
                    await crawler_service.crawl_and_stream([url], intent="patrol", mission_id=mission_id)
                    await asyncio.sleep(INTRA_BATCH_DELAY)
                
                # Pause between batches for rate limit breathing room
                if i + BATCH_SIZE < len(self.TARGETS):
                    await asyncio.sleep(INTER_BATCH_DELAY)
            
            discovery_pulse.complete_mission(mission_id, found_count=len(self.TARGETS))
        except Exception as e:
            logger.error("Sentinel patrol mission failed", error=str(e))
            discovery_pulse.complete_mission(mission_id, found_count=0)

    async def deep_scout_patrol(self, user_profile):
        """
        Cortex V3 Deep Scout -- Gemma-FREE Python Intelligence Engine.
        Gemma is reserved for extraction only. We build hyper-targeted
        direct URLs from the user's Digital DNA using pure Python logic.
        100% resilient -- never fails due to LLM rate limits.
        """
        mission_id = "deep_scout_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

        major = user_profile.get("major", "Computer Science")
        country = user_profile.get("country", "Nigeria")
        interests = user_profile.get("interests", ["AI", "Blockchain"])
        major_slug = major.replace(" ", "+").lower()
        top_interest = (interests[0] if interests else "AI").replace(" ", "+").lower()

        try:
            # === PHASE 1: Profile Analysis ===
            discovery_pulse.announce_mission(mission_id, f"[CORTEX] Analyzing Digital DNA: {major} / {country}", "active")
            logger.info("Deep Scout: Digital DNA extracted", major=major, country=country, interests=interests[:3], mission_id=mission_id)
            await asyncio.sleep(1)

            discovery_pulse.announce_mission(mission_id, f"[CORTEX] Geolocation strategy: 40% Global / 30% Africa / 30% {country}", "active")
            await asyncio.sleep(1)

            # === PHASE 2: Build Hyper-Targeted Direct URLs from Profile ===
            targets = [
                {"url": f"https://www.reddit.com/r/scholarships/search/?q={major_slug}+{top_interest}&sort=new&t=year",
                 "label": f"Scanning Reddit r/scholarships for {major} signals", "platform": "Reddit"},
                {"url": f"https://www.reddit.com/r/cscareerquestions/search/?q=fellowship+grant+{major_slug}&sort=new",
                 "label": f"Deep Scanning r/cscareerquestions for {major} fellowships", "platform": "Reddit"},
                {"url": "https://mastercardfdn.org/all/scholars/",
                 "label": "Analyzing MasterCard Foundation African Scholars portal", "platform": "MasterCard Foundation"},
                {"url": f"https://www.linkedin.com/jobs/search/?keywords={major_slug}+fellowship+africa&f_WT=2",
                 "label": f"Patrolling LinkedIn for {major} opportunities in Africa", "platform": "LinkedIn"},
                {"url": f"https://www.reddit.com/r/Nigeria/search/?q={major_slug}+scholarship+grant&sort=new",
                 "label": f"Hyper-Local Search: Nigeria r/scholarship for {major}", "platform": "Reddit"},
            ]

            # === PROFILE-TYPE AWARE TARGETS (Core Personalization Engine) ===
            major_lower = major.lower()
            interests_str = " ".join([i.lower() for i in interests])
            combined_profile = f"{major_lower} {interests_str}"

            if any(kw in combined_profile for kw in ["medicine", "medical", "health", "nursing", "pharmacy", "biology", "biochem", "clinical"]):
                discovery_pulse.announce_mission(mission_id, f"[DNA MATCH] Nursing/Medical Profile detected. Prioritizing Life Science portals.", "active")
                targets += [
                    {"url": "https://www.niaid.nih.gov/grants-contracts/training-fellowships",
                     "label": "Scanning NIH NIAID Clinical Research Fellowships", "platform": "NIH"},
                    {"url": "https://www.hhmi.org/programs/gilliam-fellowships",
                     "label": "Analyzing HHMI Gilliam Fellowships (Life Sciences)", "platform": "HHMI"},
                    {"url": "https://www.who.int/careers/fellowship-programmes",
                     "label": "Patrolling World Health Organization (WHO) Global Fellowships", "platform": "WHO"},
                    {"url": f"https://www.reddit.com/r/medicalschool/search/?q=scholarship+fellowship+grant&sort=new",
                     "label": "Searching r/medicalschool for niche medical grants", "platform": "Reddit"},
                ]
            
            elif any(kw in combined_profile for kw in ["computer", "software", "ai", "ml", "blockchain", "coding"]):
                discovery_pulse.announce_mission(mission_id, f"[DNA MATCH] Tech/Engineering Profile detected. Prioritizing Hackathon & Bounty portals.", "active")
                targets += [
                    {"url": "https://ethereum.foundation/grants/",
                     "label": "Scanning Ethereum Foundation Ecosystem Grants", "platform": "Ethereum Foundation"},
                    {"url": "https://mlh.io/seasons/2026/events",
                     "label": "Patrolling MLH Season 2026 Hackathons", "platform": "MLH"},
                    {"url": "https://immunefi.com/explore",
                     "label": "Analyzing Immunefi for security bounties", "platform": "Immunefi"},
                ]

            elif any(kw in combined_profile for kw in ["art", "design", "music", "film", "fashion", "creative", "architecture"]):
                discovery_pulse.announce_mission(mission_id, f"[DNA MATCH] Creative/Arts Profile detected. Prioritizing Residency & Arts Grant portals.", "active")
                targets += [
                    {"url": "https://www.nea.gov/grants",
                     "label": "Scanning NEA National Endowment for the Arts Grants", "platform": "NEA"},
                    {"url": "https://www.nyfa.org/awards-grants/",
                     "label": "Analyzing NYFA New York Foundation for the Arts", "platform": "NYFA"},
                ]

            # Universal: Smart Google search for the user's specific major + year
            targets.append(
                {"url": f"https://www.google.com/search?q={major_slug}+fellowship+scholarship+2026+apply",
                 "label": f"Executing Smart Search: {major} fellowships 2026", "platform": "Google"}
            )

            logger.info("Deep Scout: Target manifest built", count=len(targets), mission_id=mission_id)
            await asyncio.sleep(1)

            # === PHASE 3: Execute Drone Missions with Granular Telemetry ===
            scanned = 0
            for i, target in enumerate(targets):
                try:
                    # Update label to show sequence
                    label = f"[DRONE-{i+1:02d}] {target['label']}"
                    discovery_pulse.announce_mission(mission_id, label, "active")
                    
                    logger.info("Deep Scout drone deployed", platform=target["platform"], url=target["url"][:60], mission_id=mission_id)
                    await crawler_service.crawl_and_stream([target["url"]], intent="deep_scout", mission_id=mission_id)
                    scanned += 1
                    await asyncio.sleep(3)
                except Exception as drone_err:
                    err_msg = str(drone_err) or type(drone_err).__name__
                    logger.warning("Deep Scout drone aborted", platform=target["platform"], error=err_msg[:80], mission_id=mission_id)
                    discovery_pulse.announce_mission(mission_id, f"[ABORT] Rerouting from {target['platform']}: Connection unstable", "active")
                    await asyncio.sleep(1)

            discovery_pulse.complete_mission(mission_id, found_count=scanned)
            logger.info("Deep Scout patrol complete", scanned=scanned, total=len(targets), mission_id=mission_id)

        except Exception as e:
            err_msg = str(e) or type(e).__name__ or "UnknownError"
            logger.error("Deep Scout mission failed", error=err_msg, mission_id=mission_id)
            discovery_pulse.complete_mission(mission_id, found_count=0)


class Scout:
    """
    Reactive On-Demand Worker.
    Triggered by Chat requests to perform targeted searches via Hunter Drones.
    """
    
    async def execute_mission(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a targeted search mission.
        """
        mission_id = "scout_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        logger.info("Scout dispatching drone squad", mission=query, mission_id=mission_id)
        
        discovery_pulse.announce_mission(mission_id, f"Searching: {query}", "active")
        
        # 1. FAANG-Grade Query Expansion (Dorks)
        def generate_dorks(q: str):
            q_clean = q.replace(' ', '+')
            return [
                # Atomic Source Hunters (Bypassing Aggregators)
                f"https://duckduckgo.com/?q={q_clean}+site:*.edu+2026",
                f"https://duckduckgo.com/?q={q_clean}+site:*.gov+2026",
                f"https://duckduckgo.com/?q={q_clean}+filetype:pdf",
                f"https://duckduckgo.com/?q={q_clean}+'apply+here'+2026",
                f"https://duckduckgo.com/?q={q_clean}+'submission+portal'+2026",
                # The "Hidden Corners" (Deep Web Signals)
                f"https://duckduckgo.com/?q=site:reddit.com+{q_clean}+opportunity",
                f"https://duckduckgo.com/?q=site:linkedin.com/posts+{q_clean}+hackathon",
                f"https://duckduckgo.com/?q=site:x.com+{q_clean}+'register'+now",
                # Niche/Ecosystem Hubs (Only the high-signal ones)
                f"https://www.google.com/search?q=site:gitcoin.co+{q_clean}",
                f"https://www.google.com/search?q=site:bounties.network+{q_clean}",
            ]
        
        search_urls = generate_dorks(query)
        
        # 2. Dispatch Drones
        # Note: crawl_and_stream handles browser context and stealth
        try:
            await crawler_service.crawl_and_stream(search_urls, intent="scout_search", mission_id=mission_id)
            return [{"url": u, "status": "dispatched"} for u in search_urls]
        except Exception as e:
            logger.error("Scout mission failed", error=str(e))
            return []

# Global Instances
sentinel = Sentinel()
scout = Scout()
