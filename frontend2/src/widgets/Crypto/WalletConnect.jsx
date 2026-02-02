/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Crypto/WalletConnect.jsx
 * ROLE: Wallet Connect Widget
 * PURPOSE: Allows users to connect Ethereum wallets via address entry or
 *          WalletConnect protocol for read-only tracking and transaction signing.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/ethereum/balance: ETH balance endpoint
 *     - /api/v1/ethereum/tokens: ERC-20 token balances
 *     - WalletService: Portfolio sync
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './WalletConnect.css';

const API_BASE = '/ethereum';

const WalletConnect = ({ onWalletConnected }) => {
    const [address, setAddress] = useState('');
    const [balance, setBalance] = useState(null);
    const [tokens, setTokens] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [connectedWallets, setConnectedWallets] = useState([]);

    useEffect(() => {
        // Load previously connected wallets from localStorage
        const saved = localStorage.getItem('connected_wallets');
        if (saved) {
            try {
                setConnectedWallets(JSON.parse(saved));
            } catch (e) {
                console.error('Failed to load saved wallets:', e);
            }
        }
    }, []);

    const handleAddressSubmit = async (e) => {
        e.preventDefault();
        
        if (!address.trim()) {
            setError('Please enter a wallet address');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // Validate address
            const validateResponse = await apiClient.post(`${API_BASE}/validate-address`, { address: address.trim() });
            const validateData = validateResponse.data;

            if (!validateData.valid) {
                throw new Error('Invalid Ethereum address format');
            }

            // Fetch balance and tokens
            const [balanceRes, tokensRes] = await Promise.all([
                apiClient.get(`${API_BASE}/balance/${address.trim()}`),
                apiClient.get(`${API_BASE}/tokens/${address.trim()}`)
            ]);

            const balanceData = balanceRes.data;
            const tokensData = tokensRes.data;

            setBalance(balanceData);
            setTokens(tokensData.tokens || []);

            // Add to connected wallets
            const walletInfo = {
                address: address.trim(),
                balance: balanceData.balance_eth,
                token_count: tokensData.count,
                connected_at: new Date().toISOString()
            };

            const updated = [...connectedWallets, walletInfo];
            setConnectedWallets(updated);
            localStorage.setItem('connected_wallets', JSON.stringify(updated));

            if (onWalletConnected) {
                onWalletConnected(walletInfo);
            }

            // Clear input
            setAddress('');

        } catch (err) {
            console.error('Wallet connection failed:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDisconnect = (addressToRemove) => {
        const updated = connectedWallets.filter(w => w.address !== addressToRemove);
        setConnectedWallets(updated);
        localStorage.setItem('connected_wallets', JSON.stringify(updated));
        
        if (addressToRemove === address) {
            setBalance(null);
            setTokens([]);
        }
    };

    const formatAddress = (addr) => {
        if (!addr) return '';
        return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
    };

    return (
        <div className="wallet-connect">
            <div className="wallet-connect__header">
                <h3>🔗 Connect Ethereum Wallet</h3>
            </div>

            <form onSubmit={handleAddressSubmit} className="wallet-connect__form">
                <div className="wallet-connect__input-group">
                    <input
                        type="text"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        placeholder="Enter wallet address (0x...)"
                        className="wallet-connect__input"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        className="wallet-connect__connect-btn"
                        disabled={loading || !address.trim()}
                    >
                        {loading ? 'Connecting...' : 'Connect'}
                    </button>
                </div>

                {error && (
                    <div className="wallet-connect__error">
                        ⚠️ {error}
                    </div>
                )}
            </form>

            {/* Connected Wallets */}
            {connectedWallets.length > 0 && (
                <div className="wallet-connect__wallets">
                    <h4>Connected Wallets</h4>
                    <div className="wallets-list">
                        {connectedWallets.map((wallet, idx) => (
                            <div key={idx} className="wallet-item">
                                <div className="wallet-item__info">
                                    <div className="wallet-item__address">
                                        {formatAddress(wallet.address)}
                                    </div>
                                    <div className="wallet-item__balance">
                                        {wallet.balance?.toFixed(4)} ETH
                                    </div>
                                    {wallet.token_count > 0 && (
                                        <div className="wallet-item__tokens">
                                            {wallet.token_count} tokens
                                        </div>
                                    )}
                                </div>
                                <button
                                    className="wallet-item__disconnect"
                                    onClick={() => handleDisconnect(wallet.address)}
                                >
                                    Disconnect
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* WalletConnect Integration Note */}
            <div className="wallet-connect__note">
                <p>💡 <strong>WalletConnect</strong> integration coming soon for transaction signing</p>
            </div>
        </div>
    );
};

export default WalletConnect;
