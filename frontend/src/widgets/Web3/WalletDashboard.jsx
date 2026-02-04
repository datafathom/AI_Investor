import React, { useState, useEffect } from 'react';
import { HardDrive, Shield, RefreshCw, ExternalLink, Copy, Wallet, AlertCircle } from 'lucide-react';
import { useWeb3Store } from '../../stores/web3Store';
import './CryptoWallet.css'; // Reusing existing CSS or create new

const WalletDashboard = () => {
    const { portfolio, activeWalletId, setActiveWallet, fetchPortfolio, isLoading } = useWeb3Store();
    const [isRefreshing, setIsRefreshing] = useState(false);
    
    // Default active wallet if none selected
    useEffect(() => {
        if (!activeWalletId) setActiveWallet('ledger');
        if (!portfolio) fetchPortfolio('default_user');
    }, []);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await fetchPortfolio('default_user');
        setTimeout(() => setIsRefreshing(false), 1000);
    };

    const copyAddress = (addr) => {
        navigator.clipboard.writeText(addr);
    };

    // Mock wallet metadata (in a real app, this might come from a device manager)
    const wallets = {
        ledger: { name: 'Ledger Nano X', status: 'connected', address: portfolio?.wallets[0] || '0x...' },
        trezor: { name: 'Trezor Model T', status: 'disconnected', address: portfolio?.wallets[1] || '0x...' }
    };

    const currentWallet = wallets[activeWalletId] || wallets['ledger'];

    return (
        <div className="crypto-wallet-dashboard glass-panel p-4 h-full flex flex-col">
            <div className="wallet-header flex justify-between items-center mb-4">
                <div className="wallet-selector flex gap-2">
                    {Object.entries(wallets).map(([key, w]) => (
                        <button
                            key={key}
                            className={`wallet-tab px-3 py-1.5 rounded-lg flex items-center gap-2 text-sm transition-all ${activeWalletId === key ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-slate-800/50 text-slate-400 hover:bg-slate-700/50'}`}
                            onClick={() => setActiveWallet(key)}
                        >
                            <HardDrive size={14} />
                            <span>{w.name}</span>
                            <span className={`w-2 h-2 rounded-full ${w.status === 'connected' ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-slate-600'}`}></span>
                        </button>
                    ))}
                </div>
                <button 
                    className={`p-2 rounded-full hover:bg-slate-700/50 text-slate-400 transition-all ${isLoading || isRefreshing ? 'animate-spin' : ''}`}
                    onClick={handleRefresh}
                >
                    <RefreshCw size={14} />
                </button>
            </div>

            <div className="wallet-info bg-slate-900/50 rounded-xl p-3 mb-4 flex justify-between items-center border border-slate-800">
                <div className="flex items-center gap-2">
                    <code className="text-xs text-slate-300 font-mono bg-slate-800 px-2 py-1 rounded">{currentWallet.address.substring(0, 12)}...{currentWallet.address.substring(38)}</code>
                    <button onClick={() => copyAddress(currentWallet.address)} className="text-slate-500 hover:text-white transition-colors"><Copy size={12} /></button>
                    <a href="#" className="text-slate-500 hover:text-white transition-colors"><ExternalLink size={12} /></a>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                    <Shield size={10} />
                    <span>Hardware Secured</span>
                </div>
            </div>

            <div className="portfolio-value mb-6">
                <span className="text-slate-400 text-sm block mb-1">Total Vault Value</span>
                <span className="text-3xl font-bold text-white tracking-tight">
                    ${portfolio?.total_usd_value?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || '0.00'}
                </span>
            </div>

            <div className="holdings-list flex-1 overflow-y-auto pr-1 space-y-2 custom-scrollbar">
                {portfolio?.balances.map((holding, idx) => (
                    <div key={idx} className="holding-row flex items-center justify-between p-3 rounded-lg bg-slate-800/30 border border-slate-700/30 hover:bg-slate-800/50 transition-colors group">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-slate-300 group-hover:bg-cyan-500/20 group-hover:text-cyan-400 transition-colors">
                                <Wallet size={16} />
                            </div>
                            <div>
                                <div className="text-sm font-bold text-white">{holding.token}</div>
                                <div className="text-xs text-slate-500 capitalize">{holding.chain} Chain</div>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className="text-sm font-medium text-white">{holding.amount} {holding.token}</div>
                            <div className="text-xs text-slate-400">${holding.usd_value.toLocaleString()}</div>
                        </div>
                    </div>
                ))}
            </div>
            
            <div className="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-500 flex justify-between">
                 <span>Last synced: {portfolio ? new Date(portfolio.last_updated).toLocaleTimeString() : 'Never'}</span>
                 <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span> Live Socket</span>
            </div>
        </div>
    );
};

export default WalletDashboard;
