import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Send, Search, CheckCircle } from 'lucide-react';

const DonationManager = () => {
    const [recipients, setRecipients] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/philanthropy/recipients');
            if (res.data.success) setRecipients(res.data.data);
        };
        load();
    }, []);

    const donate = async (name) => {
        const amt = prompt(`Donation amount for ${name}:`);
        if (amt) {
            await apiClient.post('/philanthropy/donations/initiate', null, { params: { recipient: name, amount: amt } });
            alert("Donation Initiated for Approval");
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Send className="text-cyan-500" /> Grant & Donation Manager
                </h1>
                <p className="text-slate-500">Initiate Grants, Vet Charities & Track Approvals</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                        <CheckCircle size={18} className="text-emerald-500" /> Vetted Recipients
                    </h3>
                    <div className="space-y-4">
                        {recipients.map((r, i) => (
                            <div key={i} className="flex justify-between items-center p-4 bg-slate-950 rounded border border-slate-800">
                                <div>
                                    <div className="font-bold text-white">{r.name}</div>
                                    <div className="text-xs text-slate-500">EIN: {r.ein}</div>
                                </div>
                                <div className="flex items-center gap-4">
                                     <span className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded">
                                        {r.status.replace('_', ' ')}
                                     </span>
                                     <button 
                                        onClick={() => donate(r.name)}
                                        className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold py-1 px-3 rounded"
                                    >
                                        DONATE
                                     </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-center items-center text-center">
                    <Search size={48} className="text-slate-600 mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">Find New Charity</h3>
                    <p className="text-slate-500 text-sm mb-6 max-w-xs">
                        Search the IRS 501(c)(3) database or Charity Navigator to add new recipients.
                    </p>
                    <div className="flex w-full max-w-sm gap-2">
                        <input type="text" placeholder="Search by name or EIN..." className="flex-1 bg-slate-950 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-cyan-500" />
                        <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 rounded">
                            <Search size={18} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DonationManager;
