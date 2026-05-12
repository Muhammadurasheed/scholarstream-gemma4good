import asyncio
import os
import sys
import certifi

# === NUCLEAR ENVIRONMENT SANITIZER ===
for var in ["SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"]:
    if var in os.environ:
        del os.environ[var]
# =====================================

# Add backend to path
sys.path.append(os.getcwd())

from app.services.gemma_service import gemma_service

async def test_gemma_final():
    print("Testing Gemma 4 Connectivity with SSL Hardening...")
    try:
        response = await gemma_service.generate_content_async("Hello! Are you online?", enable_thinking=False)
        print("Success! Gemma responded.")
        print(f"Response: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"FAILED! Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemma_final())
