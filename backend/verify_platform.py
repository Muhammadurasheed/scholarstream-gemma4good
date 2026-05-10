
import asyncio
import os
import sys

# Add current directory to path so it can find 'app'
sys.path.append(os.getcwd())

async def test_playwright():
    print("--- Testing Playwright ---")
    try:
        from playwright.async_api import async_playwright
        print("Playwright module imported")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://example.com")
            title = await page.title()
            print(f"Playwright working: {title}")
            await browser.close()
    except Exception as e:
        print(f"Playwright FAILED: {e}")

async def test_gemma():
    print("\n--- Testing Gemma ---")
    try:
        # Set credentials env var manually for test
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), "serviceAccountKey.json")
        
        from app.services.gemma_service import gemma_service
        print("Gemma Service imported")
        
        prompt = "Say hello in 3 words"
        response = await gemma_service.generate_content_async(prompt)
        print(f"Gemma Response: {response}")
    except Exception as e:
        print(f"Gemma FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_playwright())
    asyncio.run(test_gemma())
