import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.getcwd())

from app.services.tavily_service import tavily_service

async def test_tavily():
    print("Testing Tavily Search Service...")
    query = "computer science scholarships for nigerian students 2026"
    results = await tavily_service.search_opportunities(query, max_results=3)
    
    if results:
        print(f"Success! Found {len(results)} results.")
        for i, res in enumerate(results):
            print(f"Result {i+1}: {res.get('title')} ({res.get('url')})")
            content = res.get('content', '')
            print(f"Snippet: {content[:100]}...")
    else:
        print("Failed! No results found. Check your API key.")

if __name__ == "__main__":
    asyncio.run(test_tavily())
