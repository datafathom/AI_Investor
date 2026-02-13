import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BookOpen, Download } from 'lucide-react';

const TransactionLedger = () => {
    const [txns, setTxns] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/audit/ledger');
            if (res.data.success) setTxns(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <BookOpen className="text-slate-400" /> Transaction Ledger
                    </h1>
                    <p className="text-slate-500">Double-Entry Bookkeeping Records</p>
                </div>
                <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded flex items-center gap-2 text-sm">
                    <Download size={16} /> EXPORT CSV
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Date</th>
                            <th className="p-4">Type</th>
                            <th className="p-4">Details</th>
                            <th className="p-4">Account</th>
                            <th className="p-4 text-right">Amount</th>
                            <th className="p-4 text-right">Balance</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {txns.map(t => (
                            <tr key={t.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 text-slate-400">{t.date}</td>
                                <td className="p-4 font-bold text-white">{t.type}</td>
                                <td className="p-4">
                                    {t.symbol && <span className="text-cyan-400 font-mono mr-2">{t.symbol}</span>}
                                    {t.qty > 0 && <span className="text-slate-500">x{t.qty} @ ${t.price}</span>}
                                </td>
                                <td className="p-4 text-slate-300">{t.account}</td>
                                <td className={`p-4 font-mono font-bold text-right ${t.type === 'DEPOSIT' || t.type === 'SELL' ? 'text-emerald-400' : 'text-slate-300'}`}>
                                    {t.amount ? `+${t.amount.toLocaleString()}` : `-${(t.qty * t.price).toLocaleString()}`}
                                </td>
                                <td className="p-4 font-mono text-right text-slate-400">${t.balance.toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TransactionLedger;
