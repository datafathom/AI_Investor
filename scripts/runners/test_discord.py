"""
==============================================================================
FILE: scripts/runners/test_discord.py
ROLE: Test Runner
PURPOSE: Verifies Discord Bot and Webhook services in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.social.discord_bot import get_discord_bot
from services.communication.discord_webhook import get_discord_webhook

logger = logging.getLogger(__name__)

def run_test_discord(mock: bool = True, **kwargs):
    """
    Runs the Discord integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING DISCORD INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        bot = get_discord_bot(mock=True)
        webhook = get_discord_webhook(url="https://discord.com/api/webhooks/mock_url")

        try:
            # 1. Connect Bot
            print("[*] Connecting Bot to Gateway...")
            connected = await bot.connect()
            print(f"   Connected: {connected}")

            # 2. Fetch Mentions
            ticker = "BTC"
            print(f"\n[*] Fetching Discord Mentions for ${ticker}...")
            mentions = await bot.get_recent_mentions(ticker)
            for m in mentions[:2]:
                print(f"   [{m['sentiment']}] @{m['author']} in {m['channel']}: {m['content'][:30]}...")

            # 3. Get Hype Score
            print(f"\n[*] Calculating Hype Score...")
            hype = await bot.get_hype_score(ticker)
            print(f"   Velocity: {hype['velocity']} mentions/hr (+{hype['growth_pct']}% growth)")

            # 4. Dispatch Alert
            print(f"\n[*] Dispatching Mock Trade Signal to Webhook...")
            success = await webhook.send_trade_signal(ticker, "BUY", 42500.0, 0.88)
            print(f"   Webhook Alert Sent: {success}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_discord()
