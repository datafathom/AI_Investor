import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    """
    Prevents cascading failures by stopping execution after N failures.
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 60, name: str = "default"):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED" # CLOSED (Normal), OPEN (Tripped), HALF-OPEN (Testing)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    logger.info(f"Circuit {self.name} HALF-OPEN. Retrying...")
                    self.state = "HALF-OPEN"
                else:
                    msg = f"Circuit {self.name} is OPEN. Call blocked."
                    logger.warning(msg)
                    raise CircuitBreakerOpenException(msg)

            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    logger.info(f"Circuit {self.name} RECOVERED. Closing.")
                    self.reset()
                return result
            except Exception as e:
                self.record_failure()
                raise e

        return wrapper

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        logger.error(f"Circuit {self.name} recorded failure ({self.failures}/{self.failure_threshold})")
        
        if self.failures >= self.failure_threshold:
            self.trip()

    def trip(self):
        self.state = "OPEN"
        logger.critical(f"🚨 Circuit {self.name} TRIPPED! Blocking calls for {self.recovery_timeout}s.")

    def reset(self):
        self.failures = 0
        self.state = "CLOSED"
