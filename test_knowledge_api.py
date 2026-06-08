import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:7000"

async def test_knowledge_api():
    print("\n--- KNOWLEDGE DASHBOARD API QA ---")
    
    async with httpx.AsyncClient() as client:
        # 1. Test GET /api/knowledge/sources
        print("\n[1/2] Testing GET /api/knowledge/sources...")
        try:
            resp = await client.get(f"{BASE_URL}/api/knowledge/sources")
            if resp.status_code == 200:
                print(f"  ✓ Sources endpoint reachable. Response: {resp.json()}")
            else:
                print(f"  ✗ Sources endpoint FAILED: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"  ✗ Sources endpoint connection ERROR: {e}")

        # 2. Test POST /api/knowledge/ingest
        print("\n[2/2] Testing POST /api/knowledge/ingest...")
        try:
            payload = {
                "url_or_path": "https://www.youtube.com/watch?v=UngVdAsQEiU",
                "source_type": "youtube"
            }
            resp = await client.post(f"{BASE_URL}/api/knowledge/ingest", params=payload)
            if resp.status_code == 200:
                print(f"  ✓ Ingestion triggered successfully: {resp.json()}")
            else:
                print(f"  ✗ Ingestion endpoint FAILED: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"  ✗ Ingestion endpoint connection ERROR: {e}")

    print("\n--- QA COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_knowledge_api())
