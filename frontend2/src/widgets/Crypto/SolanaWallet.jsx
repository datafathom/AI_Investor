/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Crypto/SolanaWallet.jsx
 * ROLE: Solana Wallet Widget
 * PURPOSE: Displays SOL balance and SPL tokens with logos and USD values.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/solana/balance: SOL balance endpoint
 *     - /api/v1/solana/tokens: SPL token balances
 *     - /api/v1/solana/token-info: Token metadata lookup
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import './SolanaWallet.css';

const API_BASE = '/api/v1/solana';

const SolanaWallet = ({ address, onAddressChange }) => {
    const [solBalance, setSolBalance] = useState(null);
    const [tokens, setTokens] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [inputAddress, setInputAddress] = useState(address || '');

    useEffect(() => {
        if (address) {
            loadWalletData(address);
        }
    }, [address]);

    const loadWalletData = async (walletAddress) => {
        setLoading(true);
        setError(null);

        try {
            const [balanceRes, tokensRes] = await Promise.all([
                fetch(`${API_BASE}/balance/${walletAddress}`),
                fetch(`${API_BASE}/tokens/${walletAddress}`)
            ]);

            if (!balanceRes.ok || !tokensRes.ok) {
                throw new Error('Failed to load wallet data');
            }

            const balanceData = await balanceRes.json();
            const tokensData = await tokensRes.json();

            setSolBalance(balanceData);
            setTokens(tokensData.tokens || []);

        } catch (err) {
            console.error('Failed to load Solana wallet:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleAddressSubmit = (e) => {
        e.preventDefault();
        if (inputAddress.trim() && onAddressChange) {
            onAddressChange(inputAddress.trim());
        }
    };

    const formatAddress = (addr) => {
        if (!addr) return '';
        return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
    };

    return (
        <div className="solana-wallet">
            <div className="solana-wallet__header">
                <h3>🟣 Solana Wallet</h3>
            </div>

            {!address && (
                <form onSubmit={handleAddressSubmit} className="solana-wallet__form">
                    <input
                        type="text"
                        value={inputAddress}
                        onChange={(e) => setInputAddress(e.target.value)}
                        placeholder="Enter Solana wallet address"
                        className="solana-wallet__input"
                    />
                    <button type="submit" className="solana-wallet__submit">
                        Load Wallet
                    </button>
                </form>
            )}

            {error && (
                <div className="solana-wallet__error">
                    ⚠️ {error}
                </div>
            )}

            {loading && (
                <div className="solana-wallet__loading">
                    Loading wallet data...
                </div>
            )}

            {solBalance && !loading && (
                <>
                    {/* SOL Balance */}
                    <div className="solana-wallet__balance">
                        <div className="balance-label">SOL Balance</div>
                        <div className="balance-value">
                            {solBalance.balance_sol?.toFixed(4)} SOL
                        </div>
                        {address && (
                            <div className="balance-address">
                                {formatAddress(address)}
                            </div>
                        )}
                    </div>

                    {/* SPL Tokens */}
                    {tokens.length > 0 && (
                        <div className="solana-wallet__tokens">
                            <h4>SPL Tokens ({tokens.length})</h4>
                            <div className="tokens-list">
                                {tokens.map((token, idx) => (
                                    <div key={idx} className="token-item">
                                        <div className="token-icon">
                                            {token.logo_uri ? (
                                                <img
                                                    src={token.logo_uri}
                                                    alt={token.symbol}
                                                    onError={(e) => {
                                                        e.target.style.display = 'none';
                                                    }}
                                                />
                                            ) : (
                                                <div className="token-icon-placeholder">
                                                    {token.symbol?.[0] || '?'}
                                                </div>
                                            )}
                                        </div>
                                        <div className="token-info">
                                            <div className="token-symbol">{token.symbol}</div>
                                            {token.name && (
                                                <div className="token-name">{token.name}</div>
                                            )}
                                        </div>
                                        <div className="token-balance">
                                            {token.balance?.toLocaleString(undefined, {
                                                maximumFractionDigits: token.decimals || 6
                                            })}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {tokens.length === 0 && !loading && (
                        <div className="solana-wallet__empty">
                            No SPL tokens found
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default SolanaWallet;
