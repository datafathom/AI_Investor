import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Wallet, CreditCard, Link } from 'lucide-react';

const CryptoWalletPage = () => {
    const [wallets, setWallets] = useState([]);
    const [balances, setBalances] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [wRes, bRes] = await Promise.all([
                apiClient.get('/crypto/wallets'),
                apiClient.get('/crypto/balances')
            ]);
            if (wRes.data.success) setWallets(wRes.data.data);
            if (bRes.data.success) setBalances(bRes.data.data);
        };
        load();
    }, []);

    const connectWallet = async () => {
        const addr = prompt("Enter Wallet Address:");
        if (addr) {
            await apiClient.post('/crypto/wallets', null, { params: { address: addr, label: "New Wallet" } });
            alert("Wallet Connected");
            // Reload
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Wallet className="text-orange-500" /> Unified Crypto Wallet
                </h1>
                <p className="text-slate-500">Multi-Chain Assets & Exchange Connections</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-bold text-white">Connected Wallets</h3>
                            <button onClick={connectWallet} className="text-blue-400 hover:text-blue-300">
                                <Link size={16} />
                            </button>
                        </div>
                        <div className="space-y-3">
                            {wallets.map(w => (
                                <div key={w.id} className="p-3 bg-slate-950 rounded border border-slate-800">
                                    <div className="flex justify-between items-start">
                                        <span className="font-bold text-white text-sm">{w.name}</span>
                                        <span className="text-xs text-slate-500 uppercase">{w.type}</span>
                                    </div>
                                    <div className="text-xs text-slate-400 truncate mt-1">{w.address}</div>
                                    <div className="flex gap-1 mt-2">
                                        {w.chains.map(c => (
                                            <span key={c} className="bg-slate-800 text-slate-300 px-1 py-0.5 rounded text-[10px]">{c}</span>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 border-b border-slate-800 font-bold text-white flex items-center gap-2">
                        <CreditCard size={18} className="text-emerald-500" /> Unified Balances
                    </div>
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Asset</th>
                                <th className="p-4">Balance</th>
                                <th className="p-4">Price</th>
                                <th className="p-4">Value (USD)</th>
                                <th className="p-4">Source</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {balances.map((b, i) => (
                                <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 font-bold text-white">{b.symbol}</td>
                                    <td className="p-4 text-slate-300">{b.amount}</td>
                                    <td className="p-4 font-mono text-slate-400">${b.price.toLocaleString()}</td>
                                    <td className="p-4 font-mono font-bold text-white">${b.value.toLocaleString()}</td>
                                    <td className="p-4 text-xs text-slate-500">{b.wallet}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default CryptoWalletPage;
