"""
Gemma Enrichment Service — Hackathon Native V3
Strictly uses Gemma 4 via Vertex AI MaaS for high-speed financial discovery.
Gemini has been completely purged to ensure zero-dependency on legacy models.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import asyncio
import structlog
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from app.config import settings
from app.services.gemma_service import gemma_service
from app.utils.json_utils import robust_json_loads

logger = structlog.get_logger()

class AIEnrichmentService:
    """
    Enriches raw opportunity data using Gemma 4.
    Purged of Gemini to comply with Gemma 4 Good hackathon standards.
    """
    
    def __init__(self):
        logger.info("⚡ GEMMA ENRICHMENT SERVICE ACTIVE")
    
    def clean_html(self, html_content: str) -> str:
        """Aggressively clean HTML to reduce token usage"""
        if not html_content: return ""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for tag in soup(['style', 'svg', 'path', 'noscript', 'meta', 'link', 'iframe', 'footer', 'nav']):
                tag.decompose()

            # Preserve hydration scripts for SPAs (Next.js, etc.)
            for script in soup.find_all('script'):
                sid = (script.get('id') or '').strip()
                stype = (script.get('type') or '').strip().lower()
                keep = sid == '__NEXT_DATA__' or stype in ['application/ld+json', 'application/json']
                if not keep: script.decompose()

            body = soup.body
            return str(body)[:60000] if body else str(soup)[:60000]
        except Exception as e:
            logger.warning("HTML Clean failed", error=str(e))
            return html_content[:60000]

    async def extract_opportunities_from_html_batch(self, items: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Batch process multiple HTML pages via Gemma 4."""
        if not items: return []
            
        cleaned_items = []
        for item in items:
            clean = self.clean_html(item.get('html', ''))
            if len(clean) > 50:
                cleaned_items.append({'url': item.get('url'), 'content': clean})
        
        if not cleaned_items: return []

        context_str = ""
        for i, item in enumerate(cleaned_items):
            context_str += f"\n\n[PAGE {i+1} URL: {item['url']}]\n{item['content']}\n"

        prompt = f"""You are a high-speed discovery engine powered by Gemma 4.
Extract EVERY distinct opportunity (Scholarship, Grant, Hackathon, Bounty) from the provided content.
Combined JSON list: title, organization, amount (float), deadline (YYYY-MM-DD), description, url (absolute), type, eligibility.

DATA:
{context_str}

RETURN JSON ARRAY ONLY."""

        try:
            logger.info("Gemma Discovery Mission started", pages=len(cleaned_items))
            response_json = await gemma_service.generate_content_async(prompt)
            content = response_json["choices"][0]["message"]["content"]
            
            # Use safe parsing
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            extracted = robust_json_loads(content)
            if not isinstance(extracted, list): extracted = [extracted] if isinstance(extracted, dict) else []
            
            valid_opportunities = []
            for item in extracted:
                if not item.get('title') or not item.get('url'): continue
                item['amount'] = float(item.get('amount', 0))
                valid_opportunities.append(item)

            logger.info("Gemma extraction complete", found=len(valid_opportunities))
            return valid_opportunities

        except Exception as e:
            logger.error("Gemma Enrichment failed", error=str(e))
            return []

    async def enrich_opportunities_batch(self, raw_opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return raw_opportunities # Placeholder for now

    async def extract_opportunities_from_html(self, html_content: str, url: str) -> List[Dict[str, Any]]:
        return await self.extract_opportunities_from_html_batch([{'url': url, 'html': html_content}])

# Global instance
ai_enrichment_service = AIEnrichmentService()
