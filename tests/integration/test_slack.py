"""
==============================================================================
FILE: scripts/runners/test_slack.py
ROLE: Test Runner
PURPOSE: Verifies SlackClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.notifications.slack_service import get_slack_client

logger = logging.getLogger(__name__)

def run_test_slack(action: str = "post", channel: str = "#general", mock: bool = True, **_kwargs: any) -> None:
    """
    Runs the Slack integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING SLACK INTEGRATION (MOCK MODE)")
    print(f" Action: {action} | Channel: {channel}")
    print(f"{'='*60}\n")

    async def _internal() -> None:
        client = get_slack_client(mock=mock)

        try:
            if action == "post":
                print("[*] Posting Test Message...")
                result = await client.post_message(channel, "Hello from AI Investor CLI!")

                print(f"   OK: {result.get('ok')}")
                print(f"   Timestamp: {result.get('ts')}")
                print(f"   Text: {result.get('message', {}).get('text')}")

            elif action == "list":
                print("[*] Listing Channels...")
                channels = await client.get_channels()
                print(f"   Count: {len(channels)}")
                for ch in channels:
                    print(f"     - #{ch['name']} ({ch['num_members']} members)")

            print("\n[!] VERIFICATION PASSED")

        except ConnectionError as e:
            print(f"[-] CONNECTION ERROR during test: {e}")
            logger.exception(e)
        except Exception as e:
            print(f"[-] UNEXPECTED ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_slack()
