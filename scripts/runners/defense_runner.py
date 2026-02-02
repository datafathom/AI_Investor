import logging
import json
from services.strategies.regime_detector import RegimeDetector
from services.trading.defensive_protocol import DefensiveProtocol

logger = logging.getLogger(__name__)

def status():
    """
    CLI Handler to show current Market Regime.
    """
    detector = RegimeDetector()
    regime = detector.detect_current_regime()
    
    print("\n" + "="*50)
    print("          DEFENSIVE SHIELD STATUS")
    print("="*50)
    print(f"Current Regime:   {regime['name']}")
    print(f"Confidence:       {regime['confidence'] * 100:.1f}%")
    print(f"SPY vs 200 SMA:   {regime['spy_pos']}")
    print("-" * 50)
    
    shield_status = "ACTIVE" if regime['is_risk_off'] else "STANDBY"
    color = "RED" if regime['is_risk_off'] else "GREEN"
    print(f"SHIELD STATE:     {shield_status} ({color})")
    print("="*50 + "\n")

def activate():
    """
    CLI Handler to manually activate defensive protocol.
    """
    protocol = DefensiveProtocol()
    res = protocol.engage_manual_override("CLI_USER_OVERRIDE")
    
    print("\n" + "="*50)
    print("      ⚠️ MANUAL DEFENSE ACTIVATION ⚠️")
    print("="*50)
    print(f"Action:           {res['action']}")
    print(f"Trades Queued:    {res['trades_generated']}")
    print(f"Beta Target:      {res['target_beta']}")
    print("-" * 50)
    print("System is now in FORCED DEFENSE mode.")
    print("="*50 + "\n")
