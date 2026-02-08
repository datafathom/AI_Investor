import logging
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class MetricType(Enum):
    LATENCY = "latency"
    CPU_USAGE = "cpu"
    MEMORY_USAGE = "memory"
    ERROR_RATE = "error_rate"
    DOWNTIME = "downtime"

class AlertRuleManager:
    """Manages threshold rules for automated alerting."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertRuleManager, cls).__new__(cls)
            cls._instance._init_rules()
        return cls._instance

    def _init_rules(self):
        # Default system rules
        self.rules = [
            {
                "id": "rule_latency_critical",
                "name": "API_LATENCY_CRITICAL",
                "metric": MetricType.LATENCY.value,
                "threshold": 2000, # ms
                "comparison": ">",
                "duration": 60, # seconds
                "severity": "critical",
                "enabled": True,
                "channels": ["slack", "pagerduty"]
            },
            {
                "id": "rule_error_spike",
                "name": "INTERNAL_ERROR_SPIKE",
                "metric": MetricType.ERROR_RATE.value,
                "threshold": 5, # %
                "comparison": ">",
                "duration": 300,
                "severity": "error",
                "enabled": True,
                "channels": ["slack", "email"]
            },
            {
                "id": "rule_service_down",
                "name": "CORE_SERVICE_UNREACHABLE",
                "metric": MetricType.DOWNTIME.value,
                "threshold": 1,
                "comparison": "==",
                "duration": 0,
                "severity": "critical",
                "enabled": True,
                "channels": ["slack", "pagerduty", "sms"]
            }
        ]

    def get_rules(self) -> List[Dict[str, Any]]:
        return self.rules

    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        new_rule = {
            "id": f"rule_{int(datetime.now().timestamp())}",
            **rule_data
        }
        self.rules.append(new_rule)
        logger.info(f"New alert rule created: {new_rule['name']}")
        return new_rule

    def update_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for i, rule in enumerate(self.rules):
            if rule['id'] == rule_id:
                self.rules[i].update(rule_data)
                logger.info(f"Alert rule updated: {rule_id}")
                return self.rules[i]
        return None

    def delete_rule(self, rule_id: str) -> bool:
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r['id'] != rule_id]
        if len(self.rules) < initial_count:
            logger.warning(f"Alert rule deleted: {rule_id}")
            return True
        return False

def get_alert_rule_manager() -> AlertRuleManager:
    return AlertRuleManager()
