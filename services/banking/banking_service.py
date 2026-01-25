import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Attempt to import plaid, but handle missing dependency for flexibility
try:
    import plaid
    from plaid.api import plaid_api
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.products import Products
    from plaid.model.country_code import CountryCode
except ImportError:
    plaid = None

from services.system.secret_manager import get_secret_manager

class BankingService:
    """
    Service for interfacing with the Plaid API to link bank accounts and sync transactions.
    Supports a 'Simulation Mode' if Plaid credentials are not configured.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BankingService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self) -> None:
        self.logger = logging.getLogger(__name__)
        sm = get_secret_manager()
        
        self.client_id = sm.get_secret("PLAID_CLIENT_ID")
        self.secret = sm.get_secret("PLAID_SECRET")
        self.env = sm.get_secret("PLAID_ENV", "sandbox")
        
        self.is_simulated = not (self.client_id and self.secret) and (plaid is not None)
        # Force simulation if plaid library is missing
        if plaid is None:
            self.is_simulated = True
            self.logger.warning("Plaid library missing. BankingService running in Force Simulation Mode.")
        
        if not self.is_simulated:
            configuration = plaid.Configuration(
                host=plaid.Environment.Sandbox if self.env == "sandbox" else plaid.Environment.Development,
                api_key={
                    'clientId': self.client_id,
                    'secret': self.secret,
                }
            )
            api_client = plaid.ApiClient(configuration)
            self.client = plaid_api.PlaidApi(api_client)
            self.logger.info(f"BankingService initialized (Plaid {self.env}).")
        else:
            self.logger.info("BankingService initialized (Simulation Mode).")

    def create_link_token(self, user_id: str) -> str:
        """Generates a Plaid Link Token to initiate the connection flow."""
        if self.is_simulated:
            return "sim_link_token_12345"

        try:
            request = LinkTokenCreateRequest(
                products=[Products('transactions')],
                client_name="AI Investor",
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=user_id)
            )
            response = self.client.link_token_create(request)
            return response['link_token']
        except Exception as e:
            self.logger.error(f"Failed to create Plaid link token: {e}")
            raise

    def exchange_public_token(self, public_token: str) -> str:
        """Exchanges a public token for a permanent access token."""
        if self.is_simulated:
            self.logger.info(f"Simulated token exchange for: {public_token}")
            return "sim_access_token_67890"

        try:
            from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response['access_token']
        except Exception as e:
            self.logger.error(f"Failed to exchange public token: {e}")
            raise

    def get_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """Retrieves linked accounts for an access token."""
        if self.is_simulated:
            return [
                {"id": "acc_1", "name": "Main Checking", "balance": 15420.50, "type": "depository"},
                {"id": "acc_2", "name": "Savings", "balance": 45000.00, "type": "depository"},
                {"id": "acc_3", "name": "Venture Card", "balance": -1200.40, "type": "credit"}
            ]

        try:
            from plaid.model.accounts_get_request import AccountsGetRequest
            request = AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            return [
                {
                    "id": acc.account_id,
                    "name": acc.name,
                    "balance": acc.balances.current,
                    "type": str(acc.type)
                } for acc in response['accounts']
            ]
        except Exception as e:
            self.logger.error(f"Failed to fetch accounts: {e}")
            return []

# Global Accessor
def get_banking_service() -> BankingService:
    return BankingService()
