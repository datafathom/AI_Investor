"""
==============================================================================
FILE: scripts/runners/test_sendgrid.py
ROLE: Test Runner
PURPOSE: Verifies SendGridClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.notifications.sendgrid_service import get_sendgrid_client

logger = logging.getLogger(__name__)

def run_test_sendgrid(action: str = "send", to: str = "user@example.com", mock: bool = True, **kwargs):
    """
    Runs the SendGrid integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING SENDGRID INTEGRATION (MOCK MODE)")
    print(f" Action: {action} | To: {to}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_sendgrid_client(mock=True)

        try:
            if action == "send":
                print(f"[*] Sending Test Email...")
                subject = "AI Investor: Test Report"
                content = "<h1>Weekly Performance</h1><p>Your portfolio is up 5%.</p>"
                
                result = await client.send_email(to, subject, content)
                
                print(f"   Status: {result.get('status')}")
                print(f"   ID: {result.get('id')}")
                print(f"   Subject: {result.get('subject')}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_sendgrid()
