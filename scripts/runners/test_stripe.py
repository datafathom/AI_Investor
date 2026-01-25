"""
==============================================================================
FILE: scripts/runners/test_stripe.py
ROLE: Test Runner
PURPOSE: Verifies StripeClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.payments.stripe_service import get_stripe_client

logger = logging.getLogger(__name__)

def run_test_stripe(action: str = "checkout", **_kwargs):
    """
    Runs the Stripe Billing test.
    """
    print(f"\n{'='*60}")
    print(" TESTING STRIPE BILLING (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_stripe_client(mock=True)

        try:
            if action == "checkout":
                print("[*] Creating Checkout Session...")
                result = await client.create_checkout_session("user_test", "price_pro_monthly")
                print(f"   Success! Session ID: {result['id']}")
                print(f"   URL: {result['url']}")

            elif action == "subscription":
                print("[*] Fetching Subscription...")
                result = await client.get_subscription("user_test")
                print(f"   Status: {result['status']}")
                print(f"   Plan: {result['plan']['name']} ({result['plan']['amount']} {result['plan']['currency']})")
                print(f"   Renews: {result['current_period_end']}")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_stripe()
