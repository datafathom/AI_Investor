import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ArrowLeftRight, History, CreditCard } from 'lucide-react';

const TransferCenter = () => {
    const [accounts, setAccounts] = useState([]);
    const [history, setHistory] = useState([]);
    const [formData, setFormData] = useState({ from: '', to: '', amount: '' });

    useEffect(() => {
        const load = async () => {
            const [aRes, hRes] = await Promise.all([
                apiClient.get('/banking/accounts'),
                apiClient.get('/banking/history')
            ]);
            if (aRes.data.success) {
                setAccounts(aRes.data.data);
                if (aRes.data.data.length > 0) setFormData(f => ({ ...f, from: aRes.data.data[0].id }));
            }
            if (hRes.data.success) setHistory(hRes.data.data);
        };
        load();
    }, []);

    const handleTransfer = async (e) => {
        e.preventDefault();
        await apiClient.post('/banking/transfer', formData);
        alert("Transfer Initiated");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <ArrowLeftRight className="text-blue-400" /> Transfer Center
                </h1>
                <p className="text-slate-500">Internal Funding & Vendor Payments</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <CreditCard size={18} className="text-emerald-500" /> Initiate Transfer
                    </h3>
                    <form onSubmit={handleTransfer} className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">From Account</label>
                            <select 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white outline-none"
                                value={formData.from}
                                onChange={e => setFormData({...formData, from: e.target.value})}
                            >
                                {accounts.map(a => <option key={a.id} value={a.id}>{a.name} ({a.mask})</option>)}
                            </select>
                            <div className="text-xs text-slate-500 mt-1">Available: ${accounts.find(a => a.id === formData.from)?.balance.toLocaleString()}</div>
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">To Account</label>
                            <input 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white outline-none"
                                placeholder="Enter Account Number or Select Saved"
                                onChange={e => setFormData({...formData, to: e.target.value})}
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Amount</label>
                            <div className="flex items-center bg-slate-950 border border-slate-700 rounded p-2">
                                <span className="text-slate-400 mr-2">$</span>
                                <input 
                                    className="w-full bg-transparent text-white outline-none"
                                    type="number"
                                    value={formData.amount}
                                    onChange={e => setFormData({...formData, amount: parseFloat(e.target.value)})}
                                />
                            </div>
                        </div>
                        <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded mt-4">
                            SEND FUNDS
                        </button>
                    </form>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 border-b border-slate-800 font-bold text-white flex items-center gap-2">
                        <History size={18} className="text-slate-400" /> Recent Transfers
                    </div>
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Date</th>
                                <th className="p-4">From</th>
                                <th className="p-4">To</th>
                                <th className="p-4">Amount</th>
                                <th className="p-4">Status</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {history.map((tx, i) => (
                                <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 text-slate-400">{tx.date}</td>
                                    <td className="p-4 text-white">{tx.from}</td>
                                    <td className="p-4 text-white">{tx.to}</td>
                                    <td className="p-4 font-mono font-bold text-white">${tx.amount.toLocaleString()}</td>
                                    <td className="p-4">
                                        <span className="bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded text-xs font-bold">{tx.status}</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default TransferCenter;
