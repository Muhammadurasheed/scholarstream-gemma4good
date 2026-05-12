"""
ScholarStream Gemma 4 End-to-End Connectivity Test
Tests every layer of the AI pipeline to identify exactly where failures occur.

Run: python test_gemma_live.py
"""
import asyncio
import os
import sys
import json
import time
import io

# Fix Windows cp1252 encoding crash
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

# Sanitize SSL vars (same as main.py)
for var in ["SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"]:
    if var in os.environ:
        del os.environ[var]


async def test_1_service_account():
    """Test 1: Does the service account key file exist and is it valid?"""
    print("\n" + "="*60)
    print("TEST 1: Service Account Key File")
    print("="*60)
    
    sa_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    
    if not os.path.exists(sa_path):
        print(f"❌ FAIL: serviceAccountKey.json NOT FOUND at {sa_path}")
        print("   FIX: Place your GCP service account key file here.")
        return False
    
    try:
        with open(sa_path, 'r') as f:
            sa_data = json.load(f)
        
        project_id = sa_data.get('project_id', 'MISSING')
        client_email = sa_data.get('client_email', 'MISSING')
        has_private_key = bool(sa_data.get('private_key'))
        
        print(f"✅ File exists: {sa_path}")
        print(f"   Project ID: {project_id}")
        print(f"   Client Email: {client_email}")
        print(f"   Has Private Key: {has_private_key}")
        
        if not has_private_key:
            print("❌ FAIL: Private key is missing from service account JSON")
            return False
            
        return True
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON in service account file: {e}")
        return False


async def test_2_google_auth():
    """Test 2: Can we get a valid OAuth2 Bearer token?"""
    print("\n" + "="*60)
    print("TEST 2: Google Auth - OAuth2 Bearer Token")
    print("="*60)
    
    try:
        from app.services.gemma_service import gemma_service
        
        print(f"   Endpoint: {gemma_service.endpoint}")
        print(f"   Model: {gemma_service.model_id}")
        print(f"   Project: {gemma_service.project_id}")
        print(f"   Creds type: {type(gemma_service.creds).__name__}")
        
        if gemma_service.creds is None:
            print("❌ FAIL: Credentials object is None")
            return False
        
        # Try refreshing token
        token = await gemma_service.get_access_token()
        
        if token:
            print(f"✅ Bearer token obtained: {token[:20]}...{token[-10:]}")
            print(f"   Token length: {len(token)} chars")
            return True
        else:
            print("❌ FAIL: Token is empty")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Auth error: {e}")
        return False


async def test_3_gemma_simple_prompt():
    """Test 3: Can Gemma respond to a simple prompt?"""
    print("\n" + "="*60)
    print("TEST 3: Gemma 4 Simple Prompt (Hello World)")
    print("="*60)
    
    try:
        from app.services.gemma_service import gemma_service
        
        start = time.time()
        response = await gemma_service.generate_content_async(
            prompt="Say hello in one sentence. Just respond with the greeting.",
            enable_thinking=False
        )
        elapsed = time.time() - start
        
        if not response:
            print("❌ FAIL: Empty response from Gemma")
            return False
        
        if "choices" not in response:
            print(f"❌ FAIL: No 'choices' in response. Keys: {list(response.keys())}")
            print(f"   Full response: {json.dumps(response, indent=2)[:500]}")
            return False
        
        content = response["choices"][0]["message"]["content"]
        print(f"✅ Gemma responded in {elapsed:.1f}s:")
        print(f"   \"{content[:200]}\"")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def test_4_gemma_json_extraction():
    """Test 4: Can Gemma extract JSON (the core of our pipeline)?"""
    print("\n" + "="*60)
    print("TEST 4: Gemma 4 JSON Extraction (Pipeline Core)")
    print("="*60)
    
    try:
        from app.services.gemma_service import gemma_service
        
        prompt = """
        Extract opportunity data from this text:
        
        "Google Summer of Code 2026 is now open! Apply by April 2026. 
        Google pays students $3000-$6600 to work on open source projects. 
        Open to university students worldwide."
        
        Return JSON only:
        [{"title": "...", "organization": "...", "amount": 0, "deadline": "...", "geo_tags": ["..."], "type_tags": ["..."], "description": "..."}]
        """
        
        start = time.time()
        response = await gemma_service.generate_content_async(
            prompt=prompt,
            system_instruction="You are a data extraction specialist. Return only valid JSON arrays.",
            enable_thinking=False
        )
        elapsed = time.time() - start
        
        content = response["choices"][0]["message"]["content"]
        print(f"   Raw response ({elapsed:.1f}s): {content[:300]}")
        
        # Try parsing
        parsed = gemma_service._parse_json_safe(content)
        if parsed:
            print(f"✅ JSON parsed successfully:")
            if isinstance(parsed, list):
                for item in parsed:
                    print(f"   - {item.get('title', 'N/A')} | ${item.get('amount', 0)} | {item.get('geo_tags', [])}")
            elif isinstance(parsed, dict):
                print(f"   - {parsed.get('title', 'N/A')} | ${parsed.get('amount', 0)}")
            return True
        else:
            print("❌ FAIL: Could not parse JSON from response")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def test_5_gemma_hunt_strategy():
    """Test 5: Can Gemma generate a hunt strategy from user DNA?"""
    print("\n" + "="*60)
    print("TEST 5: Gemma Hunt Strategy (Agentic Core)")
    print("="*60)
    
    try:
        from app.services.gemma_service import gemma_service
        
        profile = {
            "major": "Computer Science",
            "interests": ["Artificial Intelligence", "Web3", "Blockchain"],
            "country": "Nigeria"
        }
        
        start = time.time()
        strategy = await gemma_service.generate_hunt_strategy(profile)
        elapsed = time.time() - start
        
        if strategy:
            print(f"✅ Strategy generated in {elapsed:.1f}s:")
            print(f"   Thought: {strategy.get('thought', 'N/A')}")
            print(f"   Platforms: {strategy.get('platforms', [])}")
            print(f"   Queries: {strategy.get('search_queries', [])}")
            return True
        else:
            print("❌ FAIL: Empty strategy returned")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def test_6_tavily_search():
    """Test 6: Is Tavily working with relevant results?"""
    print("\n" + "="*60)
    print("TEST 6: Tavily AI Search")
    print("="*60)
    
    try:
        from app.services.tavily_service import tavily_service
        
        if not tavily_service.api_key:
            print("❌ FAIL: TAVILY_API_KEY not set")
            return False
        
        start = time.time()
        results = await tavily_service.search_opportunities(
            "Computer Science scholarships for Nigerian students 2026 apply now",
            max_results=5
        )
        elapsed = time.time() - start
        
        if results:
            print(f"✅ Tavily returned {len(results)} results in {elapsed:.1f}s:")
            for r in results[:3]:
                print(f"   - {r.get('title', 'N/A')[:60]}")
                print(f"     URL: {r.get('url', 'N/A')[:80]}")
                has_content = bool(r.get('raw_content') or r.get('content'))
                print(f"     Has content: {has_content}")
            return True
        else:
            print("❌ FAIL: No results from Tavily")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def test_7_intelligence_gateway():
    """Test 7: Does the Intelligence Gateway correctly route to Gemma?"""
    print("\n" + "="*60)
    print("TEST 7: Intelligence Gateway (Unified AI Entry Point)")
    print("="*60)
    
    try:
        from app.services.intelligence_gateway import intelligence_gateway
        
        start = time.time()
        result = await intelligence_gateway.generate_content(
            "What is 2+2? Answer with just the number."
        )
        elapsed = time.time() - start
        
        if result:
            print(f"✅ Gateway responded in {elapsed:.1f}s: \"{result[:100]}\"")
            return True
        else:
            print("❌ FAIL: Empty response from gateway")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def test_8_firebase():
    """Test 8: Can we connect to Firestore?"""
    print("\n" + "="*60)
    print("TEST 8: Firebase/Firestore Connection")
    print("="*60)
    
    try:
        from app.database import db
        
        # Fetch demo guest profile
        profile = await db.get_user_profile("demo_guest_user")
        
        if profile:
            print(f"✅ Firestore connected. Demo guest profile loaded:")
            p = profile.get('profile', {})
            print(f"   Name: {p.get('name')}")
            print(f"   Major: {p.get('major')}")
            print(f"   Interests: {p.get('interests', [])}")
            return True
        else:
            print("❌ FAIL: Could not load demo guest profile")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")
        return False


async def main():
    print("="*60)
    print("  ScholarStream: Gemma 4 E2E Diagnostics Suite")
    print("  Testing every layer of the AI pipeline")
    print("="*60)
    
    results = {}
    
    tests = [
        ("Service Account Key", test_1_service_account),
        ("Google Auth Token", test_2_google_auth),
        ("Gemma Simple Prompt", test_3_gemma_simple_prompt),
        ("Gemma JSON Extraction", test_4_gemma_json_extraction),
        ("Gemma Hunt Strategy", test_5_gemma_hunt_strategy),
        ("Tavily Search", test_6_tavily_search),
        ("Intelligence Gateway", test_7_intelligence_gateway),
        ("Firebase/Firestore", test_8_firebase),
    ]
    
    for name, test_fn in tests:
        try:
            result = await test_fn()
            results[name] = result
        except Exception as e:
            print(f"❌ CRASH in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("  DIAGNOSTIC SUMMARY")
    print("="*60)
    
    all_pass = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} — {name}")
        if not passed:
            all_pass = False
    
    print()
    if all_pass:
        print("🎉 ALL SYSTEMS OPERATIONAL — Pipeline is ready!")
    else:
        print("⚠️  CRITICAL FAILURES DETECTED — Fix the above before proceeding.")
    
    print()


if __name__ == "__main__":
    asyncio.run(main())
