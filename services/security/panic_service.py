import logging
import asyncio
from datetime import datetime, timezone

# We'll need access to ARQ pool to kill jobs.
# In a real app, we might inject this or fetch from app state.

logger = logging.getLogger(__name__)

class PanicService:
    """
    Handles the "Nuclear Option":
    1. FREEZE: Stops all autonomous activity.
    2. EVACUATE: Sweeps assets to cold storage.
    3. DEAD MAN: Monitors operator heartbeat.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PanicService, cls).__new__(cls)
            cls._instance.is_panic_active = False
            cls._instance.evacuation_status = "IDLE"
            cls._instance.last_heartbeat = datetime.now(timezone.utc)
            cls._instance.heartbeat_timeout = 3600 # 1 hour default (seconds)
        return cls._instance

    async def trigger_panic(self, reason: str = "MANUAL_OVERRIDE", arq_pool = None) -> bool:
        """
        Initiates the Panic Protocol.
        """
        if self.is_panic_active:
            logger.warning("Panic Protocol already active.")
            return True

        self.is_panic_active = True
        logger.critical(f"🚨 PANIC PROTOCOL INITIATED: {reason} 🚨")
        
        # 1. Kill All Agents (ARQ)
        if arq_pool:
            # This logic depends on ARQ implementation details to list/cancel jobs
            # For MVP we assume a method exists or we clear the queue.
            # await arq_pool.control.cancel_all_jobs() # Hypothetical
            logger.info("Signal sent to Kill All Jobs.")
        
        # 2. Trigger Evacuation
        asyncio.create_task(self._evacuate_assets())
        
        return True

    async def _evacuate_assets(self):
        """
        Mock implementation of Cold-Haven Evacuation.
        """
        self.evacuation_status = "IN_PROGRESS"
        logger.info("Evacuation: Scanning wallets...")
        await asyncio.sleep(1) # Sim work
        logger.info("Evacuation: Calculated exposure: $1,250,540")
        await asyncio.sleep(1)
        logger.info("Evacuation: Sweeping to Cold Storage (0xabcd...1234)")
        self.evacuation_status = "COMPLETED"
        logger.info("Evacuation: COMPLETED. Assets Secured.")

    def reset_system(self, recovery_key: str) -> bool:
        if recovery_key != "admin_recovery_key_123": # Hardcoded for MVP
            logger.warning("Invalid Recovery Key provided.")
            return False
            
        self.is_panic_active = False
        self.evacuation_status = "IDLE"
        logger.info("System RESET. Panic Protocol deactivated.")
        return True

    def record_heartbeat(self):
        """Operator check-in."""
        self.last_heartbeat = datetime.now(timezone.utc)
        logger.debug("Heartbeat received.")

    def check_dead_man_switch(self) -> bool:
        """
        Checks if heartbeat has expired. Returns True if Panic triggered.
        """
        if self.is_panic_active: return False
        
        delta = (datetime.now(timezone.utc) - self.last_heartbeat).total_seconds()
        if delta > self.heartbeat_timeout:
            logger.error(f"Dead Man's Switch Triggered! No heartbeat for {delta}s")
            # In real async context, we'd await this. 
            # For sync check, we can't await easily without loop.
            # We assume this is called from a loop.
            return True
        return False

# Singleton
panic_service = PanicService()

def get_panic_service() -> PanicService:
    return panic_service
