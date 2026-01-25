"""
==============================================================================
FILE: services/crypto/solana_client.py
ROLE: Solana RPC Client
PURPOSE: Fetches SOL and SPL token balances from Solana network. Provides
         wallet health checks and transaction history parsing.

INTEGRATION POINTS:
    - WalletService: Solana wallet portfolio sync
    - SolanaTokenRegistry: Token metadata lookup
    - PortfolioAggregator: SPL token aggregation

AUTHOR: AI Investor Team
CREATED: 2026-01-22
UPDATED: 2026-01-21 (Enhanced for Phase 25)
==============================================================================
"""

import logging
import asyncio
import random
import uuid
from typing import Dict, Any, List, Optional
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class SolanaClient:
    """
    Client for Solana RPC.
    Defaults to MOCK MODE for Phase 25.
    """
    
    def __init__(self, rpc_url: Optional[str] = None, mock: bool = True):
        self.mock = mock
        sm = get_secret_manager()
        self.rpc_url = rpc_url or sm.get_secret('SOL_RPC_URL', 'https://api.mainnet-beta.solana.com')

    async def get_sol_balance(self, address: str) -> float:
        """Get SOL balance for an address."""
        if self.mock:
            await asyncio.sleep(0.3)
            # Mock balance between 1 and 200 SOL
            return round(random.uniform(1.0, 200.0), 4)
        return 0.0

    async def get_spl_tokens(self, address: str) -> List[Dict[str, Any]]:
        """
        List SPL tokens for an address with metadata.
        
        Args:
            address: Solana wallet address
            
        Returns:
            List of SPL token dicts with balances and metadata
        """
        if self.mock:
            await asyncio.sleep(0.4)
            return [
                {
                    "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", # USDC
                    "symbol": "USDC",
                    "name": "USD Coin",
                    "balance": round(random.uniform(50.0, 1000.0), 2),
                    "decimals": 6,
                    "logo_uri": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v/logo.png"
                },
                {
                    "mint": "DezXAZ8z7PnrnMcqzR2S6Pb9k8i6yT2ccWU6Ykcr98J3", # BONK
                    "symbol": "BONK",
                    "name": "Bonk",
                    "balance": round(random.uniform(100000.0, 10000000.0), 0),
                    "decimals": 5,
                    "logo_uri": None
                },
                {
                    "mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", # USDT
                    "symbol": "USDT",
                    "name": "Tether USD",
                    "balance": round(random.uniform(10.0, 500.0), 2),
                    "decimals": 6,
                    "logo_uri": None
                }
            ]
        return []
    
    async def get_transaction_history(
        self,
        address: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get transaction history with parsed instructions.
        
        Args:
            address: Solana wallet address
            limit: Maximum transactions to return
            
        Returns:
            List of transaction dicts
        """
        if self.mock:
            await asyncio.sleep(0.3)
            return [
                {
                    "signature": f"mock_tx_{uuid.uuid4().hex[:16]}",
                    "block_time": asyncio.get_event_loop().time() - 3600,
                    "fee": 0.000005,
                    "instructions": [
                        {
                            "type": "transfer",
                            "amount": 1.5,
                            "currency": "SOL"
                        }
                    ]
                }
            ]
        return []
    
    def validate_address(self, address: str) -> bool:
        """
        Validate Solana address format (base58, 32-44 chars).
        
        Args:
            address: Address to validate
            
        Returns:
            True if valid format
        """
        if not address:
            return False
        
        # Basic validation: base58, 32-44 chars
        if len(address) < 32 or len(address) > 44:
            return False
        
        # Check for base58 characters (no 0, O, I, l)
        invalid_chars = ['0', 'O', 'I', 'l']
        if any(c in address for c in invalid_chars):
            return False
        
        return True

_instance = None

def get_solana_client(mock: bool = True) -> SolanaClient:
    global _instance
    if _instance is None:
        _instance = SolanaClient(mock=mock)
    return _instance
