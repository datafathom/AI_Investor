"""
==============================================================================
FILE: services/payments/square_service.py
ROLE: Square Payment Processing Service
PURPOSE: Interfaces with Square for merchant payment processing, customer
         management, and catalog sync. Supports in-person and online transactions
         for future retail kiosk support.

INTEGRATION POINTS:
    - SquareAPI: Payment processing endpoints
    - CatalogSyncService: Bidirectional catalog synchronization
    - UserService: Customer profile linking
    - SquareStatsWidget: Admin dashboard statistics

AUTHOR: AI Investor Team
CREATED: 2026-01-22
UPDATED: 2026-01-21 (Enhanced for Phase 14)
==============================================================================
"""

import logging
import asyncio
import uuid
import datetime
from datetime import timezone
import random
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SquareClient:
    """
    Client for Square API.
    Currently defaults to MOCK MODE as per Phase 15 requirements.
    """
    def __init__(self, access_token: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.access_token = access_token
        # TODO: Initialize live Square client here

    async def get_merchant_stats(self, merchant_id: str = "default") -> Dict[str, Any]:
        """
        Get daily sales statistics for the merchant.
        """
        if self.mock:
            await asyncio.sleep(0.6)
            # Simulate some fluctuating daily sales
            today_sales = round(random.uniform(1500.00, 5000.00), 2)
            txn_count = int(today_sales / random.uniform(20, 100))
            return {
                "merchant_id": merchant_id,
                "date": datetime.date.today().isoformat(),
                "gross_sales_money": {
                    "amount": int(today_sales * 100), # Cents
                    "currency": "USD"
                },
                "transaction_count": txn_count,
                "terminal_status": "ONLINE",
                "active_locations": 3
            }
        return {}

    async def get_catalog(self) -> List[Dict[str, Any]]:
        """
        Get product catalog.
        """
        if self.mock:
            await asyncio.sleep(0.4)
            return [
                {"id": "ITEM_1", "name": "AI Investor Pro (Monthly)", "price": 2900,
                 "currency": "USD"},
                {"id": "ITEM_2", "name": "Consultation Hour", "price": 15000, "currency": "USD"},
                {"id": "ITEM_3", "name": "Hardware Wallet (Retail)", "price": 8900,
                 "currency": "USD"}
            ]
        return []

    async def process_terminal_payment(self, amount: float) -> Dict[str, Any]:
        """
        Simulate a terminal payment (e.g., from a kiosk).
        """
        if self.mock:
            await asyncio.sleep(1.5) # Terminal lag
            return {
                "id": f"SQ_TERM_{uuid.uuid4().hex[:12]}",
                "status": "COMPLETED",
                "amount_money": {
                    "amount": int(amount * 100),
                    "currency": "USD"
                },
                "source_type": "CARD_PRESENT",
                "emv_auth_data": "mock_emv_data"
            }
        return {}
    
    async def create_payment(
        self,
        source_id: str,
        amount: float,
        currency: str = "USD",
        customer_id: Optional[str] = None,
        reference_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create payment with source ID from Square SDK.
        
        Args:
            source_id: Payment source ID from Square SDK
            amount: Payment amount
            currency: Currency code
            customer_id: Optional customer ID
            reference_id: Optional reference ID for tracking
            
        Returns:
            Payment result dict
        """
        _ = source_id  # Unused in mock mode
        if self.mock:
            await asyncio.sleep(0.8)
            return {
                "id": f"SQ_PAY_{uuid.uuid4().hex[:12]}",
                "status": "COMPLETED",
                "amount_money": {
                    "amount": int(amount * 100),
                    "currency": currency
                },
                "source_type": "CARD",
                "customer_id": customer_id,
                "reference_id": reference_id,
                "created_at": datetime.datetime.now(timezone.utc).isoformat()
            }
        return {}
    
    async def create_customer(
        self,
        email: str,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        reference_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create customer profile and link to platform user.
        
        Args:
            email: Customer email
            given_name: First name
            family_name: Last name
            phone_number: Phone number
            reference_id: Platform user ID for linking
            
        Returns:
            Customer dict with ID
        """
        if self.mock:
            await asyncio.sleep(0.5)
            return {
                "id": f"SQ_CUST_{uuid.uuid4().hex[:12]}",
                "email_address": email,
                "given_name": given_name,
                "family_name": family_name,
                "phone_number": phone_number,
                "reference_id": reference_id,
                "created_at": datetime.datetime.now(timezone.utc).isoformat()
            }
        return {}
    
    async def get_transactions(
        self,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        location_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get transaction history.
        
        Args:
            start_date: Start date for query
            end_date: End date for query
            location_id: Optional location filter
            
        Returns:
            List of transaction dicts
        """
        if self.mock:
            await asyncio.sleep(0.6)
            # Generate mock transactions
            transactions = []
            _ = (start_date, end_date)  # Unused in mock mode
            if not start_date:
                start_date = datetime.date.today() - datetime.timedelta(days=7)
            if not end_date:
                end_date = datetime.date.today()

            for _ in range(random.randint(5, 20)):
                transactions.append({
                    "id": f"SQ_TXN_{uuid.uuid4().hex[:12]}",
                    "status": "COMPLETED",
                    "amount_money": {
                        "amount": random.randint(1000, 50000),
                        "currency": "USD"
                    },
                    "created_at": (datetime.datetime.now() -
                                  datetime.timedelta(days=random.randint(0, 7))).isoformat(),
                    "location_id": location_id or "default_location"
                })

            return transactions
        return []
    
    async def get_refunds(
        self,
        _start_date: Optional[datetime.date] = None,
        _end_date: Optional[datetime.date] = None
    ) -> List[Dict[datetime.date, Any]]:
        """
        Get refund history.
        
        Args:
            start_date: Start date for query
            end_date: End date for query
            
        Returns:
            List of refund dicts
        """
        if self.mock:
            await asyncio.sleep(0.4)
            return [
                {
                    "id": f"SQ_REF_{uuid.uuid4().hex[:12]}",
                    "amount_money": {
                        "amount": random.randint(500, 5000),
                        "currency": "USD"
                    },
                    "status": "COMPLETED",
                    "created_at": (datetime.datetime.now() -
                                  datetime.timedelta(days=random.randint(1, 30))).isoformat()
                }
            ]
        return []

class SquareClientSingleton:
    """Singleton wrapper for SquareClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> SquareClient:
        """Returns the singleton instance of SquareClient."""
        if cls._instance is None:
            cls._instance = SquareClient(mock=mock)
        return cls._instance

def get_square_client(mock: bool = True) -> SquareClient:
    """Legacy helper to get the square client instance."""
    return SquareClientSingleton.get_instance(mock=mock)
