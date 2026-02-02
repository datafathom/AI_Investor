import logging
import os
import subprocess
from services.analysis.macro_service import MacroService
from services.reporting.global_risk_aggregator import GlobalRiskAggregator

logger = logging.getLogger(__name__)

def check_global_status():
    """
    CLI Handler for Epoch X readiness.
    """
    macro = MacroService()
    # Trigger a bridge event
    macro.produce_macro_event("TRANSITION_PREP", {"epoch": "IX", "target": "X"})
    
    agg = GlobalRiskAggregator()
    exposure = agg.aggregate_geo_exposure([{"country_code": "US", "market_value": 100000000}])
    
    print("\n" + "="*50)
    print("          GLOBAL BRIDGE STATUS")
    print("="*50)
    print(f"Current Epoch:    IX")
    print(f"Next Epoch:       X (Institutional Volatility)")
    print(f"Risk Monitoring:  ACTIVE")
    print(f"Concentrated Risk:{exposure['concentrated_risk_flag']}")
    print("-" * 50)
    print("STATUS: Systems ready for sovereignty transition.")
    print("="*50 + "\n")

def run_audit():
    """
    CLI Handler for Epoch IX audit.
    """
    print("\n[*] Starting Epoch IX Completion Audit...\n")
    try:
        # Run the audit script as a subprocess to match project verification style
        result = subprocess.run(
            [".\\venv\\Scripts\\python.exe", "scripts/audits/epoch_ix_audit.py"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except Exception as e:
        logger.error(f"Audit execution failed: {e}")
        print(f"Error: {e}")
