import asyncio
import os
import sys

sys.path.append(os.getcwd())

from app.services.personalization_engine import PersonalizationEngine

async def test_engine():
    engine = PersonalizationEngine()
    
    opportunity = {
        "name": "Tech Hackathon",
        "description": "A hackathon for CS students.",
        "tags": ["tech", "coding"]
    }
    
    user_profile = {
        "major": "Computer Science",
        "interests": ["coding", "AI"],
        "background": ["student"]
    }
    
    print("Testing semantic score...")
    try:
        score = await engine.calculate_semantic_score(opportunity, user_profile)
        print("Success! Score:", score)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_engine())
