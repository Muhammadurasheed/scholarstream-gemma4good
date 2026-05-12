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


async def test_pipeline():
    from app.services.crawler_service import crawler_service
    from app.services.cortex.reader_llm import reader_llm
    
    url = "https://mlh.io/seasons/2026/events"
    print(f"1. Testing full crawler stabilization on {url}")
    
    # Use fetch_content but WITHOUT the harsh route blocking that broke Nuxt apps
    # We will just fetch without route blocking for the test
    context = await crawler_service.create_stealth_context()
    page = await context.new_page()
    await page.goto(url, wait_until="networkidle", timeout=60000)
    
    # Use our new DOM stabilization logic directly here to test it
    previous_size = 0
    stable_count = 0
    print("Waiting for DOM stabilization...")
    for _ in range(10): 
        await asyncio.sleep(1.5)
        current_size = len(await page.content())
        print(f"Current DOM size: {current_size}")
        if current_size > 5000 and abs(current_size - previous_size) < 100:
            stable_count += 1
            if stable_count >= 2:
                print("DOM Stabilized!")
                break
        else:
            stable_count = 0
        previous_size = current_size
        
    html = await page.content()
    await context.close()
    
    print(f"2. Raw HTML length: {len(html)}")
    
    print("3. Pruning with BeautifulSoup...")
    cleaned = reader_llm._clean_html_to_text(html)
    print(f"Clean text length: {len(cleaned)}")
    print("Preview:")
    print("-" * 50)
    print(cleaned[:1000])
    print("-" * 50)
    
    print("4. Testing Gemma Iron Gate Prompt...")
    opportunities = await reader_llm.parse_multiple(html, url, max_items=3)
    print(f"Found {len(opportunities)} opportunities:")
    for opp in opportunities:
        print(f"  - {opp.name[:60]}")
        print(f"    Prize: {opp.amount_display} | Tags: {opp.type_tags}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
