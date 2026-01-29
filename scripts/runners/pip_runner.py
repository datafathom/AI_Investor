"""
Runner for pip calculation CLI commands.
"""
import sys
from services.pip_calculator import PipCalculatorService
from config.currency_pairs import MAJOR_PAIRS

def run_pip_test(pair: str, p1: str, p2: str):
    """
    Test pip calculation for a given pair.
    """
    calculator = PipCalculatorService()
    try:
        pips = calculator.calculate_pips(p1, p2, pair)
        print(f"Pip Difference for {pair} ({p1} -> {p2}): {pips}")
    except Exception as e:
        print(f"Error calculating pips: {e}", file=sys.stderr)
        sys.exit(1)

def run_pip_benchmark():
    """
    Run accuracy benchmarks for major pairs.
    """
    calculator = PipCalculatorService()
    print("Running Pip Calculation Benchmarks...")
    print("-" * 60)
    print(f"{'Pair':<10} | {'Price 1':<10} | {'Price 2':<10} | {'Diff':<10} | {'Pips':<10}")
    print("-" * 60)
    
    test_cases = [
        ("GBP/USD", 1.26956, 1.27056),
        ("EUR/USD", 1.08500, 1.08600),
        ("USD/JPY", 149.000, 149.100),
        ("AUD/USD", 0.65000, 0.65100),
    ]
    
    all_passed = True
    
    for pair, p1, p2 in test_cases:
        pips = calculator.calculate_pips(p1, p2, pair)
        diff = p2 - p1
        expected = 10.0
        status = "PASS" if pips == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"{pair:<10} | {p1:<10.5f} | {p2:<10.5f} | {diff:<10.5f} | {pips:<10.1f} ({status})")
        
    print("-" * 60)
    if all_passed:
        print("✅ All benchmarks passed.")
    else:
        print("❌ Some benchmarks failed.")
        sys.exit(1)
