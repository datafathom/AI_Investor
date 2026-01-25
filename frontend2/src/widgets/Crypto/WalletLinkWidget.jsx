
import React, { useState, useEffect } from 'react';
import { Wallet, Link, CheckCircle2, XCircle, AlertCircle, RefreshCw, Key } from 'lucide-react';
import './WalletLinkWidget.css';

const WalletLinkWidget = () => {
    const [linkedWallets, setLinkedWallets] = useState([]);
    const [connecting, setConnecting] = useState(false);
    const [balances, setBalances] = useState({});

    const MOCK_WALLETS = [
        { address: '0x71C...32E1', chain: 'eth', icon: 'Ξ' },
        { address: '6yP...k9pS', chain: 'sol', icon: '◎' }
    ];

    useEffect(() => {
        // Initial load simulation
        setLinkedWallets(MOCK_WALLETS);
    }, []);

    const handleConnect = () => {
        setConnecting(true);
        // Simulation: wait for metamask handshake
        setTimeout(() => {
            const newWallet = { address: '0x12a...B42c', chain: 'eth', icon: 'Ξ' };
            setLinkedWallets(prev => [...prev, newWallet]);
            setConnecting(false);
        }, 1500);
    };

    return (
        <div className="wallet-link-widget">
            <div className="wallet-header">
                <div className="title">
                    <Wallet size={18} className="text-indigo-400" />
                    <h3>Web3 Command Center</h3>
                </div>
                <div className="network-indicator">
                    <div className="dot"></div>
                    Mainnet Active
                </div>
            </div>

            <div className="wallets-grid">
                {linkedWallets.map((w, i) => (
                    <div key={i} className={`wallet-tile ${w.chain}`}>
                        <div className="chain-glyph">{w.icon}</div>
                        <div className="wallet-details">
                            <span className="address">{w.address}</span>
                            <span className="chain-label">{w.chain.toUpperCase()}</span>
                        </div>
                        <div className="verified-badge">
                            <CheckCircle2 size={12} />
                        </div>
                    </div>
                ))}

                <button className="add-wallet-btn" onClick={handleConnect} disabled={connecting}>
                    {connecting ? <RefreshCw size={16} className="spinning" /> : <Link size={16} />}
                    {connecting ? "Connecting Provider..." : "Link New Multi-Chain Wallet"}
                </button>
            </div>

            <div className="security-note">
                <Key size={12} />
                <span>Private keys never leave your browser. Verification via EIP-712.</span>
            </div>
        </div>
    );
};

export default WalletLinkWidget;
