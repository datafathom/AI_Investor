import logging
import asyncio
import random
from agents.base_agent import BaseAgent, AgentState
# Real chaos agent would interact with Docker API or Kafka Admin Client.
# For prototype, we simulate fault injection by emitting logs and triggering mock failures.

logger = logging.getLogger(__name__)

class ChaosAgent(BaseAgent):
    """
    The Joker of the deck. Injects faults to test system resilience.
    Capabilities:
    1. Induce Latency (Sleep)
    2. Sim Consumer Lag (Mock)
    3. Kill Process (Mock)
    """
    def __init__(self, name: str = "chaos_agent_01"):
        super().__init__(name=name, role="chaos_engineer", goal="Verify System Resilience")
        self.active_faults = []

    async def process_event(self, event):
        # Listen for "start_stress_test" events
        if event.get("action") == "start_stress_test":
            await self.induce_random_fault()

    async def induce_random_fault(self):
        faults = [self._sim_consumer_lag, self._sim_network_latency, self._sim_process_crash]
        selected_fault = random.choice(faults)
        await selected_fault()

    async def _sim_consumer_lag(self):
        logger.warning("😈 CHAOS: Simulating Kafka Consumer Lag (Throttling)...")
        self.active_faults.append("consumer_lag")
        # In real system: await kafka_admin.modify_config(topic, throttling=True)
        await self.emit_trace("CHAOS_INJECTION", "Simulating 5000ms consumer lag.", type="warning")

    async def _sim_network_latency(self):
        logger.warning("😈 CHAOS: Injecting Network Latency...")
        self.active_faults.append("network_latency")
        await self.emit_trace("CHAOS_INJECTION", "Injecting 200ms Jitter.", type="warning")

    async def _sim_process_crash(self):
        logger.critical("😈 CHAOS: Simulating 'Analyst' Container Crash...")
        self.active_faults.append("container_crash")
        # In real system: await docker_client.containers.get('analyst').kill()
        await self.emit_trace("CHAOS_INJECTION", "Killing Dept 1 Container.", type="error")

    async def stop_stress_test(self):
        logger.info("😇 CHAOS: Stopping all active faults.")
        self.active_faults = []
        await self.emit_trace("CHAOS_RESET", "Environment stabilized.", type="info")
