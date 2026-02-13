import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Wallet, DollarSign, TrendingUp, PieChart } from 'lucide-react';

const AccountAggregator = () => {
    const [accounts, setAccounts] = useState([]);
    const [totals, setTotals] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const [aRes, tRes] = await Promise.all([
                    apiClient.get('/brokerage/accounts'),
                    apiClient.get('/brokerage/balances')
                ]);
                if (aRes.data.success) setAccounts(aRes.data.data);
                if (tRes.data.success) setTotals(tRes.data.data);
            } catch (e) { console.error(e); }
        };
        loadData();
    }, []);

    if (!totals) return <div className="p-8 text-slate-500">Aggregating Accounts...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Wallet className="text-yellow-500" /> Account Aggregator
                </h1>
                <p className="text-slate-500">Unified Portfolio View & Balance Reconciliation</p>
            </header>

            {/* Total Balance Card */}
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-8 mb-8 flex flex-col md:flex-row justify-between items-center shadow-lg">
                <div>
                     <div className="text-sm uppercase text-slate-400 font-bold mb-1">Total Net Liquidity</div>
                     <div className="text-5xl font-black text-white font-mono tracking-tight">
                        ${totals.total_nav.toLocaleString()}
                     </div>
                </div>
                <div className="text-right mt-4 md:mt-0">
                    <div className={`text-2xl font-bold flex items-center gap-2 justify-end ${totals.day_change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {totals.day_change >= 0 ? <TrendingUp size={24} /> : <TrendingUp size={24} className="rotate-180" />}
                        {totals.day_change >= 0 ? '+' : ''}{totals.day_change.toLocaleString()} ({totals.day_change_pct}%)
                    </div>
                    <div className="text-slate-400 text-sm mt-1">Today's P&L</div>
                </div>
            </div>

            {/* Account List */}
            <div className="grid grid-cols-1 gap-4">
                {accounts.map(acc => (
                    <div key={acc.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex justify-between items-center hover:border-slate-600 transition-colors">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center font-bold text-white text-lg">
                                {acc.broker[0]}
                            </div>
                            <div>
                                <div className="font-bold text-lg text-white">{acc.broker} <span className="text-slate-500 text-sm font-normal">({acc.type})</span></div>
                                <div className="text-slate-500 font-mono text-xs">{acc.id}</div>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className="text-xl font-bold text-white font-mono">${acc.nav.toLocaleString()}</div>
                            <div className="text-xs text-green-400 font-bold">BP: ${acc.buying_power.toLocaleString()}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AccountAggregator;
