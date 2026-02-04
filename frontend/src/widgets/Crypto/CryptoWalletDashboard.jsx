import React, { useState } from 'react';
import { HardDrive, Shield, RefreshCw, ExternalLink, Copy, Wallet } from 'lucide-react';
import useWeb3Store from '../../stores/web3Store';
import './CryptoWallet.css';

/**
 * Hardware Wallet Dashboard
 * 
 * Displays crypto holdings from hardware wallets (Ledger/Trezor)
 * with portfolio breakdown and security status.
 */
const CryptoWalletDashboard = () => {
    const { portfolio, isLoading } = useWeb3Store();
    const [activeWallet, setActiveWallet] = useState('main');
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Derive wallets from portfolio data
    const wallets = {};
    if (portfolio?.wallets && Object.keys(portfolio.wallets).length > 0) {
        Object.assign(wallets, portfolio.wallets);
    } else if (portfolio?.assets) {
        // Fallback: Treat entire portfolio as one wallet
        wallets['main'] = {
            name: 'Main Portfolio',
            address: portfolio.address || '0x...',
            connected: true,
            lastSync: 'Now',
            holdings: portfolio.assets.map(a => ({
                symbol: a.symbol,
                name: a.name || a.symbol,
                amount: a.amount,
                value: a.value_usd || (a.amount * (a.price || 0)),
                change24h: a.change_24h || 0
            }))
        };
    } else {
        // Loading or Empty State
        wallets['main'] = {
            name: 'Loading...',
            address: '...',
            connected: false,
            lastSync: '...',
            holdings: []
        };
    }

    const currentWallet = wallets[activeWallet] || wallets[Object.keys(wallets)[0]];
    const totalValue = currentWallet?.holdings?.reduce((sum, h) => sum + h.value, 0) || 0;

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
