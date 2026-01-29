"""
Verification script for Phase 22.
Simulates aggressive user behavior and verifies the trigger of a 4-hour trading lock.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.risk.lock_manager import LockManager
from services.risk.tilt_detector import TiltDetector

def run_verification():
    print("=== Starting Phase 22 Verification ===")
    
    manager = LockManager()
    detector = TiltDetector()
    user_id = "user_789"

    # 1. Simulate Aggressive Interaction (Spam Click)
    print("\n[1/3] Simulating Aggressive User Behavior (10 failed clicks)...")
    is_tilt = False
    for i in range(10):
        is_tilt = detector.record_attempt()
        if is_tilt:
            print(f"✅ TILT detected at click #{i+1}!")
            break
    
    if not is_tilt:
        print("❌ Tilt detector failed to catch spam!")
        return False

    # 2. Trigger Lock
    print("\n[2/3] Applying Mandatory Cooling-Off Period (4h)...")
    manager.apply_lock(user_id, duration_hours=4, reason="TILT_DETECTED")
    
    # 3. Verify Enforcement
    print("\n[3/3] Verifying Security Lockdown...")
    locked, reason = manager.is_user_locked(user_id)
    if locked and "COOLING_OFF" in reason :
        print(f"✅ Lockdown Active: {reason}")
    else:
        print("❌ Lock manager failed to enforce cooldown!")
        return False

    print("\n=== Phase 22 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
