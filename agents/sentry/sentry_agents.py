from typing import Dict
from agents.base_agent import BaseAgent
from agents.sentry.breach_sentinel_agent import BreachSentinelAgent
from agents.sentry.api_key_rotator_agent import ApiKeyRotatorAgent
from agents.sentry.travel_mode_guard_agent import TravelModeGuardAgent
from agents.sentry.cold_storage_auditor_agent import ColdStorageAuditorAgent
from agents.sentry.permission_auditor_agent import PermissionAuditorAgent
from agents.sentry.recovery_path_builder_agent import RecoveryPathBuilderAgent

def get_sentry_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Sentry department agents.
    """
    return {
        "sentry.breach_sentinel": BreachSentinelAgent(),
        "sentry.api_key_rotator": ApiKeyRotatorAgent(),
        "sentry.travel_mode_guard": TravelModeGuardAgent(),
        "sentry.cold_storage_auditor": ColdStorageAuditorAgent(),
        "sentry.permission_auditor": PermissionAuditorAgent(),
        "sentry.recovery_path_builder": RecoveryPathBuilderAgent(),
    }
