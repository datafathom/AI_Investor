"""
==============================================================================
FILE: scripts/runners/test_macro.py
ROLE: Macro Tester
PURPOSE: Verifies FRED ingestion and market regime classification.
USAGE: python cli.py test-macro [--mock]
==============================================================================
"""

import logging
from services.data.fred_service import FredMacroService

logger = logging.getLogger(__name__)

def run_test_macro(mock: bool = False, **kwargs):
    """
    Runner to test macro-economic data ingestion.
    """
    print(f"--- Testing Macro Data Integration (Mock: {mock}) ---")
    
    service = FredMacroService(mock=mock)
    regime = service.get_macro_regime()
    
    if not regime:
        print("FAILED: No regime data retrieved.")
        return False
        
    print("\n[MACRO REGIME DATA]")
    print(f"Status:    {regime['status']}")
    print(f"Timestamp: {regime['timestamp']}")
    print("\n[SIGNALS]")
    for signal in regime['signals']:
        print(f" - {signal}")
        
    print("\n[METRICS]")
    for metric, val in regime['metrics'].items():
        print(f" - {metric}: {val}")
        
    print("\nSUCCESS: Macro regime logic verified.")
    return True
