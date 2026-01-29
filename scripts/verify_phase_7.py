"""
Verification script for Phase 7: Searcher Agent.
Runs unit tests and CLI searcher command.
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
    print("=== Starting Phase 7 Verification ===")
    
    # 1. Run Unit Tests
    print("\n[1/2] Running Unit Tests...")
    if not run_command("python -m pytest tests/unit/test_searcher_agent.py"):
        sys.exit(1)
        
    # 2. Run CLI Searcher Scan
    print("\n[2/2] Testing CLI Searcher Scan...")
    if not run_command("python cli.py test-searcher"):
        sys.exit(1)
        
    print("\n✅ All Phase 7 verifications passed!")

if __name__ == "__main__":
    main()
