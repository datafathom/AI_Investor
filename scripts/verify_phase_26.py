"""
Verification script for Phase 26.
"""
import sys, os
sys.path.append(os.getcwd())
from services.analysis.structure_scanner import StructureScanner
from services.indicators.atr_calc import ATRCalculator

def run_verification():
    print("=== Phase 26 Verification ===")
    candles = [{"open": 1.10, "high": 1.11, "low": 1.085, "close": 1.10}] * 20
    candles[5]["low"] = 1.0750 # Swing low
    
    swing = StructureScanner.get_stop_level("LONG", candles)
    atr = ATRCalculator.calculate_atr(candles)
    padded = ATRCalculator.get_padded_stop(swing, atr, "LONG")
    
    print(f"Swing Low: {swing}, ATR: {atr:.5f}, Padded SL: {padded}")
    if padded < swing:
        print("✅ Phase 26 SUCCESS")
        return True
    return False

if __name__ == "__main__":
    sys.exit(0 if run_verification() else 1)
