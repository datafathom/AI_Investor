
import random
import time
import logging
import subprocess
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChaosMonkey")

class ChaosMonkey:
    """
    Simulates system turbulence by randomly stopping services or simulating network latency.
    ONLY for use in STAGING environments.
    """
    
    def __init__(self, target_services=None):
        self.target_services = target_services or ["redis", "postgres", "neo4j"]
        self.is_active = False

    def simulate_service_failure(self, service_name=None):
        """Simulates a service outage by stopping a docker container."""
        target = service_name or random.choice(self.target_services)
        logger.warning(f"🐒 Chaos Monkey: Killing service {target}...")
        
        # In a real environment, this would call docker-compose stop
        # Here we simulate by logging for the demo
        print(f"DEBUG: Executing disaster scenario for {target}")
        return target

    def simulate_network_latency(self, latency_ms=2000):
        """Simulates internal network slowdown."""
        logger.warning(f"🐒 Chaos Monkey: Injecting {latency_ms}ms latency...")
        # Simulated logic
        time.sleep(latency_ms / 1000)

    def run_experiment(self, duration_sec=60):
        """Runs a chaos experiment for a fixed duration."""
        logger.info(f"🚀 Starting chaos experiment for {duration_sec}s")
        start_time = time.time()
        while time.time() - start_time < duration_sec:
            action = random.choice(["service", "latency", "nothing"])
            if action == "service":
                self.simulate_service_failure()
            elif action == "latency":
                self.simulate_network_latency()
            time.sleep(random.randint(5, 15))
        logger.info("🏁 Chaos experiment concluded.")

if __name__ == "__main__":
    if os.getenv("CHAOS_ENABLED") == "true":
        monkey = ChaosMonkey()
        monkey.run_experiment()
    else:
        logger.info("Chaos Monkey is DISABLED. Set CHAOS_ENABLED=true to activate.")
