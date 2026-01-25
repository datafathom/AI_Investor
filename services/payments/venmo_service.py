"""
==============================================================================
FILE: services/payments/venmo_service.py
ROLE: Payment Gateway Client
PURPOSE: Interfaces with Venmo (via PayPal SDK or Direct) for mobile payments.
         
INTEGRATION POINTS:
    - VenmoAPI: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VenmoClient:
    """
    Client for Venmo API.
    Currently defaults to MOCK MODE as per Phase 14 requirements.
    """
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # TODO: Initialize live Venmo/Braintree client here

    async def process_payment(self, amount: float, username: str = "current_user",
                              currency: str = "USD") -> Dict[str, Any]:
        """
        Process a P2P payment request.
        """
        if self.mock:
            await asyncio.sleep(1.2) # Simulate mobile app switch delay
            txn_id = f"VENMO_TXN_{uuid.uuid4().hex[:16]}"

            # Simulate random success/failure if needed, but keeping it success for demo
            return {
                "id": txn_id,
                "status": "SETTLED",
                "amount": f"{amount:.2f}",
                "currency": currency,
                "payer": {
                    "username": f"@{username}",
                    "display_name": "Mock User"
                },
                "payment_method": "VENMO_BALANCE",
                "note": "AI Investor Pro Subscription"
            }

        return {}

class VenmoClientSingleton:
    """Singleton wrapper for VenmoClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> VenmoClient:
        """Returns the singleton instance of VenmoClient."""
        if cls._instance is None:
            cls._instance = VenmoClient(mock=mock)
        return cls._instance

def get_venmo_client(mock: bool = True) -> VenmoClient:
    """Legacy helper to get the venmo client instance."""
    return VenmoClientSingleton.get_instance(mock=mock)
