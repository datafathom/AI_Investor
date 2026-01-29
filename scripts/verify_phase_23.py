"""
Verification script for Phase 23.
Simulates a database configuration load with SHA-256 integrity validation.
Verifies that Safe Mode is triggered on hash mismatch.
"""
import sys
import os
import uuid

# Ensure paths
sys.path.append(os.getcwd())

from services.security.config_integrity import ConfigIntegrity
from services.risk.config_manager import ConfigManager

def run_verification():
    print("=== Starting Phase 23 Verification ===")
    
    manager = ConfigManager()
    
    # 1. Valid Configuration State
    print("\n[1/3] Testing Valid Configuration Hydration...")
    valid_record = {
        "id": str(uuid.uuid4()),
        "version": 1,
        "max_position_size_pct": 0.01,
        "daily_drawdown_limit_pct": 0.03,
        "max_leverage_ratio": 1.0,
        "min_stop_loss_pips": 10.0
    }
    valid_hash = ConfigIntegrity.generate_state_hash(valid_record)
    
    manager.hydrate_from_db(valid_record, valid_hash)
    if not manager.safe_mode:
        print("✅ Hydration Success: Integrity verified.")
    else:
        print("❌ Hydration failed on valid data!")
        return False

    # 2. Tampered Configuration State (Tripwire Test)
    print("\n[2/3] Simulating Tripwire (Database Tampering)...")
    tampered_record = valid_record.copy()
    tampered_record["max_position_size_pct"] = 0.50 # Rogue change to 50% risk!
    
    # Use the OLD hash (simulating a DB update without signature update)
    manager.hydrate_from_db(tampered_record, valid_hash)
    
    if manager.safe_mode:
        print("✅ Tripwire Triggered: Hash mismatch detected.")
        print(f"✅ System Status: {manager.get_param('status')}")
    else:
        print("❌ Tamper attempt was NOT detected!")
        return False

    # 3. Safe Mode Parameter Enforcement
    print("\n[3/3] Verifying Safe Mode Constraints (0% Risk)...")
    risk_param = manager.get_param("max_position_size_pct")
    if risk_param == 0.0:
        print(f"✅ Enforcement Validated: Max Risk capped at {risk_param}.")
    else:
        print(f"❌ Safe Mode failed to cap risk! Value: {risk_param}")
        return False

    print("\n=== Phase 23 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
