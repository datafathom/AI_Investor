import logging
import json
from services.analysis.filing_analyzer import FilingAnalyzer
from services.valuation.dcf_engine import DCFEngine

logger = logging.getLogger(__name__)

def analyze(ticker: str):
    """
    CLI Handler for full automated Due Diligence.
    """
    print(f"\n[*] Starting deep dive research for ${ticker}...")
    analyzer = FilingAnalyzer()
    
    # Real AI analysis via LLM + SEC Scraper
    try:
        summary = analyzer.analyze_recent_filings(ticker)
        print("\n" + "="*50)
        print(f"          DEEP DIVE REPORT: ${ticker}")
        print("="*50)
        print(">> RISK FACTORS")
        print(summary.get('risk_summary', 'N/A')[:200] + "...")
        print("-" * 50)
        print(">> MANAGEMENT DISCUSSION")
        print(summary.get('mda_summary', 'N/A')[:200] + "...")
        print("-" * 50)
        print(">> MOAT ANALYSIS")
        print(f"Moat Width:     {summary.get('moat_score', 0)}/10")
        print(f"Trend:          {summary.get('moat_trend', 'Unknown')}")
        print("="*50 + "\n")
    except Exception as e:
        print(f"[ERROR] Failed to analyze {ticker}: {e}")

def calc_dcf(ticker: str = 'AAPL'):
    """
    CLI Handler for DCF Valuation.
    """
    engine = DCFEngine()
    
    # Live DCF using yfinance data
    print(f"\n[*] Calculating Intrinsic Value for ${ticker}...")
    try:
        val = engine.calculate_intrinsic_value(ticker)
        
        print("\n" + "="*50)
        print(f"          VALUATION CARD: ${ticker}")
        print("="*50)
        print(f"Current Price:    ${val.get('current_price', 0):,.2f}")
        print(f"Fair Value:       ${val.get('fair_value', 0):,.2f}")
        print("-" * 50)
        
        margin = val.get('margin_of_safety_pct', 0)
        color = "GREEN" if margin > 0 else "RED"
        status = "UNDERVALUED" if margin > 0 else "OVERVALUED"
        
        print(f"Margin of Safety: {margin:+.1f}%")
        print(f"Verdict:          {status} ({color})")
        print("="*50 + "\n")
    except Exception as e:
        print(f"[ERROR] DCF Calculation failed: {e}")
