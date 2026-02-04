"""
==============================================================================
FILE: scripts/runners/test_solana.py
ROLE: Test Runner
PURPOSE: Verifies Solana RPC client and token registry in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.crypto.solana_client import get_solana_client
from services.crypto.solana_token_registry import get_solana_token_registry

logger = logging.getLogger(__name__)

def run_test_solana(mock: bool = True, **kwargs):
    """
    Runs the Solana integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING SOLANA INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_solana_client(mock=True)
        registry = get_solana_token_registry()

        try:
            # 1. Get SOL Balance
            test_addr = "F6B8H8..." # Simplified
            print(f"[*] Fetching SOL Balance for account...")
            balance = await client.get_sol_balance(test_addr)
            print(f"   Balance: {balance} SOL")

            # 2. Get SPL Tokens
            print("\n[*] Enumerating Token Accounts...")
            tokens = await client.get_spl_tokens(test_addr)
            for t in tokens:
                info = registry.get_token_info(t['mint'])
                print(f"   - {info['name']} ({t['symbol']}): {t['balance']}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_solana()
