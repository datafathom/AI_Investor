"""
Verification script for Phase 8: Protector Agent.
Runs unit tests and CLI protector command.
"""
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        print(result.stderr)
        return False
    print(result.stdout)
    return True

def main():
    print("=== Starting Phase 8 Verification ===")
    
    # 1. Run Unit Tests
    print("\n[1/3] Running Unit Tests...")
    if not run_command("python -m pytest tests/unit/test_protector_agent.py"):
        sys.exit(1)
        
    # 2. Test Good Order
    print("\n[2/3] Testing Good Order ($500 Risk)...")
    if not run_command("python cli.py test-protector --amount 500.0"):
        sys.exit(1)

    # 3. Test Bad Order
    print("\n[3/3] Testing Bad Order ($2000 Risk)...")
    if not run_command("python cli.py test-protector --amount 2000.0"):
        sys.exit(1)
        
    print("\n✅ All Phase 8 verifications passed!")

if __name__ == "__main__":
    main()
