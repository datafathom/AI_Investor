import pytest
from services.analytics.alpha_reporting import get_alpha_reporting_service
from services.meta_optimizer import get_meta_optimizer_service

def test_alpha_reporting_logic():
    svc = get_alpha_reporting_service()
    report = svc.generate_eod_report()
    
    assert report['status'] == "GENERATED"
    assert report['total_pnl'] > 0
    # Based on mock data: Crypto (0.15) > Equities (0.08) > Bonds (0.005) > Macro (-0.02)
    assert report['mvp_agent']['sector'] == "Crypto"
    assert "Crypto" in report['sector_performance']

def test_meta_mission_proposals():
    # Meta Optimizer relies on Alpha Reporting
    meta_svc = get_meta_optimizer_service()
    proposals = meta_svc.run_optimization_cycle()
    
    assert len(proposals) >= 1
    
    # Check for Scaling UP the winner (Crypto)
    scale_up = next((p for p in proposals if p['type'] == "SCALE_UP"), None)
    assert scale_up is not None
    assert scale_up['target_sector'] == "Crypto"
    
    # Check for Scaling DOWN the loser (Macro)
    scale_down = next((p for p in proposals if p['type'] == "SCALE_DOWN"), None)
    assert scale_down is not None
    assert scale_down['target_sector'] == "Macro"
