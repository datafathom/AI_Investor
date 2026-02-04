import React, { useEffect } from 'react';
import { TrendingUp, DollarSign, Users } from 'lucide-react';
import useInstitutionalStore from '../../stores/institutionalStore';
import { SimpleLineChart } from '../Charts/SimpleCharts';
import './RevenuePulse.css';

const RevenuePulse = ({ clientId = null }) => {
    const { revenueForecast, fetchRevenueForecast, loading } = useInstitutionalStore();

    useEffect(() => {
        fetchRevenueForecast(clientId);
    }, [clientId, fetchRevenueForecast]);

    if (!revenueForecast && loading) {
        return <div className="revenue-pulse-loading glass-premium">Loading Forecast...</div>;
    }

    const { current_fees, projected_fees, growth_rate, history } = revenueForecast || {
        current_fees: 0,
        projected_fees: 0,
        growth_rate: 0,
        history: []
    };

    // Transform history for SimpleLineChart
    const chartData = [
        {
            label: 'Fee Revenue',
            values: history.map(h => ({ x: h.date, y: h.amount }))
        }
    ];

    return (
        <div className="revenue-pulse glass-premium p-6 rounded-3xl border border-white/5">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-slate-400 text-xs uppercase tracking-widest font-bold flex items-center gap-2">
                        <DollarSign size={14} className="text-primary" />
                        Revenue Pulse
                    </h3>
                    <div className="text-3xl font-bold mt-1">
                        ${current_fees.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                        <span className="text-xs text-slate-500 font-normal ml-2">/ month</span>
                    </div>
                </div>
                <div className={`px-2 py-1 rounded-lg text-[10px] font-bold flex items-center gap-1 ${
                    growth_rate >= 0 ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
                }`}>
                    <TrendingUp size={10} />
                    {growth_rate > 0 ? '+' : ''}{(growth_rate * 100).toFixed(1)}%
                </div>
            </div>

            <div className="h-32 mb-6">
                <SimpleLineChart data={chartData} />
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">Projected (Q4)</div>
                    <div className="text-lg font-bold">${projected_fees.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
                </div>
                <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">AUM Efficiency</div>
                    <div className="text-lg font-bold">1.25%</div>
                </div>
            </div>
        </div>
    );
};

export default RevenuePulse;
