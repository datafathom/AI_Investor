import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { TrendingUp, Award, Zap } from 'lucide-react';

const DeFiYieldDashboard = () => {
    const [yields, setYields] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/defi/yields');
            if (res.data.success) setYields(res.data.data);
        };
        load();
    }, []);

    const stake = async (pool) => {
        const amount = prompt(`Enter amount to stake in ${pool}:`);
        if (amount) {
            await apiClient.post('/defi/stake', null, { params: { protocol_id: "mock_id", amount, asset: pool } });
            alert("Staking Transaction Broadcasted");
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Zap className="text-yellow-500" /> DeFi Yield Aggregator
                </h1>
                <p className="text-slate-500">Cross-Chain Yield Farming & Staking Opportunities</p>
            </header>

            <div className="grid grid-cols-1 gap-6">
                {yields.map((y, i) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex justify-between items-center hover:border-slate-700 transition-colors">
                        <div className="flex items-center gap-4">
                            <div className="bg-slate-800 p-3 rounded-full">
                                <TrendingUp className="text-emerald-500" size={24} />
                            </div>
                            <div>
                                <h3 className="font-bold text-white text-lg">{y.pool}</h3>
                                <div className="text-sm text-slate-400">{y.protocol}</div>
                            </div>
                        </div>

                        <div className="flex gap-8 text-center">
                            <div>
                                <div className="text-xs uppercase text-slate-500 font-bold">Base APY</div>
                                <div className="text-xl font-bold text-white">{y.apy}%</div>
                            </div>
                            <div>
                                <div className="text-xs uppercase text-slate-500 font-bold">Rewards</div>
                                <div className="text-xl font-bold text-yellow-400">+{y.rewards_apy}%</div>
                            </div>
                            <div>
                                <div className="text-xs uppercase text-slate-500 font-bold">Risk</div>
                                <div className={`text-xl font-bold ${y.risk === 'LOW' ? 'text-emerald-400' : 'text-red-400'}`}>{y.risk}</div>
                            </div>
                        </div>

                        <button 
                            onClick={() => stake(y.pool)}
                            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-6 rounded"
                        >
                            STAKE
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DeFiYieldDashboard;
