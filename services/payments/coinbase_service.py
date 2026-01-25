"""
==============================================================================
FILE: services/payments/coinbase_service.py
ROLE: Crypto Wallet Client
PURPOSE: Interfaces with Coinbase for wallet linking and balance checks.
         
INTEGRATION POINTS:
    - CoinbaseAPI: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
import random
import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CoinbaseClient:
    """
    Client for Coinbase API.
    Currently defaults to MOCK MODE as per Phase 17 requirements.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        self.api_secret = api_secret
        # TODO: Initialize live Coinbase client here

    async def connect_wallet(self, user_id: str) -> Dict[str, Any]:
        """
        Simulate OAuth connection to Coinbase.
        """
        if self.mock:
            await asyncio.sleep(0.8)
            return {
                "status": "connected",
                "wallet_id": f"cb_wallet_{uuid.uuid4().hex[:16]}",
                "user_id": user_id,
                "connected_at": datetime.datetime.utcnow().isoformat()
            }
        return {}

    async def get_wallet_balance(self) -> Dict[str, Any]:
        """
        Fetch crypto balances.
        """
        if self.mock:
            await asyncio.sleep(0.6)
            return {
                "total_balance_usd": 14520.50,
                "assets": [
                    {
                        "currency": "BTC",
                        "name": "Bitcoin",
                        "amount": 0.15,
                        "price_usd": 65000.00,
                        "value_usd": 9750.00
                    },
                    {
                        "currency": "ETH",
                        "name": "Ethereum",
                        "amount": 1.25,
                        "price_usd": 3200.00,
                        "value_usd": 4000.00
                    },
                    {
                        "currency": "SOL",
                        "name": "Solana",
                        "amount": 5.50,
                        "price_usd": 140.00,
                        "value_usd": 770.00
                    },
                    {
                        "currency": "USDC",
                        "name": "USD Coin",
                        "amount": 0.50,
                        "price_usd": 1.00,
                        "value_usd": 0.50
                    }
                ]
            }
        return {"total_balance_usd": 0.0, "assets": []}

    async def get_transactions(self) -> List[Dict[str, Any]]:
        """
        Fetch recent transactions.
        """
        if self.mock:
            await asyncio.sleep(0.5)
            return [
                {
                    "id": f"tx_{uuid.uuid4().hex[:8]}",
                    "type": "buy",
                    "amount": {"amount": "0.05", "currency": "BTC"},
                    "native_amount": {"amount": "3250.00", "currency": "USD"},
                    "status": "completed",
                    "created_at": (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()
                },
                {
                    "id": f"tx_{uuid.uuid4().hex[:8]}",
                    "type": "sell",
                    "amount": {"amount": "2.00", "currency": "SOL"},
                    "native_amount": {"amount": "280.00", "currency": "USD"},
                    "status": "completed",
                    "created_at": (datetime.datetime.utcnow() - datetime.timedelta(days=3)).isoformat()
                }
            ]
        return []

_instance = None

def get_coinbase_client(mock: bool = True) -> CoinbaseClient:
    global _instance
    if _instance is None:
        _instance = CoinbaseClient(mock=mock)
    return _instance
