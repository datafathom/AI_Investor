import pytest
import time
from arq import create_pool
from arq.connections import RedisSettings
import os

@pytest.mark.asyncio
async def test_queue_submission_latency():
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "127.0.0.1"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", "84zMsasS0WfXGGVFU6t7vLd9")
    )
    
    start_time = time.time()
    try:
        pool = await create_pool(redis_settings)
        # Mock mission data
        mission_data = {"mission_id": "latency_test", "dept_id": 1}
        job = await pool.enqueue_job('run_agent_logic', mission_data)
        latency = (time.time() - start_time) * 1000 # ms
        
        assert job.job_id is not None
        assert latency < 100, f"Queue submission too slow: {latency}ms"
        print(f"Queue Latency: {latency:.2f}ms")
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis or enqueue job: {e}")
