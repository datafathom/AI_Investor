
from services.analysis.morning_briefing import get_briefing_service
from services.communication.notification_manager import get_notification_manager, AlertPriority

def run_test_briefing(args=None):
    """
    Test Phase 29 Morning Briefing Generation.
    """
    print("Testing Morning Briefing Service...")
    
    briefing_service = get_briefing_service()
    
    # Scene 1: Panic Mode
    print("\n--- SCENARIO: MARKET CRASH (Fear 10) ---")
    report_panic = briefing_service.generate_briefing(
        user_name="Mr. Anderson",
        portfolio_value=95000.00,
        fear_index=10,
        market_sentiment="BEARISH"
    )
    print(report_panic)
    
    # Scene 2: Greed Mode
    print("\n--- SCENARIO: BULL RUN (Greed 90) ---")
    report_greed = briefing_service.generate_briefing(
        user_name="Mr. Anderson",
        portfolio_value=125000.00,
        fear_index=90,
        market_sentiment="BULLISH"
    )
    print(report_greed)
    
    # Test Alert System
    print("\n--- Testing Alert Notification ---")
    notifier = get_notification_manager()
    notifier.send_alert("Test Critical Alert", AlertPriority.CRITICAL)
    print("✅ Notification sent to mock channels.")
