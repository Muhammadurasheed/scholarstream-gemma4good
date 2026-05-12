import asyncio
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()
for var in ["SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"]:
    if var in os.environ: del os.environ[var]


async def test_extraction():
    from app.services.crawler_service import crawler_service
    from app.services.cortex.reader_llm import reader_llm
    
    url = "https://www.kaggle.com/competitions"
    print(f"1. Fetching raw HTML from {url}...")
    
    # We use fetch_content to get the fully hydrated SPA
    html = await crawler_service.fetch_content(url, max_retries=1)
    
    if not html:
        print("Failed to fetch HTML. Exiting.")
        return
        
    print(f"2. Fetch complete. Raw HTML length: {len(html)} bytes")
    
    print("3. Pruning DOM with BeautifulSoup...")
    cleaned_text = reader_llm._clean_html_to_text(html)
    print(f"4. DOM Pruned! Clean text length: {len(cleaned_text)} bytes")
    
    print("Preview of clean text:")
    print("-" * 50)
    print(cleaned_text[:1000])
    print("-" * 50)
    
    print("5. Sending to Gemma for extraction (max 5 items)...")
    opportunities = await reader_llm.parse_multiple(html, url, max_items=5)
    
    print(f"6. Extraction complete! Found {len(opportunities)} opportunities:")
    for opp in opportunities:
        print(f"  - {opp.name[:60]}")
        print(f"    Prize: {opp.amount_display}")
        print(f"    Tags: {opp.type_tags}")

if __name__ == "__main__":
    asyncio.run(test_extraction())
