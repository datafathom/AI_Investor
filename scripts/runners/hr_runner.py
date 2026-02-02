import logging
import json
from decimal import Decimal
from services.performance.staff_attribution import StaffAttributionEngine
from services.operations.outsource_calc import OperationsOutsourceCalculator

logger = logging.getLogger(__name__)

def check_comp(role: str):
    """
    CLI Handler for Staff Compensation Benchmarking.
    """
    engine = StaffAttributionEngine()
    bench = engine.get_comp_benchmark(role)
    
    print("\n" + "="*50)
    print(f"          COMPENSATION BENCHMARK: {role.upper()}")
    print("="*50)
    print(f"Base Range:  ${bench['market_base_range'][0]:,.2f} - ${bench['market_base_range'][1]:,.2f}")
    print(f"Target Bonus: {bench['target_bonus_pct']}% of base")
    print("-" * 50)
    print("Source: AI_Investor Institutional HR Data")
    print("="*50 + "\n")

def calc_bonus(staff_id: str, alpha_bps: float = 0):
    """
    CLI Handler for Bonus Calculation.
    """
    # Simple logic: 20% of alpha dollar value if performance-based
    # For demo, assumes $100M AUM
    aum = Decimal('100000000')
    alpha_val = aum * (Decimal(str(alpha_bps)) / Decimal('10000'))
    bonus = alpha_val * Decimal('0.20')
    
    print("\n" + "="*50)
    print(f"          BONUS PROJECTION: {staff_id}")
    print("="*50)
    print(f"Alpha Generated:  {alpha_bps} bps (${alpha_val:,.2f})")
    print(f"Projected Bonus:  ${bonus:,.2f} (20% Carry)")
    print("-" * 50)
    print("STATUS: PENDING APPROVAL")
    print("="*50 + "\n")
