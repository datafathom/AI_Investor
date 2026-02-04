import React from 'react';
import { Wallet, Landmark, CreditCard, PieChart, TrendingUp, DollarSign } from 'lucide-react';
import '../App.css';

const PortfolioManagement = () => {
    const accounts = [
        { id: 'robinhood', name: 'Robinhood', balance: 125430.22, change: '+1.2%', icon: <TrendingUp size={24} className="text-green-400" /> },
        { id: 'boa', name: 'Bank of America', balance: 45200.00, change: '0.0%', icon: <Landmark size={24} className="text-blue-400" /> },
        { id: 'chime', name: 'Chime Bank', balance: 8400.50, change: '-0.5%', icon: <CreditCard size={24} className="text-yellow-400" /> },
        { id: '401k', name: 'Fidelity 401k', balance: 342000.00, change: '+0.8%', icon: <PieChart size={24} className="text-purple-400" /> },
    ];

    const totalBalance = accounts.reduce((acc, curr) => acc + curr.balance, 0);

    return (
        <div className="portfolio-management-dashboard glass-panel p-8 animate-fade-in">
            <header className="mb-10">
                <div className="flex items-center gap-4 mb-6">
                    <div className="p-3 bg-cyan-500/10 rounded-2xl text-cyan-400 border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]">
                        <Wallet size={28} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-black text-white tracking-tight uppercase">Net Worth Home Base</h1>
                        <p className="text-zinc-500 font-medium">Consolidated Assets across all connected accounts</p>
                    </div>
                </div>

                <div className="bg-zinc-900/40 border border-zinc-800 p-8 rounded-3xl mb-8 relative overflow-hidden">
                    <div className="relative z-10">
                        <h2 className="text-zinc-500 text-sm font-bold uppercase tracking-[0.2em] mb-2">Total Combined Balance</h2>
                        <div className="text-6xl font-black text-white tracking-tighter flex items-center gap-2">
                             <span className="text-cyan-500">$</span>{totalBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </div>
                    </div>
                    {/* Background glow */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 blur-[100px] -mr-32 -mt-32" />
                </div>
            </header>

            <section>
                <h4 className="text-zinc-600 uppercase text-[10px] font-black tracking-[0.2em] mb-6">Connected Accounts</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {accounts.map((account) => (
                        <div key={account.id} className="group bg-zinc-900/40 border border-zinc-800 p-6 rounded-2xl hover:border-cyan-500/40 hover:bg-cyan-500/5 transition-all duration-300">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-2 bg-zinc-800 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                                    {account.icon}
                                </div>
                                <span className={`text-[10px] font-bold px-2 py-1 rounded-md ${account.change.startsWith('+') ? 'bg-green-500/10 text-green-400' : account.change.startsWith('-') ? 'bg-red-500/10 text-red-400' : 'bg-zinc-800 text-zinc-400'}`}>
                                    {account.change}
                                </span>
                            </div>
                            <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider mb-1">{account.name}</h3>
                            <div className="text-2xl font-black text-white">
                                ${account.balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                            </div>
                            <div className="mt-4 pt-4 border-t border-zinc-800/50 flex gap-2">
                                <button className="text-[10px] font-black uppercase tracking-widest text-cyan-400 hover:text-white transition-colors">View Details</button>
                                <button className="text-[10px] font-black uppercase tracking-widest text-zinc-500 hover:text-white transition-colors">Sync</button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default PortfolioManagement;
