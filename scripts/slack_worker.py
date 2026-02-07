import os
import asyncio
import json
import logging
import time
import re
import datetime
from pathlib import Path
from services.notifications.slack_service import get_slack_service
from dotenv import load_dotenv

load_dotenv()

# Configure logging to see worker activity clearly
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | 👷 WORKER | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

BRIDGE_FILE = ".slack_kafka_bridge.jsonl"
HEARTBEAT_FILE = ".slack_worker_alive"

def update_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "w") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        logger.error(f"Failed to update heartbeat: {e}")

# Global lock to ensure only one queue-processing loop runs at a time
processing_lock = asyncio.Lock()

async def process_job(service, payload):
    """
    Simulates the actual execution of a background task.
    """
    trigger_job_id = payload.get("job_id")
    command = payload.get("command", "")
    channel = payload.get("channel")

    if "test add" in command:
        logger.info(f"ACK: Received 'test add' for {trigger_job_id}. Job remains Queued.")
        return
    
    elif "test start" in command:
        if processing_lock.locked():
            logger.warning(f"⚠️ Trigger ignored: Queue processing already in progress (Triggered by {trigger_job_id}).")
            return

        async with processing_lock:
            logger.info(f"🚀 STARTING QUEUE PROCESSING (Triggered by {trigger_job_id})")
            update_heartbeat()
            
            # Immediate ACK for the start command itself
            await service.send_notification(
                text=f"⚙️ **Worker Switch ON:** Starting sequential processing of the job queue...",
                level="success",
                channel=channel,
                job_id=trigger_job_id
            )

            while True:
                update_heartbeat()
                # 1. Reload the queue to find the next Queued job
                active_jobs = service._load_active_jobs()
                queued_jobs = [jid for jid, info in active_jobs.items() if info.get("status") == "Queued"]
                
                if not queued_jobs:
                    logger.info("✨ Queue processing complete. No more Queued items.")
                    await service.send_notification(
                        text="🏁 **Queue Processed:** All pending jobs are now complete.",
                        level="success",
                        channel=channel
                    )
                    break

                # 2. Pick the first one in line
                target_jid = queued_jobs[0]
                logger.info(f"⏳ Processing Job {target_jid}...")

                # 3. Update status to Started and Notify
                active_jobs[target_jid]["status"] = "Started"
                service._active_jobs = active_jobs
                service._save_active_jobs()

                await service.send_notification(
                    text=f"⏳ **Started:** Processing job `{target_jid}`... (8s timer)",
                    level="info",
                    channel=channel
                )

                # 4. STRICTLY WAIT before marking as completed
                await asyncio.sleep(8)

                # 5. Update status to Completed and Notify
                active_jobs = service._load_active_jobs()
                if target_jid in active_jobs:
                    active_jobs[target_jid]["status"] = "Completed"
                    service._active_jobs = active_jobs
                    service._save_active_jobs()

                await service.send_notification(
                    text=f"✅ **Completed:** Job `{target_jid}` finished successfully.",
                    level="success",
                    channel=channel
                )
                
                # Brief pause before next job to ensure sequential clarity
                await asyncio.sleep(1)
    
    else:
        logger.warning(f"Unknown command received: {command}")

async def main():
    logger.info("🚀 Standalone Slack Worker Starting... (Polling file-based bridge)")
    update_heartbeat()
    
    try:
        service = get_slack_service(mock=False)
    except Exception as e:
        logger.error(f"🔥 Critical Error: Could not initialize SlackService: {e}")
        return
    
    if not os.path.exists(BRIDGE_FILE):
        Path(BRIDGE_FILE).touch()

    while True:
        try:
            update_heartbeat()
            # Check for new jobs in the bridge
            with open(BRIDGE_FILE, "r+") as f:
                lines = f.readlines()
                if lines:
                    # Clear the file so we don't double process
                    f.truncate(0)
                    f.seek(0)
                    
                    for line in lines:
                        if not line.strip():
                            continue
                        logger.info(f"📥 New Job Detected: {line.strip()}")
                        payload = json.loads(line)
                        
                        # Process each job in the background (asynchronous)
                        asyncio.create_task(process_job(service, payload))

            # Poll every second
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Worker Loop Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user.")
    except Exception as e:
        logger.critical(f"FATAL: Worker crashed with error: {e}")
