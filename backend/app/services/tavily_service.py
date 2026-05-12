
import httpx
import structlog
from typing import List, Dict, Any, Optional
from app.config import settings

logger = structlog.get_logger()

# Known high-quality opportunity platforms — Tavily will prefer these
OPPORTUNITY_DOMAINS = [
    # Scholarships
    "bold.org", "scholarships.com", "fastweb.com", "niche.com",
    "goingmerry.com", "scholarshipamerica.org", "unigo.com",
    "internationalscholarships.com", "bachelorsportal.com",
    "scholarshipsads.com", "opportunitiesforafricans.com",
    "afterschoolafrica.com",
    # Hackathons
    "devpost.com", "mlh.io", "devfolio.co", "hackerearth.com",
    "lablab.ai", "dorahacks.io", "hackquest.io", "taikai.network",
    "bemyapp.com", "eventornado.com", "unstop.com",
    # Bug Bounties
    "immunefi.com", "hackerone.com", "bugcrowd.com", "intigriti.com",
    # Grants & Web3
    "gitcoin.co", "questbook.xyz", "earn.superteam.fun",
    "ethereum.org", "solana.com",
    # Competitions
    "kaggle.com", "topcoder.com",
    # General
    "opportunities.com", "fundingcircle.com",
]

# Domains that should NEVER appear in results — blogs, PDFs, research, news
BLOCKED_DOMAINS = [
    "pmc.ncbi.nlm.nih.gov", "arxiv.org", "researchgate.net",
    "medium.com", "wikipedia.org", "reddit.com", "quora.com",
    "youtube.com", "twitter.com", "facebook.com", "linkedin.com",
    "news.ycombinator.com", "stackoverflow.com",
]


class TavilySearchService:
    """
    Tavily AI Search Service (Cortex V3)
    Replaces brittle scrapers with AI-powered search for high-fidelity discovery.
    V2: Domain-constrained for opportunity-only results.
    """
    
    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.base_url = "https://api.tavily.com/search"
        
        if not self.api_key:
            logger.warning("TAVILY_API_KEY not found in environment. Search capabilities will be limited.")

    async def search_opportunities(
        self, 
        query: str, 
        search_depth: str = "advanced",
        include_raw_content: bool = True,
        max_results: int = 10,
        include_domains: List[str] = None,
        exclude_domains: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute an AI-powered search for opportunities.
        V2: Adds domain constraints and result validation.
        """
        if not self.api_key:
            logger.error("Tavily search aborted: No API Key")
            return []

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "include_raw_content": include_raw_content,
            "max_results": max_results,
            "include_answer": True
        }
        
        # Apply domain constraints
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        else:
            # Always exclude known non-opportunity domains
            payload["exclude_domains"] = BLOCKED_DOMAINS

        logger.info("Tavily searching for opportunities", query=query, depth=search_depth)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                results = data.get("results", [])
                
                # Post-filter: Validate each result URL
                validated = []
                for r in results:
                    url = r.get("url", "").lower()
                    
                    # Skip if URL contains blocked domain
                    if any(blocked in url for blocked in BLOCKED_DOMAINS):
                        logger.debug("Tavily result filtered out (blocked domain)", url=url[:60])
                        continue
                    
                    # Skip obvious non-opportunity pages (PDFs, research papers)
                    if url.endswith(".pdf") or "/article/" in url or "/paper/" in url:
                        logger.debug("Tavily result filtered out (non-opportunity)", url=url[:60])
                        continue
                    
                    validated.append(r)
                
                logger.info(
                    "Tavily search complete", 
                    results_found=len(results), 
                    after_filter=len(validated),
                    query=query
                )
                return validated
                
            except httpx.HTTPStatusError as e:
                logger.error("Tavily API HTTP error", status=e.response.status_code, text=e.response.text)
                return []
            except Exception as e:
                logger.error("Tavily search failed", error=str(e))
                return []

    async def search_targeted_platforms(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search ONLY within known opportunity platforms.
        Used for Phase 1 (high-confidence) discovery.
        """
        return await self.search_opportunities(
            query=query,
            include_domains=OPPORTUNITY_DOMAINS,
            max_results=max_results,
            search_depth="advanced",
            include_raw_content=True,
        )

# Global Instance
tavily_service = TavilySearchService()
