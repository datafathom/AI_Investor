import logging
import json
from decimal import Decimal
from services.pe.lbo_engine import LBOEngine
from services.pe.efficiency_engine import EfficiencyEngine

logger = logging.getLogger(__name__)

def calc_lbo(ebitda: str, multiple: float, equity_pct: float = 0.3):
    """
    CLI Handler for quick LBO modeling.
    """
    try:
        engine = LBOEngine()
        ebitda_val = Decimal(ebitda.replace(',', ''))
        
        # Scenario assumptions
        results = engine.project_deal_returns(
            entry_ebitda=ebitda_val,
            entry_multiple=Decimal(str(multiple)),
            equity_contribution_pct=Decimal(str(equity_pct)),
            exit_multiple=Decimal(str(multiple)), # Default: no multiple expansion
            years=5,
            revenue_growth_pct=Decimal('0.05') # 5% growth
        )
        
        print("\n" + "="*50)
        print("          PRIVATE EQUITY LBO PROJECTION")
        print("="*50)
        print(f"Entry EBITDA:     ${ebitda_val:,.2f} x {multiple}")
        print(f"Equity (at {equity_pct*100}%):  ${results['entry_equity']:,.2f}")
        print("-" * 50)
        print(f"Exit Equity (Yr 5): ${results['exit_equity']:,.2f}")
        print(f"MOIC:             {results['moic']}x")
        print(f"IRR:              {results['irr_pct']}%")
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"LBO Calculation Failed: {e}")
        print(f"Error: {e}")

def vintage_stats(year: int):
    """
    CLI Handler for PE Vintage Year Analysis.
    """
    engine = EfficiencyEngine()
    stats = engine.get_vintage_performance(year)
    
    print("\n" + "="*50)
    print(f"          PE VINTAGE YEAR STATS: {year}")
    print("="*50)
    print(f"Market Cycle:     {stats['market_cycle']}")
    print(f"Average MOIC:     {stats['avg_moic']}x")
    print(f"Average IRR:      {stats['avg_irr']}%")
    print("-" * 50)
    print("Source: AI_Investor Market Cycle Analyzer")
    print("="*50 + "\n")
