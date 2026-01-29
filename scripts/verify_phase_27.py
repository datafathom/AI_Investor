"""
Verification script for Phase 27.
"""
import sys, os
sys.path.append(os.getcwd())
from services.warden.routine_runner import WardenRoutine

def run_verification():
    print("=== Phase 27 Verification ===")
    warden = WardenRoutine()
    result = warden.perform_health_check()
    print(f"Health Check: {result}")
    if result["overall_status"] == "HEALTHY":
        print("✅ Phase 27 SUCCESS")
        return True
    return False

if __name__ == "__main__":
    sys.exit(0 if run_verification() else 1)
