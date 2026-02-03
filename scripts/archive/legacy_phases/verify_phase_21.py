"""
Verification script for Phase 21.
Simulates a global portfolio drawdown of 3.5% to verify the 3% circuit breaker intervention.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.risk.drawdown_aggregator import DrawdownAggregator
from services.risk.portfolio_circuit_breaker import PortfolioCircuitBreaker
from services.kafka.freeze_publisher import FreezePublisher

def run_verification():
    print("=== Starting Phase 21 Verification ===")
    
    agg = DrawdownAggregator(start_of_day_equity=Decimal("100000.00"))
    breaker = PortfolioCircuitBreaker(agg)
    publisher = FreezePublisher()

    # 1. Simulate Heavy Day Loss (3.5% Drawdown)
    print("\n[1/3] Simulating Extreme Daily Loss ($3,500)...")
    agg.update_pnl(realized=Decimal("-2000.00"), unrealized=Decimal("-1500.00"))
    loss_pct = agg.get_total_drawdown_pct()
    print(f"Current Daily Drawdown: {loss_pct:.2%}")

    if agg.is_3_percent_breached():
         print("✅ 3% Breach Detected by Aggregator.")
    else:
         print("❌ Aggregator failed to detect breach!")
         return False

    # 2. Test Trading Blockade (Zen Mode)
    print("\n[2/3] Verifying Execution Blockade (Gatekeeper)...")
    allowed, reason = breaker.is_trading_allowed()
    if not allowed and "ZEN_MODE" in reason:
        print(f"✅ Trading Blocked: {reason}")
    else:
        print(f"❌ Circuit breaker failed to block trading!")
        return False

    # 3. Test Kafka Broadcast
    print("\n[3/3] Simulating Global Freeze Broadcast...")
    event = publisher.publish_freeze(loss_pct, float(Decimal("100000.00") + Decimal("-3500.00")))
    if event["event_type"] == "THE_3_PERCENT_FREEZE":
        print("✅ Global broadcast packet validated.")
    else:
        print("❌ Broadcast failed!")
        return False

    print("\n=== Phase 21 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
