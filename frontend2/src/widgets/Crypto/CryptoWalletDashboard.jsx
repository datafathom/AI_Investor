import React, { useState } from 'react';
import { HardDrive, Shield, RefreshCw, ExternalLink, Copy, Wallet } from 'lucide-react';
import './CryptoWallet.css';

/**
 * Hardware Wallet Dashboard
 * 
 * Displays crypto holdings from hardware wallets (Ledger/Trezor)
 * with portfolio breakdown and security status.
 */
const CryptoWalletDashboard = () => {
    const [activeWallet, setActiveWallet] = useState('ledger');
    const [isRefreshing, setIsRefreshing] = useState(false);

    const wallets = {
        ledger: {
            name: 'Ledger Nano X',
            address: '0x742d...f8a9',
            connected: true,
            lastSync: '2 min ago',
            holdings: [
                { symbol: 'BTC', name: 'Bitcoin', amount: 1.25, value: 52500, change24h: 2.3 },
                { symbol: 'ETH', name: 'Ethereum', amount: 15.8, value: 37500, change24h: -1.2 },
                { symbol: 'SOL', name: 'Solana', amount: 450, value: 45000, change24h: 5.1 },
            ]
        },
        trezor: {
            name: 'Trezor Model T',
            address: '0x8f3c...2b1e',
            connected: false,
            lastSync: '1 hour ago',
            holdings: [
                { symbol: 'BTC', name: 'Bitcoin', amount: 0.5, value: 21000, change24h: 2.3 },
                { symbol: 'LINK', name: 'Chainlink', amount: 1500, value: 15000, change24h: -3.5 },
            ]
        }
    };

    const currentWallet = wallets[activeWallet];
    const totalValue = currentWallet.holdings.reduce((sum, h) => sum + h.value, 0);

    const handleRefresh = () => {
        setIsRefreshing(true);
        setTimeout(() => setIsRefreshing(false), 2000);
    };

    const copyAddress = () => {
        navigator.clipboard.writeText(currentWallet.address);
    };

    return (
        <div className="crypto-wallet-dashboard">
            <div className="wallet-header">
                <div className="wallet-selector">
                    {Object.entries(wallets).map(([key, wallet]) => (
                        <button
                            key={key}
                            className={`wallet-tab ${activeWallet === key ? 'active' : ''}`}
                            onClick={() => setActiveWallet(key)}
                        >
                            <HardDrive size={14} />
                            <span>{wallet.name}</span>
                            <span className={`status-dot ${wallet.connected ? 'connected' : 'disconnected'}`}></span>
                        </button>
                    ))}
                </div>
                <button className={`refresh-btn ${isRefreshing ? 'spinning' : ''}`} onClick={handleRefresh}>
                    <RefreshCw size={14} />
                </button>
            </div>

            <div className="wallet-info">
                <div className="address-row">
                    <code>{currentWallet.address}</code>
                    <button onClick={copyAddress}><Copy size={12} /></button>
                    <a href="#" target="_blank"><ExternalLink size={12} /></a>
                </div>
                <div className="security-badge">
                    <Shield size={12} />
                    <span>Hardware Secured</span>
                </div>
            </div>

            <div className="portfolio-value">
                <span className="label">Total Value</span>
                <span className="value">${totalValue.toLocaleString()}</span>
            </div>

            <div className="holdings-list">
                {currentWallet.holdings.map((holding, idx) => (
                    <div key={idx} className="holding-row">
                        <div className="holding-icon">
                            <Wallet size={16} />
                        </div>
                        <div className="holding-info">
                            <span className="symbol">{holding.symbol}</span>
                            <span className="name">{holding.name}</span>
                        </div>
                        <div className="holding-amount">
                            <span>{holding.amount}</span>
                        </div>
                        <div className="holding-value">
                            <span className="usd">${holding.value.toLocaleString()}</span>
                            <span className={`change ${holding.change24h >= 0 ? 'positive' : 'negative'}`}>
                                {holding.change24h >= 0 ? '+' : ''}{holding.change24h}%
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="wallet-footer">
                <span>Last synced: {currentWallet.lastSync}</span>
            </div>
        </div>
    );
};

export default CryptoWalletDashboard;
