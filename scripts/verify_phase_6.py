"""
Verification script for Phase 6: Demo Account.
Runs unit tests and CLI demo commands.
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
    print("=== Starting Phase 6 Verification ===")
    
    # 1. Run Unit Tests
    print("\n[1/3] Running Unit Tests...")
    if not run_command("python -m pytest tests/unit/test_demo_broker.py"):
        sys.exit(1)
        
    # 2. Run CLI Demo Reset
    print("\n[2/3] Testing CLI Demo Reset...")
    if not run_command("python cli.py demo-reset"):
        sys.exit(1)

    # 3. Run CLI Demo Trade
    print("\n[3/3] Testing CLI Demo Trade...")
    if not run_command("python cli.py demo-trade --symbol AAPL --side BUY --qty 10 --price 150.00"):
        sys.exit(1)
        
    print("\n✅ All Phase 6 verifications passed!")

if __name__ == "__main__":
    main()
