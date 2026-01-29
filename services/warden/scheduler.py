"""
Warden Scheduler.
Runs the periodic health checks.
"""
import logging
import asyncio
from services.warden.routine_runner import WardenRoutine

logger = logging.getLogger(__name__)

class WardenScheduler:
    """Schedules Warden routines."""
    
    def __init__(self):
        self.runner = WardenRoutine()
        self.interval = 300 # seconds (5 mins)
        self.running = False
        
    async def start(self):
        self.running = True
        logger.info("WARDEN_SCHEDULER: Starting periodic health checks.")
        while self.running:
            try:
                self.runner.perform_health_check()
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"WARDEN_ERROR: {e}")
                await asyncio.sleep(60) # Failure backoff
                
    def stop(self):
        self.running = False
