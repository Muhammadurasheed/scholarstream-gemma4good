
import structlog
from typing import Optional, Dict, Any, List
from app.config import settings
from app.models import OpportunitySchema
from app.utils.json_utils import robust_json_loads
# NOTE: rate limiting is handled INSIDE the intelligence_gateway → gemma_service layer.
# Do NOT import gemini_rate_limiter here — it caused Gemma calls to be throttled at 30 RPM.
import json
import asyncio
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from app.services.intelligence_gateway import intelligence_gateway

logger = structlog.get_logger()

class ReaderLLM:
    """
    The 'Reader' V2: Turns Raw HTML/Text into Structured JSON.
    UPGRADED: Can extract MULTIPLE opportunities from list pages.
    Natively powered by Gemma 4 via IntelligenceGateway.
    """
    
    def __init__(self):
        logger.info("ReaderLLM initialized via IntelligenceGateway")

    def _clean_html_to_text(self, raw_html: str) -> str:
        """
        DOM PRUNING: Strips noise from massive SPA payloads.
        Converts 1MB of HTML into ~5KB of pure content text.
        """
        if not raw_html:
            return ""
            
        try:
            soup = BeautifulSoup(raw_html, "html.parser")
            
            # Remove invisible/noisy tags
            for element in soup(["script", "style", "noscript", "svg", "path", "nav", "footer", "header", "iframe", "meta", "link"]):
                element.extract()
                
            # Extract text with newlines for readability
            text = soup.get_text(separator='\n', strip=True)
            
            # Collapse multiple newlines/spaces
            text = re.sub(r'\n+', '\n', text)
            text = re.sub(r' {2,}', ' ', text)
            
            return text
        except Exception as e:
            logger.warning("DOM Pruning failed, falling back to raw HTML", error=str(e))
            return raw_html

    async def parse_opportunity(self, raw_text: str, source_url: str) -> Optional[OpportunitySchema]:
        """
        Extracts a SINGLE opportunity from raw text.
        Use parse_multiple for list pages.
        """
        result = await self.parse_multiple(raw_text, source_url, max_items=1)
        return result[0] if result else None

    async def parse_multiple(
        self, 
        raw_text: str, 
        source_url: str, 
        max_items: int = 50
    ) -> List[OpportunitySchema]:
        """
        V2 CORE: Extracts MULTIPLE opportunities from list/aggregator pages.
        This is critical for DevPost, DoraHacks, etc. that show many items per page.
        """
        if not settings.gemma_engine_enabled:
            logger.warning("Gemma AI engine flag is False in settings — proceeding anyway (hackathon mode). Set GEMMA_ENGINE_ENABLED=true in .env to suppress this warning.")

        # DOM Pruning: Clean the raw HTML into pure text
        cleaned_text = self._clean_html_to_text(raw_text)
        
        # Truncate text to avoid token limits (now much safer since it's pure text, not HTML)
        truncated_text = cleaned_text[:80000]
        
        # Detect platform for specialized parsing
        platform_hint = self._detect_platform(source_url)

        # Contextual timescale for accurate extraction
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""
        You are an elite Intelligence Extraction Agent for ScholarStream.
        Today's Date: {current_date}
        Platform context: {platform_hint}
        
        Extract UP TO {max_items} distinct OPPORTUNITIES (Hackathons, Scholarships, Bounties, Grants, Fellowships) from the text below.
        
        CRITICAL ANTI-HALLUCINATION PROTOCOL (IRON GATE):
        1. NEVER extract university course catalogs, seminars, generic jobs, books, podcasts, or reading lists.
        2. If the page only contains courses (e.g. "Theory of Education", "Philosophy 101"), RETURN AN EMPTY ARRAY [].
        3. A valid opportunity MUST have a concrete application process or prize/stipend.
        
        Return a JSON ARRAY. Each item must match this schema:
        {{
            "title": "String (opportunity name)",
            "organization": "String (hosting org/company)",
            "amount": Number (total prize pool in USD. Parse values like '$50K' to 50000. Set to 0 ONLY if truly unknown),
            "amount_display": "Human-readable prize string (e.g. '$50,000', 'Up to $10K')",
            "deadline": "ISO 8601 Date String (YYYY-MM-DD) or null",
            "deadline_timestamp": Number (Unix Timestamp) or null,
            "geo_tags": ["String"] (e.g. ["Global", "Remote", "USA"]),
            "type_tags": ["String"] (e.g. ["Hackathon", "Bounty", "Scholarship"]),
            "description": "Short summary (1-2 sentences)",
            "eligibility_text": "Requirements snippet",
            "source_url": "Direct URL to this specific opportunity (if extractable)"
        }}

        General Rules (STRICT QUALITY CONTROL):
        1. CRITICAL: SKIP any opportunity where the deadline has already passed (Today's Date: {current_date}).
        2. SKIP sections clearly marked as "Ended", "Past", "Closed", or "Finished".
        3. If deadline is missing, use null (don't guess).
        4. If prize is unclear, set amount_display to "Check listing for details" and amount to 0. NEVER use "Varies".
        5. source_url should be the direct link if visible, else use "{source_url}"
        
        Source Page URL: {source_url}
        
        Page Content:
        {truncated_text}
        
        Return ONLY a valid JSON array. No markdown, no explanations. If no valid opportunities exist, return [].
        """

        try:
            # Call AI gateway directly — rate limiting is handled inside gemma_service
            # (uses gemma_rate_limiter at 200 RPM, not the old gemini_rate_limiter at 30 RPM)
            raw_response = await self._call_ai_gateway(prompt)
            
            # Handle potential JSON issues
            if raw_response.startswith("```"):
                raw_response = raw_response.split("```")[1]
                if raw_response.startswith("json"):
                    raw_response = raw_response[4:]
            
            data = robust_json_loads(raw_response)
            
            if data is None:
                logger.warning("Cortex Reader: No valid JSON data extracted from AI response", url=source_url)
                return []
            
            # Ensure it's a list
            if isinstance(data, dict):
                data = [data]
            
            opportunities = []
            from app.services.discovery_pulse import discovery_pulse
            
            for item in data[:max_items]:
                try:
                    # Generate stable ID
                    item_url = item.get('source_url') or item.get('url') or source_url
                    
                    # NORMALIZE URL to prevent 404s and duplication
                    item_url = self._normalize_url(item_url, source_url)
                    item['source_url'] = item_url
                    
                    from app.services.flink_processor import generate_opportunity_id
                    item['id'] = generate_opportunity_id(item)
                    
                    # Map 'title' to 'name' for schema compatibility
                    if 'title' in item and 'name' not in item:
                        item['name'] = item['title']
                    elif 'name' in item and 'title' not in item:
                        item['title'] = item['name']
                    
                    # Validate with Pydantic
                    opp = OpportunitySchema(**item)
                    opportunities.append(opp)
                    
                    # TELEMETRY: Announce Match to Discovery Pulse
                    mission_id = f"extract_{opp.id[:8]}"
                    opp_label = opp.name[:40] + ("..." if len(opp.name) > 40 else "")
                    await discovery_pulse.announce_mission(
                        mission_id, 
                        f"✨ Match discovered: {opp_label} on {platform_hint}", 
                        "active"
                    )
                    
                except Exception as parse_error:
                    logger.warning(
                        "Failed to parse individual opportunity", 
                        error=str(parse_error),
                        item=str(item)[:100]
                    )
                    continue
            
            logger.info(
                "Cortex Reader: Agentic extraction loop complete",
                source=source_url[:50],
                extracted=len(opportunities),
                platform=platform_hint
            )
            
            return opportunities

        except json.JSONDecodeError as je:
            logger.error("Reader LLM JSON parse error", url=source_url, error=str(je))
            return []
        except Exception as e:
            logger.error("Gemma AI extraction failed", url=source_url, error=str(e))
            return []

    async def _call_ai_gateway(self, prompt: str) -> str:
        """
        Calls the unified IntelligenceGateway.
        This automatically routes to Gemma 4 via Intelligence Gateway.
        """
        return await intelligence_gateway.generate_content(prompt)

    def _detect_platform(self, url: str) -> str:
        """Detect platform for specialized parsing hints"""
        url_lower = url.lower()
        
        if 'devpost.com' in url_lower:
            return 'DevPost'
        elif 'dorahacks.io' in url_lower:
            return 'DoraHacks'
        elif 'mlh.io' in url_lower:
            return 'Major League Hacking (MLH)'
        elif 'hackquest' in url_lower:
            return 'HackQuest'
        elif 'angelhack' in url_lower:
            return 'AngelHack'
        elif 'devfolio' in url_lower:
            return 'Devfolio'
        elif 'kaggle.com' in url_lower:
            return 'Kaggle'
        elif 'gitcoin' in url_lower:
            return 'Gitcoin'
        elif 'immunefi' in url_lower:
            return 'Immunefi Bug Bounty'
        elif 'hackerone' in url_lower:
            return 'HackerOne Bug Bounty'
        elif 'bugcrowd' in url_lower:
            return 'Bugcrowd Bug Bounty'
        elif 'superteam' in url_lower or 'earn.superteam' in url_lower:
            return 'Superteam (Solana Ecosystem)'
        elif 'layer3' in url_lower:
            return 'Layer3 Web3 Quests'
        elif 'bold.org' in url_lower:
            return 'Bold.org Scholarships'
        elif 'scholarships.com' in url_lower:
            return 'Scholarships.com'
        elif 'fastweb' in url_lower:
            return 'Fastweb Scholarships'
        else:
            return 'General Opportunity Platform'

    def _normalize_url(self, url: str, base_url: str) -> str:
        """
        Normalize URLs to prevent duplicates and broken links.
        Especially handles DevPost, DoraHacks, etc.
        """
        if not url:
            return base_url
            
        try:
            # 1. Resolve relative URLs
            if not url.startswith(('http://', 'https://')):
                url = urljoin(base_url, url)
                
            # 2. Platform specialized normalization
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.rstrip('/')
            
            # DevPost Normalization: ALWAYS use canonical path format (devpost.com/hackathons/name)
            # Subdomain URLs (e.g., project.devpost.com) break after hackathons end!
            if 'devpost.com' in domain:
                # 1. Handle subdomains FIRST (e.g., gemini-3-hackathon.devpost.com → devpost.com/hackathons/gemini-3-hackathon)
                if domain != 'devpost.com' and domain.endswith('.devpost.com'):
                    # Extract project name from subdomain
                    project_name = domain.replace('.devpost.com', '')
                    if project_name and project_name not in ['www', 'api', 'help', 'blog', 'info']:
                        return f"https://devpost.com/hackathons/{project_name}/"
                
                # 2. If path is /hackathons/projectName, normalize it
                if path.startswith('/hackathons/'):
                    project_name = path.replace('/hackathons/', '').split('/')[0]
                    # Restore canonical path which is most compatible
                    if project_name and project_name not in ['hackathons', 'challenges', 'discover', '']:
                        return f"https://devpost.com/hackathons/{project_name}/"
                
                # 3. Default: keep as canonical path
                return f"https://devpost.com{path}/" if path else "https://devpost.com/"
            
            # DoraHacks Normalization
            if 'dorahacks.io' in domain:
                # Keep only the main path, strip track IDs etc.
                if path.startswith('/hackathon/'):
                    return f"https://dorahacks.io{path}"
            
            # Generic: Strip common tracking query params
            query_to_strip = ['ref', 'utm_source', 'utm_medium', 'utm_campaign', 'ref_feature', 'ref_medium']
            from urllib.parse import parse_qs, urlencode, urlunparse
            query_params = parse_qs(parsed.query)
            filtered_params = {k: v for k, v in query_params.items() if k.lower() not in query_to_strip}
            
            new_query = urlencode(filtered_params, doseq=True)
            return urlunparse(parsed._replace(query=new_query, fragment=''))
            
        except Exception as e:
            logger.warning("URL normalization failed", url=url, error=str(e))
            return url


reader_llm = ReaderLLM()
