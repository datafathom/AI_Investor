"""
==============================================================================
FILE: services/payments/plaid_service.py
ROLE: Bank Integration Client
PURPOSE: Interfaces with Plaid for linking bank accounts and fetching balances.
         
INTEGRATION POINTS:
    - PlaidAPI: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
import random
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PlaidClient:
    """
    Client for Plaid API.
    Currently defaults to MOCK MODE as per Phase 16 requirements.
    """
    
    def __init__(self, client_id: Optional[str] = None, secret: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.client_id = client_id
        self.secret = secret
        # TODO: Initialize live Plaid client here

    async def create_link_token(self, user_id: str) -> Dict[str, Any]:
        """
        Create a Link Token to initialize Plaid Link.
        """
        if self.mock:
            await asyncio.sleep(0.5)
            link_token = f"link-sandbox-{uuid.uuid4().hex[:16]}"
            return {
                "link_token": link_token,
                "expiration": "2026-01-23T00:00:00Z",
                "request_id": f"req_{uuid.uuid4().hex[:8]}"
            }
        return {}

    async def exchange_public_token(self, public_token: str) -> Dict[str, Any]:
        """
        Exchange public_token for access_token.
        """
        if self.mock:
            await asyncio.sleep(0.8)
            # In mock mode, we just return a sandbox access token
            return {
                "access_token": f"access-sandbox-{uuid.uuid4().hex[:24]}",
                "item_id": f"item_{uuid.uuid4().hex[:8]}",
                "request_id": f"req_{uuid.uuid4().hex[:8]}"
            }
        return {}

    async def get_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Fetch accounts and balances.
        """
        if self.mock:
            await asyncio.sleep(1.0)
            return [
                {
                    "account_id": f"acc_{uuid.uuid4().hex[:8]}",
                    "name": "Plaid Checking",
                    "mask": "0000",
                    "type": "depository",
                    "subtype": "checking",
                    "balances": {
                        "available": 1100.50,
                        "current": 1100.50,
                        "iso_currency_code": "USD"
                    }
                },
                {
                    "account_id": f"acc_{uuid.uuid4().hex[:8]}",
                    "name": "Plaid Savings",
                    "mask": "1111",
                    "type": "depository",
                    "subtype": "savings",
                    "balances": {
                        "available": 23000.00,
                        "current": 23000.00,
                        "iso_currency_code": "USD"
                    }
                }
            ]
        return []

_instance = None

def get_plaid_client(mock: bool = True) -> PlaidClient:
    global _instance
    if _instance is None:
        _instance = PlaidClient(mock=mock)
    return _instance
