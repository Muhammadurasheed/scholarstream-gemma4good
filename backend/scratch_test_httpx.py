
import httpx
import asyncio

async def test_httpx():
    print("Testing httpx call...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://www.google.com")
            print(f"Success! Status: {response.status_code}")
    except Exception as e:
        print(f"Failed with error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_httpx())
