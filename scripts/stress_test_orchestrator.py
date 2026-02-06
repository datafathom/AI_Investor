"""
==============================================================================
FILE: scripts/stress_test_orchestrator.py
ROLE: Performance & Stress Testing Utility
PURPOSE: Simulates high concurrent load on the Agent Orchestration Service.
         Validates concurrency limits (semaphore) and system stability.

USAGE:
    python scripts/stress_test_orchestrator.py --concurrency 50 --total 100
==============================================================================
"""
import asyncio
import aiohttp
import time
import argparse
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StressTester")

BASE_URL = "http://localhost:5050"

async def invoke_agent(session: aiohttp.ClientSession, agent_id: str, task: str) -> dict:
    """Send a single agent invocation request."""
    url = f"{BASE_URL}/api/departments/1/agents/{agent_id}/invoke"
    payload = {"task": task, "context": {"stress_test": True}}
    
    start_time = time.time()
    try:
        async with session.post(url, json=payload, timeout=30) as response:
            status = response.status
            data = await response.json()
            duration = time.time() - start_time
            return {
                "status": status,
                "duration": duration,
                "success": status == 200 and "error" not in data,
                "error": data.get("error") if status != 200 else None
            }
    except Exception as e:
        return {
            "status": 500,
            "duration": time.time() - start_time,
            "success": False,
            "error": str(e)
        }

async def run_stress_test(concurrency: int, total_requests: int):
    """Run the stress test with controlled concurrency."""
    logger.info(f"🚀 Starting Stress Test: Concurrency={concurrency}, Total Requests={total_requests}")
    
    # Use a semaphore to limit concurrent requests from the client side
    # to match the desired concurrency
    semaphore = asyncio.Semaphore(concurrency)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        async def wrapped_invoke():
            async with semaphore:
                # We use a random agent from a few known ones
                agents = ["orchestrator_agent", "architect_agent", "trader_agent"]
                import random
                agent = random.choice(agents)
                return await invoke_agent(session, agent, "Benchmarking system performance under load.")

        for _ in range(total_requests):
            tasks.append(wrapped_invoke())
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_time
        
        # Analyze results
        successes = [r for r in results if r["success"]]
        failures = [r for r in results if not r["success"]]
        durations = [r["duration"] for r in results]
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        rps = total_requests / total_duration if total_duration > 0 else 0
        
        logger.info("="*50)
        logger.info("STRESS TEST RESULTS")
        logger.info("="*50)
        logger.info(f"Total Requests: {total_requests}")
        logger.info(f"Successes: {len(successes)}")
        logger.info(f"Failures: {len(failures)}")
        logger.info(f"Total Duration: {total_duration:.2f}s")
        logger.info(f"Average Latency: {avg_duration:.2f}s")
        logger.info(f"Requests Per Second: {rps:.2f}")
        logger.info("="*50)
        
        if failures:
            logger.warning(f"First 5 failure reasons: {[f['error'] for f in failures[:5]]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Investor Stress Tester")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("--total", type=int, default=20, help="Total number of requests")
    args = parser.parse_args()
    
    asyncio.run(run_stress_test(args.concurrency, args.total))
