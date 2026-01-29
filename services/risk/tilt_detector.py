"""
Tilt Detector Service.
Monitors system telemetry for signs of emotional instability or "Tilt".
Triggers locks if specific aggressive patterns are detected.
"""
import logging
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TiltDetector:
    """
    Analyzes user interaction frequency and patterns.
    """

    def __init__(self):
        self.failed_attempts: List[float] = [] # timestamps

    def record_attempt(self) -> bool:
        """
        Record a failed or blocked attempt (e.g., clicking 'Buy' while locked).
        :return: True if TILT detected.
        """
        now = time.time()
        self.failed_attempts.append(now)

        # Cleanup attempts older than 1 minute
        self.failed_attempts = [t for t in self.failed_attempts if now - t < 60]

        # Criteria: 10 attempts in 60 seconds is "Tilting"
        if len(self.failed_attempts) >= 10:
            logger.critical("TILT_DETECTED: High frequency of aggressive interaction found.")
            return True

        return False

    def reset(self):
        self.failed_attempts = []
