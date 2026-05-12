"""Test the revived pipeline: Hunt Strategy + Tavily with domain constraints"""
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


async def test():
    from app.services.gemma_service import gemma_service
    from app.services.tavily_service import tavily_service
    
    profile = {
        "major": "Computer Science",
        "interests": ["Artificial Intelligence", "Web3", "Blockchain"],
        "country": "Nigeria",
        "academic_status": "Undergraduate"
    }
    
    print("=" * 60)
    print("  TEST: New Hunt Strategy (Opportunity-Focused)")
    print("=" * 60)
    strategy = await gemma_service.generate_hunt_strategy(profile)
    thought = strategy.get("thought", "N/A")
    print(f"Thought: {thought[:120]}")
    print(f"Platforms: {strategy.get('platforms', [])}")
    queries = strategy.get("search_queries", [])
    for i, q in enumerate(queries):
        print(f"  Query {i+1}: {q}")
    
    print()
    print("=" * 60)
    print("  TEST: Tavily Search with Domain Constraints")
    print("=" * 60)
    if queries:
        results = await tavily_service.search_opportunities(queries[0], max_results=5)
        print(f"Found {len(results)} results:")
        for r in results:
            title = r.get("title", "N/A")[:60]
            url = r.get("url", "N/A")[:80]
            has_content = bool(r.get("raw_content") or r.get("content"))
            print(f"  - {title}")
            print(f"    URL: {url}")
            print(f"    Has content: {has_content}")
    else:
        print("No queries generated!")
    
    print()
    print("=" * 60)
    print("  TEST: DNA-Resolved Platform URLs")
    print("=" * 60)
    from app.services.cortex.navigator import _resolve_platforms_for_profile
    urls = _resolve_platforms_for_profile(profile)
    print(f"Resolved {len(urls)} platform URLs for CS/AI/Web3/Blockchain student:")
    for url in urls:
        print(f"  - {url}")
    
    print()
    print("ALL TESTS COMPLETE")

if __name__ == "__main__":
    asyncio.run(test())
