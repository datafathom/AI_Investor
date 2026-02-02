import logging
from services.quantitative.reflexivity_engine import ReflexivityEngine
from services.simulation.reflexivity_sim import ReflexivitySim
from services.alerts.demographic_risk import DemographicRiskMonitor

logger = logging.getLogger(__name__)

def check_stock(ticker: str):
    """
    CLI Handler for passive saturation check.
    """
    engine = ReflexivityEngine()
    # Mock data for demonstration
    res = engine.check_passive_saturation(ticker, 45000000, 100000000)
    
    print("\n" + "="*50)
    print("          PASSIVE SATURATION CHECK")
    print("="*50)
    print(f"Ticker:           {res['ticker']}")
    print(f"Passive Ownership:{res['passive_ownership_pct']}%")
    print(f"Saturated:        {res['is_saturated_reflexive']}")
    print(f"Inelasticity:     {res['inelasticity_rank']}")
    print("-" * 50)
    print("STATUS: " + ("EXTREME RISK" if res['is_saturated_reflexive'] else "NORMAL"))
    print("="*50 + "\n")

def sim_crash():
    """
    CLI Handler for passive unwind simulation.
    """
    sim = ReflexivitySim()
    res = sim.simulate_unwind(450.0, 0.15)
    
    drm = DemographicRiskMonitor()
    demo = drm.calculate_net_flow_status(12.5, 8.2)
    
    print("\n" + "="*50)
    print("          PASSIVE UNWIND SIMULATION")
    print("="*50)
    print(f"Current Price:    ${res['initial_price']:.2f}")
    print(f"Social Shock:     -{res['shock_pct']:.0%}")
    print("-" * 50)
    print(f"Unwind Price:     ${res['final_unwind_price']:.2f}")
    print(f"Crash Probability: {res['status']}")
    print("-" * 50)
    print(f"Demographic Flow: ${demo['net_flow_b']}B (NET OUTFLOW)")
    print(f"Recommendation:   {demo['recommendation']}")
    print("="*50 + "\n")
