/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Wallet/CryptoWallet.jsx
 * ROLE: Wallet Integration Widget
 * PURPOSE: Simulates Coinbase Wallet connection and asset display.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import useWalletStore from '../../stores/walletStore';
import './CryptoWallet.css';

const CryptoWallet = ({ mock = true }) => {
    const { balance, transactions, isConnected, connectWallet, loading, error } = useWalletStore();

    const handleConnect = () => {
        connectWallet(mock);
    };

    return (
        <div className="crypto-wallet-widget">
            <header className="widget-header">
                <h3>Crypto Wallet</h3>
                <span className={`status-pill ${isConnected ? 'active' : ''}`}>
                    {isConnected ? 'Connected' : 'Disconnected'}
                </span>
            </header>

            {error && <div className="error-banner">{error}</div>}

            {!isConnected ? (
                <div className="connect-screen">
                    <p>Link your Coinbase account to track assets and trade via AI.</p>
                    <button 
                        className="cb-connect-btn" 
                        onClick={handleConnect}
                        disabled={loading}
                    >
                        {loading ? 'Connecting...' : 'Connect with Coinbase'}
                    </button>
                    <p className="secure-note">🔒 Read-only access initially</p>
                </div>
            ) : (
                <div className="wallet-content">
                    {/* Total Balance */}
                    <div className="total-balance">
                        <span className="label">Total Balance</span>
                        <div className="value">
                            ${(balance?.total_balance_usd || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                        </div>
                    </div>

                    {/* Assets Grid */}
                    <div className="assets-list">
                        <h4>Assets</h4>
                        {balance?.assets?.map((asset, idx) => (
                            <div key={idx} className="asset-row">
                                <div className="asset-name">
                                    <span className="ticker">{asset.currency}</span>
                                    <span className="name">{asset.name}</span>
                                </div>
                                <div className="asset-val">
                                    <div className="usd">${(asset.value_usd).toLocaleString()}</div>
                                    <div className="amt">{asset.amount} {asset.currency}</div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Recent Txns */}
                    <div className="txns-list">
                        <h4>Recent Activity</h4>
                        {transactions?.map(tx => (
                            <div key={tx.id} className="txn-row">
                                <span className={`type ${tx.type}`}>{tx.type.toUpperCase()}</span>
                                <span className="detail">
                                    {tx.amount.amount} {tx.amount.currency}
                                </span>
                                <span className="date">{new Date(tx.created_at).toLocaleDateString()}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            <div className="footer">
                <span>Coinbase Integration {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default CryptoWallet;
