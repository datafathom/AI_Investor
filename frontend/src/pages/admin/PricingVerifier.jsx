import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { DollarSign, Search, AlertCircle } from 'lucide-react';

const PricingVerifier = () => {
    const [checks, setChecks] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/valuation/pricing-check');
            if (res.data.success) setChecks(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <DollarSign className="text-emerald-500" /> Pricing Verifier
                </h1>
                <p className="text-slate-500">Cross-Source Validation & Bad Tick Detection</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Provider A</th>
                            <th className="p-4">Provider B</th>
                            <th className="p-4">Variance</th>
                            <th className="p-4">Status</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {checks.map((c, i) => (
                            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{c.symbol}</td>
                                <td className="p-4 font-mono text-slate-300">${c.provider_a.toFixed(2)}</td>
                                <td className="p-4 font-mono text-slate-300">${c.provider_b.toFixed(2)}</td>
                                <td className={`p-4 font-mono font-bold ${c.diff > 0.1 ? 'text-red-400' : 'text-slate-500'}`}>
                                    {c.diff.toFixed(2)}
                                </td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold flex items-center gap-1 w-fit ${
                                        c.status === 'MATCH' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                                    }`}>
                                        {c.status === 'MATCH' ? 'OK' : <AlertCircle size={12} />} {c.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PricingVerifier;
