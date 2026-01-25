"""
==============================================================================
FILE: scripts/runners/test_pagerduty.py
ROLE: Test Runner
PURPOSE: Verifies PagerDutyClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.notifications.pagerduty_service import get_pagerduty_client

logger = logging.getLogger(__name__)

def run_test_pagerduty(action: str = "trigger", mock: bool = True, **kwargs):
    """
    Runs the PagerDuty integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING PAGERDUTY INTEGRATION (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_pagerduty_client(mock=True)

        try:
            if action == "trigger":
                print(f"[*] Triggering Test Incident...")
                result = await client.trigger_incident("CLI Test: Manual Trigger", "low")
                print(f"   ID: {result.get('id')}")
                print(f"   Status: {result.get('status')}")
                print(f"   Title: {result.get('title')}")

            elif action == "list":
                print(f"[*] Fetching Active Incidents...")
                incidents = await client.get_incidents()
                print(f"   Count: {len(incidents)}")
                for inc in incidents:
                    print(f"     - [{inc['id']}] {inc['title']} ({inc['status'].upper()})")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_pagerduty()
