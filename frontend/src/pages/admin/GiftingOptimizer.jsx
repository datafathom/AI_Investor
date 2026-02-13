import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Gift, PieChart } from 'lucide-react';

const GiftingOptimizer = () => {
    const [status, setStatus] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/wealth/gifting/status');
            if (res.data.success) setStatus(res.data.data);
        };
        load();
    }, []);

    const recordGift = async () => {
        const name = prompt("Recipient Name:");
        const amt = prompt("Amount:");
        if (name && amt) {
            await apiClient.post('/wealth/gifting/record', null, { params: { recipient: name, amount: amt } });
            alert("Gift Recorded");
            // Reload
        }
    };

    if (!status) return <div>Loading Gifting Data...</div>;

    const percentUsed = (status.used / status.annual_exclusion) * 100;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Gift className="text-pink-500" /> Gifting Optimizer
                    </h1>
                    <p className="text-slate-500">Annual Exclusions & Lifetime Exemption Tracker</p>
                </div>
                <button onClick={recordGift} className="bg-pink-600 hover:bg-pink-500 text-white font-bold py-2 px-4 rounded">
                    Record Gift
                </button>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-white">Annual Exclusion ({new Date().getFullYear()})</h3>
                        <span className="text-slate-500">${status.annual_exclusion.toLocaleString()} / recipient</span>
                    </div>
                    
                    <div className="mb-4">
                        <div className="flex justify-between text-sm mb-1">
                            <span className="text-slate-400">Total Utilized (Avg)</span>
                            <span className="text-white font-bold">{Math.round(percentUsed)}%</span>
                        </div>
                        <div className="h-4 bg-slate-950 rounded-full overflow-hidden">
                            <div className="h-full bg-pink-500" style={{ width: `${Math.min(percentUsed, 100)}%` }}></div>
                        </div>
                    </div>

                    <div className="space-y-2">
                        {status.recipients.map((r, i) => (
                            <div key={i} className="flex justify-between text-sm p-2 bg-slate-950 rounded">
                                <span className="text-white">{r.name}</span>
                                <span className="font-bold text-emerald-400">${r.amount.toLocaleString()}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                     <h3 className="font-bold text-white mb-4">Lifetime Exemption Used</h3>
                     <div className="flex items-center gap-6">
                        <PieChart size={64} className="text-slate-700" /> {/* Placeholder for real pie chart */}
                        <div>
                            <div className="text-3xl font-bold text-white">${status.lifetime_exemption_used.toLocaleString()}</div>
                            <div className="text-sm text-slate-500">of ${status.lifetime_exemption_total.toLocaleString()} Total</div>
                            <div className="text-xs text-emerald-500 mt-2 font-bold">
                                ${(status.lifetime_exemption_total - status.lifetime_exemption_used).toLocaleString()} REMAINING
                            </div>
                        </div>
                     </div>
                </div>
            </div>
        </div>
    );
};

export default GiftingOptimizer;
