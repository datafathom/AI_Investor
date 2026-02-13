import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Receipt, Tag, DollarSign } from 'lucide-react';

const ExpenseManager = () => {
    const [expenses, setExpenses] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/banking/expenses');
            if (res.data.success) setExpenses(res.data.data);
        };
        load();
    }, []);

    const categorize = async (id) => {
        const cat = prompt("Enter Category:");
        if (!cat) return;
        await apiClient.post('/banking/expenses/categorize', null, { params: { id, category: cat } });
        // Refresh
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Receipt className="text-pink-500" /> Expense Management
                </h1>
                <p className="text-slate-500">Operational Costs & Vendor Payments</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Date</th>
                            <th className="p-4">Vendor</th>
                            <th className="p-4">Category</th>
                            <th className="p-4 text-right">Amount</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {expenses.map(exp => (
                            <tr key={exp.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 text-slate-400">{exp.date}</td>
                                <td className="p-4 font-bold text-white">{exp.vendor}</td>
                                <td className="p-4">
                                    <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs">{exp.category}</span>
                                </td>
                                <td className="p-4 font-mono font-bold text-right text-white">${exp.amount.toLocaleString()}</td>
                                <td className="p-4">
                                    <button 
                                        onClick={() => categorize(exp.id)}
                                        className="text-slate-500 hover:text-white transition-colors"
                                    >
                                        <Tag size={16} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-2">Top Spend Category</h3>
                    <div className="text-2xl font-bold text-pink-400">Data Feeds</div>
                    <div className="text-sm text-slate-500">35% of monthly budget</div>
                </div>
            </div>
        </div>
    );
};

export default ExpenseManager;
