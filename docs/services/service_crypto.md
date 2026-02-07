# Backend Service: Crypto

## Overview
The **Crypto Service** is the platform's portal to the digital asset ecosystem. It provides a unified, cross-chain interface for managing self-custody wallets (Ethereum, Solana, Bitcoin, Polygon), institutional exchange accounts (Coinbase Advanced), and decentralized finance (DeFi) interactions. It handles the complexity of gas optimization, signature verification, and multi-chain balance aggregation.

## Core Components

### 1. Multi-Chain Wallet Orchestration (`wallet_service.py`)
The central hub for user-controlled assets.
- **Cross-Chain Aggregation**: Consolidates balances across disparate networks (ETH, SOL, BTC) into a single `CryptoPortfolio` view.
- **Ownership Verification**: Implements EIP-191 style message signing and verification to securely link on-chain addresses to platform users.
- **Address Validation**: Provides chain-specific regex and checksum validation for preventing loss of funds due to invalid destination addresses.

### 2. Blockchain & Exchange Clients
- **Network Clients (`ethereum_client.py`, `solana_client.py`)**: Direct RPC integrations for fetching native and token (ERC-20, SPL) balances, price feeds, and transaction statuses.
- **Institutional Gateway (`coinbase_client.py`, `coinbase_custody.py`)**: Programmatic access to Coinbase Advanced Trading and Vaults, enabling seamless transition between centralized and decentralized liquidity.

### 3. Gas & Fee Optimization (`gas_service.py`)
Ensures cost-effective on-chain execution.
- **Real-Time Monitoring**: Tracks gas prices on Ethereum, Polygon, and Arbitrum.
- **Optimal Window Detection**: Analyzes historical volatility to recommend low-fee execution windows (e.g., finding periods where gas is <3 std dev from the 24h mean).
- **Transaction Queuing**: Allows users to "Set and Forget" transactions that execute automatically when gas hits a target Gwei threshold.

### 4. Advanced Security (`shamir_secret.py`)
- **Key Sharding**: Implements Shamir's Secret Sharing (SSS) to shard sensitive master keys or recovery phrases across multiple encrypted storage nodes, eliminating single points of failure in key management.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Crypto Terminal** | Portfolio Overview | `wallet_service.get_aggregated_portfolio()` |
| **Wallet Connect** | Auth Modal | `wallet_service.verify_ownership()` (Signature) |
| **Trade Modal** | Gas Fee Estimator | `gas_service.get_current_gas()` |
| **Trade Modal** | Execution Scheduler | `gas_service.get_optimal_execution_window()` |
| **DeFi Hub** | Yield Aggregator | `lp_tracker_service.py` (Liquidity metrics) |

## Dependencies
- `web3`: For Ethereum JSON-RPC communication and signature recovery.
- `pydantic`: For strictly-typed models like `Balance` and `CryptoPortfolio`.
- `services.system.secret_manager`: Securely retrieves RPC URLs and API credentials.

## Usage Examples

### Fetching a Unified Cross-Chain Portfolio
```python
from services.crypto.wallet_service import get_wallet_service

wallet_svc = get_wallet_service()

# Aggregates ETH, SOL, and others into a single USD-denominated view
portfolio = await wallet_svc.get_aggregated_portfolio(user_id="user_vanguard_1")

print(f"Total Crypto Value: ${portfolio.total_usd_value:,.2f}")
for balance in portfolio.balances:
    print(f"- {balance.amount} {balance.token} on {balance.chain}")
```

### Scheduling a Low-Fee Transaction
```python
from services.crypto.gas_service import GasService

gas_svc = GasService()

# Check if now is a good time to execute
if await gas_svc.detect_spike("ethereum"):
    # Find the next cheap window instead
    window = await gas_svc.get_optimal_execution_window()
    print(f"Gas Spike Detected! Optimal window: {window.start_time}")
else:
    print("Gas levels stable. Executing now.")
```
