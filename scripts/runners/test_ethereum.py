"""
==============================================================================
FILE: scripts/runners/test_ethereum.py
ROLE: Test Runner
PURPOSE: Verifies Ethereum RPC client and wallet service in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.crypto.ethereum_client import get_eth_client
from services.crypto.wallet_service import get_wallet_service

logger = logging.getLogger(__name__)

def run_test_ethereum(mock: bool = True, **kwargs):
    """
    Runs the Ethereum integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING ETHEREUM INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_eth_client(mock=True)
        wallet_service = get_wallet_service()

        try:
            # 1. Get ETH Balance
            test_addr = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
            print(f"[*] Fetching ETH Balance for {test_addr}...")
            balance = await client.get_eth_balance(test_addr)
            print(f"   Balance: {balance} ETH")

            # 2. Get Token Balance
            usdt_addr = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
            print(f"\n[*] Fetching USDT Balance for {test_addr}...")
            token_res = await client.get_token_balance(test_addr, usdt_addr)
            print(f"   {token_res['symbol']}: {token_res['balance']}")

            # 3. Add to Wallet Service
            print("\n[*] Adding wallet to WalletService...")
            wallet_res = await wallet_service.add_wallet(test_addr)
            print(f"   Status: Success (Chain: {wallet_res['chain']})")

            # 4. Get Gas Price
            gas = await client.get_gas_price()
            print(f"\n[*] Current Gas Estimate: {gas} Gwei")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_ethereum()
