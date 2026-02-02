import logging
import datetime
from decimal import Decimal
from services.compliance.insider_trading_svc import InsiderTradingService
from services.ingestion.sec_scraper import SECScraper

logger = logging.getLogger(__name__)

def check_limit(ticker: str, shares: int, outstanding: int, vol: int):
    """
    CLI Handler for Rule 144(e) volume limit check.
    """
    svc = InsiderTradingService()
    # Assume 180 day lockup usually, but for check-limit we focus on volume
    open_date = datetime.date.today() - datetime.timedelta(days=1)
    
    res = svc.validate_sale_compliance(
        ticker, 
        shares, 
        outstanding, 
        vol, 
        open_date,
        is_affiliate=True
    )
    
    # ... (Keep existing print logic if generic, or simplify/rewrite for consistency)
    
    print("\n" + "="*50)
    print(f"        RULE 144 VOLUME AUDIT: {ticker}")
    print("="*50)
    print(f"Proposed Sale:       {shares:,} shares")
    print(f"Outstanding Shares:  {outstanding:,}")
    print(f"Avg Weekly Volume:   {vol:,}")
    print("-" * 50)
    
    status = "[PASS]" if res["compliant"] else "[FAIL]"
    print(f"COMPLIANCE STATUS:   {status}")
    
    if not res["compliant"]:
        print(f"REASON: {res['reason']}")
    else:
        print(f"MSG: {res['msg']}")
        limits = res["volume_details"]
        print(f"Max Sellable:        {limits['max_sellable_volume']:,}")
    print("="*50 + "\n")

def audit_insider(ticker: str):
    """
    CLI Handler for checking Rule 144 limits based on LIVE data.
    """
    print(f"\n[*] Auditing insider limits for {ticker} using LIVE market data...")
    scraper = SECScraper()
    try:
        data = scraper.get_financials(ticker)
        outstanding = data.get('shares_outstanding', 0)
        avg_vol = data.get('average_volume', 0)
        
        if outstanding == 0:
            print("[ERROR] Could not fetch share data. Check ticker.")
            return

        svc = InsiderTradingService()
        limits = svc.calculate_sellable_volume(ticker, outstanding, avg_vol)
        
        print("\n" + "="*50)
        print(f"       LIVE RULE 144 LIMITS: ${ticker}")
        print("="*50)
        print(f"Outstanding Shares: {outstanding:,}")
        print(f"Avg Weekly Volume:  {avg_vol:,}")
        print("-" * 50)
        print(f"1% Cap:             {limits['one_percent_limit']:,}")
        print(f"Volume Cap:         {limits['avg_weekly_volume']:,}")
        print(f">> MAX SELLABLE:    {limits['max_sellable_volume']:,}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to audit {ticker}: {e}")

def scan_anomalies():
    """
    CLI Handler for scanning watchlist for pump-and-dump anomalies.
    """
    from services.market.anomaly_detector_svc import AnomalyDetectorService
    
    svc = AnomalyDetectorService()
    # Real tickers for E2E
    watchlist = ["MSFT", "TSLA", "GME", "AMC", "SPY", "NVDA"]
    print(f"\n[*] Scanning {len(watchlist)} tickers for anomalies using LIVE data...")
    
    results = svc.scan_watchlist(watchlist)
    
    print("\n" + "="*50)
    print("          ANOMALY DETECTION REPORT")
    print("="*50)
    
    found = False
    for ticker, res in results.items():
        if res.get('is_anomalous'):
            found = True
            print(f"[ALERT] {ticker}: {res['anomaly_type']} (Score: {res['divergence_score']})")
        
        # Verbose for verify
        if not res.get('is_anomalous') and 'error' not in res:
             print(f"[OK] {ticker}: Score {res.get('divergence_score', 0)} - {res.get('risk_level', 'LOW')}")
        elif 'error' in res:
             print(f"[ERR] {ticker}: {res['error']}")
            
    if not found:
        print("-" * 50)
        print("[CLEAR] No critical anomalies detected.")
        
    print("="*50 + "\n")

def check_bots(ticker: str):
    """
    CLI Handler for checking social bot activity for a ticker.
    """
    from services.social.bot_monitor_svc import BotMonitorService
    
    svc = BotMonitorService()
    print(f"\n[*] Analyzing social stream for ${ticker}...")
    
    # Simulate fetch count
    res = svc.analyze_ticker(ticker)
    
    print("\n" + "="*50)
    print(f"          BOT ACTIVITY REPORT: ${ticker}")
    print("="*50)
    print(f"Total Mentions:   {res['total_mentions']}")
    print(f"Unique Authors:   {res['unique_authors']}")
    print(f"Bot Probability:  {res['bot_probability'] * 100:.1f}%")
    print("-" * 50)
    
    status = "CRITICAL" if res['is_attack'] else "NORMAL"
    print(f"STATUS:           {status}")
    
    if res['is_attack']:
        print(f"[!] WARNING: High probability of coordinated bot attack.")
        
    print("="*50 + "\n")
