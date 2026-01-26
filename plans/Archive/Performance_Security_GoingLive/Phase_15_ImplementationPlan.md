# Phase 15: Real-Chain Crypto Wallet Connectivity
> **Phase ID**: 15
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement cross-chain wallet connectivity to enable users to track decentralized assets (DeFi, NFTs) alongside their institutional holdings. This phase focuses on the integration of Web3 providers (MetaMask, Phantom) and multi-chain balance tracking.

## Objectives
- [ ] Add `web3` and `solana` (or `solders`) to `requirements.txt`.
- [ ] Create `Web3WalletService` (backend) to verify wallet ownership and fetch balances.
- [ ] Implement support for Ethereum (EVM) and Solana (non-EVM) chains.
- [ ] Add API endpoints:
    - `POST /api/v1/crypto/wallet/link`
    - `GET /api/v1/crypto/wallet/balances`
- [ ] Create `WalletLinkWidget` (frontend).
- [ ] Integrate with the `CryptoDashboard`.

## Files to Modify/Create
1.  `requirements.txt` (Add `web3`, `solana`)
2.  `services/crypto/wallet_service.py` **[NEW]**
3.  `web/api/crypto_api.py` **[NEW]**
4.  `web/app.py` (Register Crypto API)
5.  `frontend2/src/widgets/Crypto/WalletLinkWidget.jsx` **[NEW]**
6.  `frontend2/src/pages/CryptoDashboard.jsx` (Integrate Widget)

## Technical Design

### Backend (`Web3WalletService`)
- Uses `web3.py` for Ethereum/Polygon/Base.
- Uses `solana-py` for Solana.
- **Simulation Mode**: Fallback to mock balances if no RPC nodes are configured.
- **Verification**: Support message signing (EIP-712) for secure ownership verification.

### API
- `POST /wallet/link`: Receives a public address and signed message to verify ownership.
- `GET /wallet/balances`: Aggregates balances across multiple linked wallets.

### Frontend
- **WalletLinkWidget**: Provides a "Connect Wallet" button using `wagmi` or `WalletConnect` patterns.
- Visualizes linked addresses with chain-specific icons (Ξ, ◎).

## Verification Plan

### Automated Tests
- `tests/system/test_wallet_service.py`:
    - Mock Web3/Solana RPC responses.
    - Verify balance aggregation logic.
    - Test signature verification (simulated).

### Manual Verification
1.  Navigate to `/portfolio/crypto`.
2.  Connect a MetaMask (EVM) or Phantom (SOL) wallet.
3.  Confirm cross-chain totals appear in the dashboard summary.
