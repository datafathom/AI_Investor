"""
Sentry Department Agents (11.3)
Phase 8 Implementation: The Global HQ

Handles Travel Security, Geofencing, and Biometric Re-Sync.
"""

import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentState
from services.security.geofence_service import get_geofence_service

logger = logging.getLogger(__name__)

class TravelGuardAgent(BaseAgent):
    """
    AGENT 11.3: The Travel-Mode Guard
    Monitors device divergence and triggers biometric lockouts.
    """
    def __init__(self):
        super().__init__("sentry.guard.11.3")
        self.geofence = get_geofence_service()

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Processes location updates and heartbeat checks.
        """
        e_type = event.get("type")
        
        if e_type == "security.location_update":
            self.geofence.update_location(
                event.get("device_id"),
                event.get("lat"),
                event.get("lon")
            )
            return {"status": "received"}

        elif e_type == "security.check_divergence":
            return await self._check_divergence(event)
            
        return None

    async def _check_divergence(self, event: Dict[str, Any]) -> Dict[str, Any]:
        await self.transition_to(AgentState.SCANNING, "Auditing device coordinate synchronization")
        
        primary = event.get("primary_device")
        mobile = event.get("trusted_mobile")
        
        await self.transition_to(AgentState.ANALYZING, f"Calculating distance between {primary} and {mobile}")
        
        verdict = self.geofence.check_security_violation(primary, mobile)
        
        if not verdict.get("is_safe", True):
            await self.transition_to(AgentState.ERROR, f"DIVERGENCE DETECTED: {verdict['distance_meters']:.2f} meters")
            await self.emit_trace("SECURITY_ALERT", f"Divergence mismatch. Proximity threshold exceeded.", "error")
            return {
                "action": "LOCK_SYSTEM",
                "details": verdict
            }

        await self.transition_to(AgentState.COMPLETED, "Proximity within safe parameters")
        return {
            "action": "CONTINUE",
            "details": verdict
        }
