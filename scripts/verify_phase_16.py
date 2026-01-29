"""
Verification script for Phase 16.
Simulates high-risk trade scenarios to ensure the 1% rule and risk gates are working.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.risk.position_sizer import PositionSizer
from services.risk.risk_constraint import RiskConstraint
from services.portfolio.fast_balance import get_balance_service
from services.risk.bypass_detector import BypassDetector

def run_verification():
    print("=== Starting Phase 16 Verification ===")
    
    balance_svc = get_balance_service()
    equity = balance_svc.get_latest_equity()
    print(f"Initial Equity: ${equity:,.2f}")

    # 1. Standard Compliant Trade
    print("\n[1/4] Testing Standard 1% Trade (EUR/USD, 30 pip SL)...")
    sizing = PositionSizer.calculate_size(equity, 30.0, "EUR/USD")
    print(f"Calculated Sizing: {sizing['lots']} lots | Risk: ${sizing['risk_amount']}")
    
    is_valid, reason = RiskConstraint.validate_proposal(sizing, equity)
    if is_valid:
        print(f"✅ Trade Validated: {reason}")
    else:
        print(f"❌ Trade Rejected: {reason}")
        return False

    # 2. Risk Violation (Manual calculation attempt)
    print("\n[2/4] Testing Risk Violation Detection (10.0 lots on tiny SL)...")
    bad_proposal = {
        "lots": 10.0,
        "risk_amount": 5000.0, # 5% of 100k
        "stop_loss_pips": 5.0
    }
    is_valid, reason = RiskConstraint.validate_proposal(bad_proposal, equity)
    if not is_valid and "EXCESSIVE_RISK" in reason:
        print(f"✅ Blocked Excessive Risk: {reason}")
    else:
        print("❌ Failed to block excessive risk.")
        return False

    # 3. Circuit Breaker Test
    print("\n[3/4] Testing Drawdown Circuit Breaker (4% Drawdown)...")
    is_valid, reason = RiskConstraint.validate_proposal(sizing, equity, daily_drawdown_pct=0.04)
    if not is_valid and "CIRCUIT_BREAKER" in reason:
        print(f"✅ Blocked by Circuit Breaker: {reason}")
    else:
        print("❌ Circuit breaker failed to trigger.")
        return False

    # 4. Bypass Certification Test
    print("\n[4/4] Testing Bypass Detection...")
    order_req = {"symbol": "GBP/USD", "lots": 1.0} # Lacks 'risk_certified'
    approved, reason = BypassDetector.inspect_order(order_req)
    if not approved and "SECURITY_VIOLATION" in reason:
        print(f"✅ Security Bypass Detected: {reason}")
    else:
        print("❌ Bypass detector failed to catch uncertified order.")
        return False

    print("\n=== Phase 16 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
