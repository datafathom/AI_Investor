"""
==============================================================================
FILE: services/payments/paypal_service.py
ROLE: Payment Gateway Client
PURPOSE: Interfaces with PayPal or Mock for order creation and capture.
         
INTEGRATION POINTS:
    - PayPalAPI: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PayPalClient:
    """
    Client for PayPal API.
    Currently defaults to MOCK MODE as per Phase 13 requirements.
    """
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.client_id = client_id
        self.client_secret = client_secret
        # TODO: Initialize live PayPal SDK client here

    async def create_order(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        """
        Creates a payment order.
        """
        _ = (amount, currency)  # Unused in mock mode
        if self.mock:
            await asyncio.sleep(0.7)
            order_id = f"PAYPAL_MOCK_ORDER_{uuid.uuid4().hex[:12]}"
            return {
                "id": order_id,
                "status": "CREATED",
                "links": [
                    {
                        "href": f"https://www.sandbox.paypal.com/checkoutnow?token={order_id}",
                        "rel": "approve",
                        "method": "GET"
                    }
                ]
            }
        return {}

    async def capture_order(self, order_id: str) -> Dict[str, Any]:
        """
        Captures payment for an order.
        """
        if self.mock:
            await asyncio.sleep(0.8)
            transaction_id = f"TXN_{uuid.uuid4().hex[:16]}"
            return {
                "id": order_id,
                "status": "COMPLETED",
                "purchase_units": [
                    {
                        "payments": {
                            "captures": [
                                {
                                    "id": transaction_id,
                                    "status": "COMPLETED",
                                    "amount": {
                                        "currency_code": "USD",
                                        "value": "29.00"
                                    },
                                    "final_capture": True
                                }
                            ]
                        }
                    }
                ]
            }
        return {}

class PayPalClientSingleton:
    """Singleton wrapper for PayPalClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> PayPalClient:
        """Returns the singleton instance of PayPalClient."""
        if cls._instance is None:
            cls._instance = PayPalClient(mock=mock)
        return cls._instance

def get_paypal_client(mock: bool = True) -> PayPalClient:
    """Legacy helper to get the paypal client instance."""
    return PayPalClientSingleton.get_instance(mock=mock)
