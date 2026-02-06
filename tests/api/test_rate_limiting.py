
import pytest
import httpx
import asyncio
from typing import List

@pytest.mark.async_timeout(30)
@pytest.mark.asyncio
async def test_rate_limiting_health_check():
    """
    Verifies that the rate limiter triggers after exceeding the configured limit.
    """
    url = "http://127.0.0.1:5050/health"
    limit = 5  # We'll use a low limit for testing if possible, or just spam
    
    # We expect this test to be run against a live server or 
    # we use TestClient if the server is in-process. 
    # Since we want to verify the REDIS integration, a real request is better.
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # First check
        try:
            response = await client.get(url)
            if response.status_code != 200:
                print(f"FAILED: Status={response.status_code}, Body={response.text}")
            assert response.status_code == 200
        except Exception as e:
            print(f"ERROR: {e}")
            raise
        
        # Rapid fire requests
        tasks = [client.get(url) for _ in range(20)]
        results = await asyncio.gather(*tasks)
        
        status_codes = [r.status_code for r in results]
        
        # At least one should be 429 Too Many Requests if the limit is < 20
        assert 429 in status_codes
        print(f"Rate limit verification success. Received 429 on {status_codes.count(429)}/{len(status_codes)} requests.")

if __name__ == "__main__":
    # Internal runner for quick verification
    asyncio.run(test_rate_limiting_health_check())
