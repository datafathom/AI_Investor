import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { GitPullRequest, CheckSquare, MessageSquare } from 'lucide-react';

const DiscrepancyResolution = () => {
    const [breaks, setBreaks] = useState([]);

    useEffect(() => {
        loadBreaks();
    }, []);

    const loadBreaks = async () => {
        const res = await apiClient.get('/audit/discrepancies');
        if (res.data.success) setBreaks(res.data.data);
    };

    const resolve = async (id) => {
        const comment = prompt("Enter resolution comment:");
        if (!comment) return;
        await apiClient.post(`/audit/discrepancies/${id}/resolve`, null, { params: { comment } });
        loadBreaks();
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <GitPullRequest className="text-orange-500" /> Discrepancy Resolution
                </h1>
                <p className="text-slate-500">Break Management Workbench</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Type</th>
                            <th className="p-4">Account</th>
                            <th className="p-4">Details</th>
                            <th className="p-4">Age</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {breaks.map(b => (
                            <tr key={b.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{b.type.replace('_', ' ')}</td>
                                <td className="p-4 text-slate-300">{b.account}</td>
                                <td className="p-4">
                                    {b.symbol && <span className="text-cyan-400 font-mono mr-2">{b.symbol}</span>}
                                    {b.diff_qty && <span className="text-red-400">Qty Diff: {b.diff_qty}</span>}
                                    {b.amount && <span className="text-red-400">Amt: ${b.amount}</span>}
                                </td>
                                <td className="p-4 text-slate-500">{b.age}</td>
                                <td className="p-4">
                                    <span className="bg-orange-500/20 text-orange-400 px-2 py-1 rounded text-xs font-bold">{b.status}</span>
                                </td>
                                <td className="p-4">
                                    <button 
                                        onClick={() => resolve(b.id)}
                                        className="text-xs bg-emerald-900/30 hover:bg-emerald-900/50 text-emerald-400 border border-emerald-900/50 px-3 py-1 rounded flex items-center gap-1"
                                    >
                                        <CheckSquare size={12} /> RESOLVE
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {breaks.length === 0 && (
                            <tr>
                                <td colSpan="6" className="p-8 text-center text-slate-500">No active discrepancies found.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DiscrepancyResolution;
