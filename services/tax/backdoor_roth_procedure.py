import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BackdoorRothProcedure:
    """Automates the multi-step Backdoor Roth conversion protocol."""
    
    def get_step_plan(self, current_ira_balance: float) -> List[Dict[str, str]]:
        steps = [
            {"step": 1, "action": "CONTRIBUTE_NON_DEDUCTIBLE", "desc": "Make non-deductible contribution to Traditional IRA."},
            {"step": 2, "action": "WAIT_SETTLEMENT", "desc": "Wait for funds to settle (typically 1-3 days)."},
            {"step": 3, "action": "CONVERT_TO_ROTH", "desc": "Convert entire Trad IRA balance to Roth IRA."}
        ]
        
        if current_ira_balance > 0:
            logger.warning("TAX_WARNING: Mixed Trad IRA balance detected. Pro-Rata rule will trigger taxes.")
            steps.insert(0, {"step": 0, "action": "CLEAR_TRAD_IRA", "desc": "Rollover existing Trad IRA to 401k to avoid Pro-Rata taxes."})
            
        return steps
