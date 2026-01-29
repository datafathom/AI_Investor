import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmergencyFundAlertService:
    """
    Tiered alert system for emergency fund coverage.
    """
    
    TIERS = {
        'CRITICAL': {'min': 0, 'max': 3, 'color': 'red', 'block_trades': True, 'alert_type': 'URGENT'},
        'LOW': {'min': 3, 'max': 6, 'color': 'orange', 'block_trades': False, 'alert_type': 'WARNING'},
        'ADEQUATE': {'min': 6, 'max': 12, 'color': 'yellow', 'block_trades': False, 'alert_type': 'INFO'},
        'STRONG': {'min': 12, 'max': 24, 'color': 'green', 'block_trades': False, 'alert_type': 'NONE'},
        'FORTRESS': {'min': 24, 'max': 36, 'color': 'blue', 'block_trades': False, 'alert_type': 'NONE'}
    }
    
    def evaluate_coverage(self, months: float) -> Dict[str, Any]:
        """Determine tier and required actions based on months of coverage."""
        for tier, config in self.TIERS.items():
            if config['min'] <= months < config['max']:
                result = {
                    "tier": tier,
                    "config": config,
                    "action_required": config['block_trades'],
                    "message": f"Emergency fund status: {tier}. {'Trading RESTRICTED' if config['block_trades'] else 'Monitoring active'}"
                }
                logger.info(f"ALERT_EVAL: {result['message']}")
                return result
        
        # Default for fortress
        return {"tier": "FORTRESS", "config": self.TIERS['FORTRESS'], "action_required": False}

    def get_notification_channels(self, tier: str) -> list:
        if tier == "CRITICAL":
            return ["PUSH", "EMAIL", "SMS"]
        if tier == "LOW":
            return ["PUSH", "EMAIL"]
        return ["PUSH"]
