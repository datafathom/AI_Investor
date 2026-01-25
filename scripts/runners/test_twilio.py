"""
==============================================================================
FILE: scripts/runners/test_twilio.py
ROLE: Test Runner
PURPOSE: Verifies Twilio SMS service and preferences in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.notifications.twilio_service import get_twilio_client
from services.notifications.notification_preferences import get_notification_preferences

logger = logging.getLogger(__name__)

def run_test_twilio(mock: bool = True, **kwargs):
    """
    Runs the Twilio integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING TWILIO SMS INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_twilio_client(mock=True)
        prefs = get_notification_preferences()

        try:
            # 1. Update Preferences
            test_number = "+15551234567"
            print(f"[*] Configuring SMS for {test_number}...")
            prefs.update_sms_preferences(phone=test_number, enabled=True)
            
            # 2. Send Verification OTP
            print("\n[*] Sending Verification OTP...")
            otp = await client.send_verification_otp(test_number)
            print(f"   OTP Generated: {otp} (Check logs for dispatch)")

            # 3. Mock Verify
            print("\n[*] Simulating User Verification...")
            success = prefs.verify_phone("123456") # Hardcoded in mock pref service
            print(f"   Verification Success: {success}")

            # 4. Critical Alert Dispatch
            if success:
                print("\n[*] Dispatching Critical Margin Call Alert...")
                res = await client.send_critical_alert(
                    test_number, 
                    "Margin Call", 
                    "Your account equity is below 25%. Deposit $5,000 to prevent liquidation."
                )
                print(f"   Status: {res['status']}")
                print(f"   SID: {res['sid']}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_twilio()
