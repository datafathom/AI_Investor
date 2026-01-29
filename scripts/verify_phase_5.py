"""
Verification script for Phase 5: Pip Calculator.
Runs unit tests and CLI benchmark.
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
    print("=== Starting Phase 5 Verification ===")
    
    # 1. Run Unit Tests
    print("\n[1/2] Running Unit Tests...")
    if not run_command("python -m pytest tests/unit/test_pip_calculator.py"):
        sys.exit(1)
        
    # 2. Run CLI Benchmark
    print("\n[2/2] Running CLI Benchmark...")
    if not run_command("python cli.py pip-benchmark"):
        sys.exit(1)
        
    print("\n✅ All Phase 5 verifications passed!")

if __name__ == "__main__":
    main()
