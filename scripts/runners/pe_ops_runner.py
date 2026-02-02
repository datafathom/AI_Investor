import logging
from decimal import Decimal
from services.pe.efficiency_engine import EfficiencyEngine
from services.simulation.sensitivity_analysis import SensitivityEngine

logger = logging.getLogger(__name__)

def run_ops_sim(ebitda: float, opex: float, cut_pct: float):
    """
    CLI Handler for efficiency simulations.
    """
    engine = EfficiencyEngine()
    res = engine.simulate_value_creation(
        Decimal(str(ebitda)),
        Decimal(str(opex)),
        Decimal(str(cut_pct / 100)),
        Decimal('0.05') # 5% baseline efficiency gain
    )
    
    print("\n" + "="*50)
    print("          PE OPERATIONAL VALUE CREATION")
    print("="*50)
    print(f"Base EBITDA:    ${ebitda:,.2f}")
    print(f"OpEx Cut:       {cut_pct}%")
    print("-" * 50)
    print(f"OpEx SAVINGS:   ${res['opex_savings']:,.2f}")
    print(f"NEW EBITDA:     ${res['revised_ebitda']:,.2f}")
    print(f"EBITDA Growth:  {res['ebitda_growth_pct']}%")
    print("="*50 + "\n")

def run_sensitivity(ebitda: float, multiple: float):
    """
    CLI Handler for sensitivity analysis.
    """
    engine = SensitivityEngine()
    res = engine.run_sensitivity_scenarios(Decimal(str(ebitda)), multiple)
    
    print("\n" + "="*50)
    print("          PE SENSITIVITY ANALYSIS")
    print("="*50)
    print(f"Input EBITDA:   ${ebitda:,.2f}")
    print(f"Exit Multiple:  {multiple}x")
    print("-" * 50)
    print(f"Bear Case Min:  ${res['bear_case_min']:,.2f}")
    print(f"MEAN VALUATION: ${res['mean_valuation']:,.2f}")
    print(f"Bull Case Max:  ${res['bull_case_max']:,.2f}")
    print("="*50 + "\n")
