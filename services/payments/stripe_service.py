"""
==============================================================================
FILE: services/payments/stripe_service.py
ROLE: Payment Gateway Client
PURPOSE: Interfaces with Stripe or Mock for subscription billing and
         checkout sessions.
         
INTEGRATION POINTS:
    - UserService: Used to link Stripe Customer IDs to users.
    - StripeAPI: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class StripeClient:
    """
    Client for Stripe API.
    Currently defaults to MOCK MODE as per Phase 12 requirements.
    """
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # TODO: Initialize live Stripe client here

    async def create_checkout_session(self, user_id: str, plan_id: str) -> Dict[str, Any]:
        """
        Creates a checkout session for a subscription.
        """
        if self.mock:
            await asyncio.sleep(0.8)
            session_id = f"cs_test_{uuid.uuid4().hex[:16]}"
            return {
                "id": session_id,
                "url": f"https://checkout.stripe.mock/pay/{session_id}?user={user_id}&plan={plan_id}",
                "status": "open"
            }
        return {}

    async def get_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        Gets the current subscription status for a user.
        """
        _ = user_id  # Unused in mock mode
        if self.mock:
            await asyncio.sleep(0.5)
            # Default to FREE for now, or random for testing
            return {
                "status": "active",
                "plan": {
                    "id": "price_free_tier",
                    "name": "Free Tier",
                    "amount": 0,
                    "currency": "usd"
                },
                "current_period_end": (datetime.datetime.now() +
                                      datetime.timedelta(days=30)).isoformat()
            }
        return {}

    async def cancel_subscription(self, subscription_id: str) -> bool:
        """
        Cancels a subscription.
        """
        _ = subscription_id  # Unused in mock mode
        if self.mock:
            await asyncio.sleep(1.0)
            return True
        return False

class StripeClientSingleton:
    """Singleton wrapper for StripeClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> StripeClient:
        """Returns the singleton instance of StripeClient."""
        if cls._instance is None:
            cls._instance = StripeClient(mock=mock)
        return cls._instance

def get_stripe_client(mock: bool = True) -> StripeClient:
    """Legacy helper to get the stripe client instance."""
    return StripeClientSingleton.get_instance(mock=mock)
