"""
Institutional Risk Limits Configuration.
Defines hard constraints for position sizing and portfolio drawdown.
"""
from typing import Dict, Any

# Hard Risk Constraints (as decimals)
RISK_CONFIG: Dict[str, Any] = {
    "REGIMES": {
        "NORMAL": {
            "max_risk_per_trade": 0.01,  # 1%
            "trigger": "DEFAULT",
            "description": "Standard market conditions"
        },
        "CONSERVATIVE": {
            "max_risk_per_trade": 0.005, # 0.5%
            "trigger": "VIX > 25",
            "description": "High volatility/uncertainty"
        },
        "ULTRA_SAFE": {
            "max_risk_per_trade": 0.0025, # 0.25%
            "trigger": "CIRCUIT_BREAKER",
            "description": "Systemic risk/post-stopout"
        }
    },
    "MAX_DAILY_DRAWDOWN": 0.03,  # 3% - Freeze all new entries
    "MAX_ASSET_EXPOSURE": 0.10,  # 10% - Force liquidate if loss hits this
    "MIN_STOP_LOSS_PIPS": 10.0,  # Prevent proximity stop-outs
}
