import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def verify_strategist():
    print("Verifying Strategist Department Imports...")
    try:
        from agents.strategist import (
            LogicArchitectAgent,
            StressTesterAgent,
            RebalanceBotAgent,
            OpportunityScreenerAgent,
            EdgeDecayMonitorAgent,
            PlaybookEvolutionistAgent,
            ConvictionAnalyzerAgent,
            get_strategist_agents
        )
        print("✅ SUCCESS: All strategist agents imported successfully.")
        
        agents = get_strategist_agents()
        print(f"✅ SUCCESS: Factory returned {len(agents)} agents.")
        expected_keys = [
            "strategist.logic_architect",
            "strategist.stress_tester",
            "strategist.rebalance_bot",
            "strategist.opportunity_screener",
            "strategist.edge_decay_monitor",
            "strategist.playbook_evolutionist",
            "strategist.conviction_analyzer"
        ]
        for key in expected_keys:
            if key in agents:
                print(f"  - Found {key}")
            else:
                print(f"  ❌ MISSING: {key}")
                return False
        return True
    except ImportError as e:
        print(f"❌ FAILED: Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = verify_strategist()
    sys.exit(0 if success else 1)
