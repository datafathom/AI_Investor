"""
==============================================================================
FILE: services/crypto/solana_token_registry.py
ROLE: Solana Token Registry Service
PURPOSE: Maintains registry of SPL token metadata (name, symbol, decimals,
         logo) for display in portfolio. Updates weekly from Jupiter aggregator.

INTEGRATION POINTS:
    - SolanaClient: Token metadata lookup
    - SolanaWallet: Frontend token display

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Common SPL tokens registry
COMMON_TOKENS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "logo_uri": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v/logo.png"
    },
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {
        "symbol": "USDT",
        "name": "Tether USD",
        "decimals": 6,
        "logo_uri": None
    },
    "DezXAZ8z7PnrnMcqzR2S6Pb9k8i6yT2ccWU6Ykcr98J3": {
        "symbol": "BONK",
        "name": "Bonk",
        "decimals": 5,
        "logo_uri": None
    },
    "So11111111111111111111111111111111111111112": {
        "symbol": "SOL",
        "name": "Solana",
        "decimals": 9,
        "logo_uri": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png"
    }
}


class SolanaTokenRegistry:
    """
    Registry for SPL token metadata.
    """
    
    def __init__(self, mock: bool = False):
        """
        Initialize token registry.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
        self._registry = COMMON_TOKENS.copy()
        self._last_update = datetime.now()
    
    def get_token_info(self, mint_address: str) -> Optional[Dict[str, Any]]:
        """
        Get token metadata by mint address.
        
        Args:
            mint_address: SPL token mint address
            
        Returns:
            Token metadata dict or None if not found
        """
        token_info = self._registry.get(mint_address)
        
        if token_info:
            return token_info
        
        # Fallback: return address as symbol
        return {
            "symbol": mint_address[:8] + "...",
            "name": "Unknown Token",
            "decimals": 9,  # Default
            "logo_uri": None
        }
    
    async def update_from_jupiter(self) -> bool:
        """
        Update registry from Jupiter aggregator.
        In production, fetches from Jupiter token list API.
        
        Returns:
            True if updated successfully
        """
        if self.mock:
            await asyncio.sleep(0.5)
            logger.info("[MOCK] Token registry updated from Jupiter")
            self._last_update = datetime.now()
            return True
        
        # In production:
        # 1. Fetch token list from Jupiter API
        # 2. Update registry
        # 3. Store in database/cache
        
        return False
    
    def get_all_tokens(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered tokens.
        
        Returns:
            Dict mapping mint addresses to token info
        """
        return self._registry.copy()
    
    def add_token(
        self,
        mint_address: str,
        symbol: str,
        name: str,
        decimals: int,
        logo_uri: Optional[str] = None
    ):
        """
        Add or update token in registry.
        
        Args:
            mint_address: Token mint address
            symbol: Token symbol
            name: Token name
            decimals: Token decimals
            logo_uri: Optional logo URL
        """
        self._registry[mint_address] = {
            "symbol": symbol,
            "name": name,
            "decimals": decimals,
            "logo_uri": logo_uri
        }


# Singleton instance
_token_registry: Optional[SolanaTokenRegistry] = None


def get_token_registry(mock: bool = True) -> SolanaTokenRegistry:
    """
    Get singleton token registry instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        SolanaTokenRegistry instance
    """
    global _token_registry
    
    if _token_registry is None:
        _token_registry = SolanaTokenRegistry(mock=mock)
        logger.info(f"Solana token registry initialized (mock={mock})")
    
    return _token_registry
