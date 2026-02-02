
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from services.system.secret_manager import get_secret_manager

from services.crypto.ethereum_client import get_eth_client

logger = logging.getLogger(__name__)

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BITCOIN = "bitcoin"
    POLYGON = "polygon"

class WalletType(str, Enum):
    METAMASK = "metamask"
    PHANTOM = "phantom"
    LEDGER = "ledger"

class Balance(BaseModel):
    token: str
    chain: Chain
    amount: float
    usd_value: float
    price: float = 0.0

class CryptoPortfolio(BaseModel):
    user_id: str
    total_usd_value: float
    balances: List[Balance]
    wallets: List[str]
    last_updated: datetime

class ConnectionStatus(BaseModel):
    connected: bool
    wallet_address: Optional[str] = None
    chain: Optional[Chain] = None

class WalletService:
    """
    Service for cross-chain crypto wallet connectivity (ETH, SOL, etc.)
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WalletService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self.eth_client = get_eth_client(mock=True) # Default to mock for Phase 24
        
        sm = get_secret_manager()
        self._eth_rpc = sm.get_secret('ETH_RPC_URL', 'https://cloudflare-eth.com')
        self._sol_rpc = sm.get_secret('SOL_RPC_URL', 'https://api.mainnet-beta.solana.com')
        self._is_simulated = True


    async def get_wallet_balance(self, address: str, chain: str) -> Optional[Balance]:
        """Get balance for a single address."""
        # For simulation, return a mock Balance
        if self._is_simulated:
             return Balance(
                 token="ETH" if chain == "ethereum" else "SOL",
                 chain=Chain(chain),
                 amount=1.5,
                 usd_value=3500.00,
                 price=2333.33
             )
        
        res = await self.get_wallet_balances([{"address": address, "chain": chain}])
        if res:
            # Convert dict to Balance if needed, but get_wallet_balances returns dicts
            r = res[0]
            return Balance(
                token=r.get("symbol", ""),
                chain=Chain(chain),
                amount=r.get("balance", 0.0),
                usd_value=r.get("value_usd", 0.0),
                price=0.0
            ) 
        return None
    
    def validate_wallet_address(self, address: str, chain: str) -> bool:
        """
        Validate wallet address format for a given chain.
        
        Args:
            address: Wallet address
            chain: Chain type (ethereum, solana)
            
        Returns:
            True if valid
        """
        if chain.lower() == "ethereum":
            from services.crypto.ethereum_client import get_eth_client
            client = get_eth_client()
            return client.validate_address(address)
        elif chain.lower() == "solana":
            from services.crypto.solana_client import get_solana_client
            client = get_solana_client()
            return client.validate_address(address)
        return False
    
    async def refresh_token_balances(self, user_id: str) -> Dict[str, Any]:
        """
        Refresh token balances for all connected wallets (hourly).
        
        Args:
            user_id: User ID
            
        Returns:
            Refresh statistics
        """
        if self._is_simulated:
            await asyncio.sleep(0.3)
            return {
                "wallets_refreshed": 2,
                "tokens_updated": 8,
                "refreshed_at": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
            }
        
        # In production:
        # 1. Get all user's connected wallets
        # 2. Fetch balances from each chain
        # 3. Update database
        # 4. Calculate USD values using price feeds
        
        return {
            "wallets_refreshed": 0,
            "tokens_updated": 0
        }

    async def get_aggregated_portfolio(self, user_id: str) -> CryptoPortfolio:
        """Mock implementation of aggregated portfolio."""
        return CryptoPortfolio(
            user_id=user_id,
            total_usd_value=5000.0,
            balances=[
                Balance(token="ETH", chain=Chain.ETHEREUM, amount=1.2, usd_value=3000.0, price=2500.0),
                Balance(token="SOL", chain=Chain.SOLANA, amount=20.0, usd_value=2000.0, price=100.0)
            ],
            wallets=["0x123...", "789..."],
            last_updated=datetime.utcnow()
        )

    async def verify_connection(self, wallet_type: str) -> bool:
        """
        Verify if a wallet type can be connected.
        """
        # In a real implementation, this might check for browser extensions or specific protocols.
        # For now, we mock it as True for supported wallets.
        return wallet_type.lower() in [w.value for w in WalletType]

    def get_supported_chains(self) -> List[str]:
        return ["ethereum", "solana", "polygon", "bitcoin"]

    def get_wallet_balances(self, addresses: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Fetches balances for a list of cross-chain addresses.
        addresses: [{"address": "0x...", "chain": "eth"}, {"address": "...", "chain": "sol"}]
        """
        if self._is_simulated:
            return [
                {"address": addr['address'], "chain": addr['chain'], "balance": 1.5, "symbol": "ETH" if addr['chain'] == 'eth' else "SOL", "value_usd": 3500.00}
                for addr in addresses
            ]

        results = []
        for item in addresses:
            addr = item.get('address')
            chain = item.get('chain', 'eth').lower()
            
            try:
                if chain == 'eth':
                    balance_wei = self._w3.eth.get_balance(addr)
                    balance = self._w3.from_wei(balance_wei, 'ether')
                    results.append({"address": addr, "chain": "eth", "balance": float(balance), "symbol": "ETH"})
                elif chain == 'sol':
                    # Simplified Sol mock for now as solana-py can be flaky in some envs
                    results.append({"address": addr, "chain": "sol", "balance": 10.0, "symbol": "SOL"})
            except Exception as e:
                logger.error(f"Failed to fetch balance for {addr} on {chain}: {e}")
                
        return results

    def verify_ownership(self, address: str, signature: str, message: str) -> bool:
        """
        Verifies that a user owns a wallet via signature verification.
        """
        if self._is_simulated:
            return True
            
        try:
            from eth_account.messages import encode_defunct
            from web3 import Web3
            w3 = Web3()
            msghash = encode_defunct(text=message)
            recovered_addr = w3.eth.account.recover_message(msghash, signature=signature)
            return recovered_addr.lower() == address.lower()
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False

def get_wallet_service():
    return WalletService()
