import sys
import os
import logging

# Add project root to path
sys.path.append(os.getcwd())

from services.vc.deal_aggregator import VCDealAggregator
from services.vc.tier1_scorer import Tier1Scorer
from services.vc.contrarian_detector import ContrarianDetector
from services.neo4j.vc_network import VCNetworkService
from services.simulation.power_law_sim import PowerLawSimulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_165")

def verify_165():
    print("\n" + "="*60)
    print("       PHASE 165: VENTURE CAPITAL DEAL FLOW VERIFICATION")
    print("="*60 + "\n")

    # 1. Deal Aggregator
    print("[*] Testing VCDealAggregator...")
    agg = VCDealAggregator()
    deals = agg.get_active_deals(min_ticket_k=100)
    print(f"    Found {len(deals)} deals >= $100k (Expected: 2)")
    
    # 2. Tier 1 Scorer
    print("\n[*] Testing Tier1Scorer...")
    scorer = Tier1Scorer()
    res = scorer.get_firm_score("Sequoia")
    print(f"    Sequoia is Tier 1: {res['is_tier1']} (Expected: True)")

    # 3. Contrarian Detector
    print("\n[*] Testing ContrarianDetector...")
    det = ContrarianDetector()
    opp = det.analyze_deal_sentiment("AI Infrastructure", 0.95)
    print(f"    High Hype AI Contrarian: {opp['is_contrarian_bet']} (Expected: False)")

    # 4. VC Network
    print("\n[*] Testing VCNetworkService...")
    graph = VCNetworkService()
    graph.map_founder_network("SerialFounder", ["a16z", "Benchmark"])
    serials = graph.find_serial_entrepreneurs()
    print(f"    Serial Entrepreneurs: {serials}")

    # 5. Power Law Simulator
    print("\n[*] Testing PowerLawSimulator...")
    sim = PowerLawSimulator()
    outcome = sim.simulate_vc_outcomes(50)
    print(f"    50-Deal Portfolio Multiple: {outcome['fund_multiple']}x")

    print("\n" + "="*60)
    print("               PHASE 165 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_165()
