import asyncio
import os
import sys

sys.path.append(os.getcwd())

from app.services.gemma_service import gemma_service

async def test_gemma_call():
    print("Testing Gemma call to reproduce Errno 2...")
    try:
        prompt = f"User is a Computer Science student. Opportunity is 'Hackathon'. Is this highly relevant for them? Answer YES/NO only."
        judgment = await gemma_service.generate_content_async(prompt, enable_thinking=False)
        print("Success:", judgment)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemma_call())
