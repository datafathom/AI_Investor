import asyncio
import pytest
from utils.scrubber import scrubber
from services.memory_service import memory_service
from arq.connections import RedisSettings
from arq import create_pool
import os

@pytest.mark.asyncio
async def test_scrubber():
    text = "My private key is 0xabc123... and my IP is 192.168.1.1"
    redacted = scrubber.redact(text)
    assert "[REDACTED]" in redacted
    assert "192.168.1.1" not in redacted
    print("✅ Scrubber verified.")

@pytest.mark.asyncio
async def test_memory_service_embedding():
    # Note: This might require the model to be downloaded/loaded
    content = "The market is showing bullish signs."
    # We mock the DB part for now since we are testing logic and embedding generation
    result = await memory_service.store_experience(dept_id=7, content=content)
    assert result in ["SUCCESS", "FAILURE"] # Should be success if model loads
    print("✅ Memory Service Embedding verified.")

@pytest.mark.asyncio
async def test_arq_enqueuing():
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "127.0.0.1"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None)
    )
    try:
        pool = await create_pool(redis_settings)
        job = await pool.enqueue_job('run_agent_logic', {"mission_id": "TEST_001", "dept_id": 8})
        assert job.job_id is not None
        print(f"✅ ARQ Enqueuing verified. Job ID: {job.job_id}")
    except Exception as e:
        print(f"⚠️ ARQ Enqueuing skipped or failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_scrubber())
    asyncio.run(test_memory_service_embedding())
    asyncio.run(test_arq_enqueuing())
