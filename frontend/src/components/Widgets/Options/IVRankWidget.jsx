import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { TrendingUp, ArrowUp, ArrowDown, Activity } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';

const IVRankWidget = ({ ticker = 'AAPL' }) => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const res = await apiClient.get(`/options/${ticker}/iv-rank`);
                if (res.data.success) setData(res.data.data);
            } catch (e) {
                console.error(e);
            }
        };
        loadData();
    }, [ticker]);

    if (!data) return <div className="p-4 text-slate-500 animate-pulse">Scanning IV...</div>;

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-white font-bold flex items-center gap-2">
                        <Activity className="text-purple-500" size={18} /> IV Rank: {data.ticker}
                    </h3>
                    <div className="text-xs text-slate-500 uppercase font-bold mt-1 max-w-[200px] truncate">
                        52W Range: {(data.low_52w * 100).toFixed(0)}% - {(data.high_52w * 100).toFixed(0)}%
                    </div>
                </div>
                <div className={`text-right ${data.iv_rank > 50 ? 'text-red-400' : 'text-green-400'}`}>
                    <div className="text-2xl font-bold">{data.iv_rank.toFixed(0)}</div>
                    <div className="text-[10px] uppercase font-bold">Percentile</div>
                </div>
            </div>

            <div className="relative h-2 bg-slate-800 rounded-full mb-4 overflow-hidden">
                <div 
                    className={`absolute top-0 bottom-0 left-0 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500`}
                    style={{ width: `${data.iv_rank}%` }}
                />
            </div>

            <div className="grid grid-cols-2 gap-4 text-center">
                <div className="bg-slate-950 rounded p-2 border border-slate-800">
                    <div className="text-slate-500 text-xs uppercase">Current IV</div>
                    <div className="text-white font-mono font-bold">{(data.current_iv * 100).toFixed(1)}%</div>
                </div>
                <div className="bg-slate-950 rounded p-2 border border-slate-800">
                    <div className="text-slate-500 text-xs uppercase">Term Struct</div>
                    <div className="text-blue-400 font-bold text-xs uppercase">{data.term_structure}</div>
                </div>
            </div>
        </div>
    );
};

export default IVRankWidget;
