import asyncio
import os
import sys

# Add app to path
sys.path.append(os.getcwd())

from app.services.gemma_service import gemma_service

async def test_gemma():
    print("Testing Gemma AIService with hardened auth...")
    try:
        # Simple prompt
        response = await gemma_service.generate_content_async("Hello Gemma, are you online?")
        print("\nSuccess!")
        print(f"Response: {response.get('choices', [{}])[0].get('message', {}).get('content', '')}")
    except Exception as e:
        print(f"\nFailed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemma())
