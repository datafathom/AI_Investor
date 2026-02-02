import logging
import json
from services.vc.deal_aggregator import VCDealAggregator
from services.simulation.power_law_sim import PowerLawSimulator

logger = logging.getLogger(__name__)

def list_deals(min_ticket: int = 50):
    """
    CLI Handler for listing active VC deals.
    """
    aggregator = VCDealAggregator()
    deals = aggregator.get_active_deals(min_ticket)
    
    print("\n" + "="*50)
    print(f"          ACTIVE VC DEAL FLOW (Min: ${min_ticket}k)")
    print("="*50)
    if not deals:
        print("No deals matching criteria found.")
    else:
        for d in deals:
            print(f"ID: {d['id']:8} | Name: {d['name']:20} | Stage: {d['stage']}")
            print(f"Sector:  {d['sector']:8} | Min Ticket: ${d['min_ticket_k']}k")
            print("-" * 50)
    print("="*50 + "\n")

def simulate_power_law(count: int = 20):
    """
    CLI Handler for Power Law simulation.
    """
    sim = PowerLawSimulator()
    results = sim.simulate_vc_outcomes(count)
    
    print("\n" + "="*50)
    print(f"          VC POWER LAW SIMULATION ({count} DEALS)")
    print("="*50)
    print(f"Total Invested:   ${results['total_invested_k']:,.0f}k")
    print(f"Total Returned:   ${results['total_returned_k']:,.0f}k")
    print(f"Fund Multiple:    {results['fund_multiple']}x")
    print(f"Home Runs (10x+): {results['winning_ticket_count']}")
    print("-" * 50)
    print("The Power Law: Most returns come from 1-2 winners.")
    print("="*50 + "\n")
