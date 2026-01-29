"""
Verification script for Phase 20.
Simulates an asset price collapse of 11% to verify the 10% Kill Switch intervention.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.risk.asset_kill_switch import AssetKillSwitch
from services.audit.forensic_vault import ForensicVault

def run_verification():
    print("=== Starting Phase 20 Verification ===")
    
    ks = AssetKillSwitch(kill_threshold=0.10)
    vault = ForensicVault()

    # 1. Simulate Active Position
    print("\n[1/3] Setting up Position (EUR/USD, Entry 1.1000)...")
    positions = [{"symbol": "EUR/USD", "entry_price": 1.1000, "side": "LONG"}]
    
    # 2. Market Collapse (Price drops 11%)
    print("\n[2/3] Simulating Market Collapse (Price drops to 0.9790)...")
    spot_prices = {"EUR/USD": 0.9790} # 1.10 * 0.89 = 0.979 (11% loss)
    
    targets = ks.inspect_portfolio(positions, spot_prices)
    
    if "EUR/USD" in targets:
        print("✅ Nuclear Trigger Identified: Asset breached 10% limit.")
        ks.execute_liquidation("EUR/USD")
    else:
        print("❌ Kill Switch failed to detect 11% breach!")
        return False

    # 3. Forensic Capture
    print("\n[3/3] Testing Forensic State Capture...")
    context = vault.get_market_context()
    incident = vault.capture_incident("EUR/USD", 0.11, context)
    
    if incident["severity"] == "CRITICAL" and incident["drawdown_pct"] == 0.11:
        print("✅ Forensic Package Validated.")
    else:
        print("❌ Forensic capture failed!")
        return False

    print("\n=== Phase 20 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
