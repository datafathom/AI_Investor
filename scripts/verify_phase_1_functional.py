import asyncio
import os
import logging
from dotenv import load_dotenv
from services.memory_service import memory_service
from arq import create_pool
from arq.connections import RedisSettings

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_phase_1_functional():
    load_dotenv()
    
    # 1. Test Memory Service (Storage & Recall)
    logger.info("--- Testing Memory Service ---")
    dept_id = 99  # Test Dept
    mission_id = "VERIFY_PHASE_1_E2E"
    content = "This is a secret test for Phase 1: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    
    logger.info(f"Storing experience (with PII)...")
    status = await memory_service.store_experience(dept_id, content, mission_id)
    print(f"Store Status: {status}")
    
    if status == "SUCCESS":
        logger.info("Recalling memories...")
        results = await memory_service.recall_memories("secret test", limit=1)
        if results:
            print(f"Recall Result: {results[0]['content']}")
            if "[REDACTED]" in results[0]['content']:
                print("✅ REDACTION SUCCESSFUL")
            else:
                print("❌ REDACTION FAILED")
        else:
            print("❌ RECALL FAILED (No results)")

    # 2. Test ARQ Enqueue
    logger.info("\n--- Testing ARQ Enqueue ---")
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "127.0.0.1"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None)
    )
    
    try:
        redis = await create_pool(redis_settings)
        job = await redis.enqueue_job('run_agent_logic', {"mission_id": "TEST_JOB", "dept_id": 1})
        print(f"Job Enqueued: {job.job_id}")
        
        # Wait for worker results (requires worker to be running)
        print("Checking job status (waiting 2s)...")
        await asyncio.sleep(2)
        info = await job.info()
        print(f"Job Info: {info}")
        
    except Exception as e:
        print(f"ARQ Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_phase_1_functional())
