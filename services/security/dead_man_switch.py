import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeadManSwitchService:
    """
    Phase 206.4: Digital Inheritance & Dead Man's Switch.
    Monitors user activity. Triggers asset release protocols if inactivity exceeds threshold.
    """

    def __init__(self):
        self.last_checkin = datetime.now()
        self.timeout_days = 30
        self.status = "ARMED"
        self.beneficiaries = ["trustee@family-office.com", "heir@protonmail.com"]

    def check_in(self):
        """
        Resets the timer.
        """
        self.last_checkin = datetime.now()
        logger.info("Dead Man Switch: Check-in received. Timer reset.")
        return {"status": "ARMED", "days_remaining": self.timeout_days}

    def verify_status(self) -> Dict[str, Any]:
        """
        Checks if the switch should trigger.
        """
        delta = datetime.now() - self.last_checkin
        if delta.days > self.timeout_days:
            self.trigger_release()
            return {"status": "TRIGGERED", "triggered_at": datetime.now().isoformat()}
            
        return {
            "status": "ARMED",
            "last_checkin": self.last_checkin.isoformat(),
            "days_until_trigger": self.timeout_days - delta.days
        }

    def trigger_release(self):
        """
        Executes the release protocol.
        """
        if self.status != "TRIGGERED":
            logger.critical("🚨 DEAD MAN SWITCH TRIGGERED 🚨")
            logger.critical(f"Releasing keys to beneficiaries: {self.beneficiaries}")
            self.status = "TRIGGERED"
            # Logic to email crypto keys / shards would go here
