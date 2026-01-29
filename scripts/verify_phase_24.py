"""
Verification script for Phase 24.
Simulates institutional Order Block detection and trade filtering.
"""
import sys
import os

# Ensure paths
sys.path.append(os.getcwd())

from services.analysis.order_blocks import OrderBlockDetector
from services.neo4j.liquidity_graph import LiquidityGraph
from services.strategies.zone_filter import ZoneFilter

def run_verification():
    print("=== Starting Phase 24 Verification ===")
    
    detector = OrderBlockDetector()
    graph = LiquidityGraph()
    z_filter = ZoneFilter()

    # 1. Simulate Order Block Detection (Institutional Move)
    print("\n[1/3] Simulating Institutional Demand Zone Detection...")
    candles = [
        {"open": 1.0800, "high": 1.0810, "low": 1.0790, "close": 1.0805}, # Consolidation
        {"open": 1.0805, "high": 1.1050, "low": 1.0800, "close": 1.1000}  # Strong Impulse Up
    ]
    zones = detector.detect_zones(candles, atr_multiplier=2.0)
    if zones and zones[0]["type"] == "DEMAND":
        print(f"✅ Demand Zone Detected at {zones[0]['price_low']} - {zones[0]['price_high']}")
        demand_zone = zones[0]
        graph.add_zone("EURUSD", demand_zone)
    else:
        print("❌ Failed to detect Demand zone!")
        return False

    # 2. Test Signal Filtering (Avoid Sell into Demand)
    print("\n[2/3] Verifying Signal Gate (Sell into Demand Block)...")
    price_near_demand = 1.0803 # Inside Demand zone [1.0790, 1.0810]
    ok, reason = z_filter.validate_signal("SELL", price_near_demand, nearest_demand=demand_zone)
    if not ok and "LIMIT_BLOCKED" in reason:
        print(f"✅ Trade Blocked: {reason}")
    else:
        print("❌ Zone filter failed to block low-probability sell signal!")
        return False

    # 3. Test Signal Approval (Safe Trade)
    print("\n[3/3] Verifying Signal Gate (Clearing Safe Trade)...")
    price_safe = 1.0850 # Clear of demand
    ok, reason = z_filter.validate_signal("BUY", price_safe, nearest_demand=demand_zone)
    if ok:
        print(f"✅ Signal Cleared: {reason}")
    else:
        print("❌ Filter blocked a safe trade!")
        return False

    print("\n=== Phase 24 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
