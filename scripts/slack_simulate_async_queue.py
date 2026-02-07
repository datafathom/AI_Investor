import os
import asyncio
import random
import time
from services.notifications.slack_service import get_slack_service
from dotenv import load_dotenv

load_dotenv()

async def simulate_job(service, job_id, delay):
    """Simulates a single job processing with Slack notifications."""
    # 1. Processing Start
    service.register_job(
        job_id=job_id,
        user_id="U-STRESS-TEST",
        command=f"stress-test --id {job_id}"
    )
    
    print(f"[{job_id}] ⏳ Starting with {delay}s delay...")
    await service.send_notification(
        text=f"⏳ **Processing:** Job `{job_id}` (Estimated: {delay}s)",
        level="info"
    )

    # 2. Simulate Work
    await asyncio.sleep(delay)

    # 3. Completion (Passing job_id to clear it)
    print(f"[{job_id}] ✅ Completed after {delay}s")
    await service.send_notification(
        text=f"✅ **Completed:** Job `{job_id}` (Actual: {delay}s)",
        level="success",
        job_id=job_id
    )

async def main():
    service = get_slack_service(mock=False)
    
    # We want 10 jobs with cascading delays: 20s - index
    delays = [20 - i for i in range(10)]
    
    print("🚀 Triggering 10 ASYNC JOBS with LIVE TRACKING (!queue enabled)...")
    
    # Initial "Queue" Message
    queue_msg = "📂 **Current Job Queue:**\n"
    for i in range(10):
        queue_msg += f"- Job `JB-{i:03}` (Queued)\n"
    
    await service.send_notification(text=queue_msg, level="info")
    
    # Start all jobs concurrently
    tasks = []
    for i, delay in enumerate(delays):
        job_id = f"JB-{i:03}"
        tasks.append(simulate_job(service, job_id, delay))
    
    # Wait for all to finish
    await asyncio.gather(*tasks)
    
    # Final cleanup
    await service.close()
    print("\n🏁 All simulator jobs processed. Check Slack!")

if __name__ == "__main__":
    asyncio.run(main())
