import asyncio
import os
import sys

# Add app to path
sys.path.append(os.getcwd())

from app.services.scrapers.hackathons.devpost_api_scraper import scrape_devpost_api

async def test_devpost():
    print("Testing DevPost API Scraper...")
    try:
        results = await scrape_devpost_api(max_pages=1)
        print(f"\nSuccess! Found {len(results)} hackathons.")
        for s in results[:3]:
            print(f"  - {s.name}")
    except Exception as e:
        print(f"\nFailed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_devpost())
