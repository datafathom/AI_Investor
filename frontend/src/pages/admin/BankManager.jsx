import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Building, Phone, Shield } from 'lucide-react';

const BankManager = () => {
    const [banks, setBanks] = useState([]);
    const [selectedBank, setSelectedBank] = useState(null);
    const [fees, setFees] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/banking/relationships');
            if (res.data.success) setBanks(res.data.data);
        };
        load();
    }, []);

    const viewFees = async (id) => {
        setSelectedBank(id);
        const res = await apiClient.get(`/banking/fees/${id}`);
        if (res.data.success) setFees(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Building className="text-indigo-500" /> Bank Relationship Manager
                </h1>
                <p className="text-slate-500">Institutional Partners & Fee Structures</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="space-y-4">
                    {banks.map(bank => (
                        <div 
                            key={bank.id} 
                            onClick={() => viewFees(bank.id)}
                            className={`p-6 bg-slate-900 border rounded-xl cursor-pointer transition-colors ${
                                selectedBank === bank.id ? 'border-indigo-500' : 'border-slate-800 hover:border-slate-700'
                            }`}
                        >
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-xl font-bold text-white">{bank.name}</h3>
                                <Shield className="text-emerald-500" size={20} />
                            </div>
                            <div className="space-y-2 text-sm text-slate-400">
                                <div className="flex items-center gap-2">
                                    <Phone size={14} /> {bank.rep} ({bank.phone})
                                </div>
                                <div>FDIC Coverage: <span className="text-emerald-400 font-bold">${bank.fdic_coverage.toLocaleString()}</span></div>
                            </div>
                        </div>
                    ))}
                </div>

                {selectedBank && fees && (
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <h3 className="font-bold text-white mb-6">Fee Schedule</h3>
                        <table className="w-full text-left">
                            <thead className="text-slate-500 text-xs uppercase border-b border-slate-800">
                                <tr>
                                    <th className="pb-2">Service</th>
                                    <th className="pb-2 text-right">Fee</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {fees.map((f, i) => (
                                    <tr key={i} className="border-b border-slate-800 last:border-0">
                                        <td className="py-3 text-slate-300">{f.service}</td>
                                        <td className="py-3 text-right font-mono text-white">${f.fee.toFixed(2)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default BankManager;
