/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/System/QuotaHealthMeter.jsx
 * ROLE: API Quota & Rate Limit Monitor 
 * PURPOSE: Monitors external API provider usage to prevent downtime 
 *          due to rate limit exhaustion.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { Activity, Gauge, AlertCircle, CheckCircle, ExternalLink } from 'lucide-react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import './QuotaHealthMeter.css';

const QuotaHealthMeter = () => {
    const { quotas, fetchQuotas } = useSystemHealthStore();

    useEffect(() => {
        fetchQuotas();
        const interval = setInterval(fetchQuotas, 30000);
        return () => clearInterval(interval);
    }, [fetchQuotas]);

    const getStatusColor = (status) => {
        switch (status) {
            case 'critical': return 'text-red-500';
            case 'warning': return 'text-amber-500';
            case 'nominal': return 'text-emerald-500';
            default: return 'text-slate-500';
        }
    };

    return (
        <div className="quota-meter">
            <div className="quota-meter__header">
                <div className="flex items-center gap-2">
                    <Gauge size={16} className="text-blue-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Quota Health Meter</h3>
                </div>
                <div className="text-[10px] font-mono text-slate-500">
                    {Object.keys(quotas).length} Providers
                </div>
            </div>

            <div className="quota-meter__list scrollbar-hide">
                {Object.entries(quotas).map(([provider, stats]) => (
                    <div key={provider} className="quota-meter__item">
                        <div className="flex justify-between items-center mb-1.5">
                            <span className="text-[10px] font-black text-white">{provider}</span>
                            <span className={`text-[10px] font-bold ${getStatusColor(stats.status)}`}>
                                {stats.percent_day}%
                            </span>
                        </div>
                        <div className="quota-meter__progress-bg">
                            <div 
                                className={`quota-meter__progress-fill ${stats.status === 'nominal' ? 'bg-blue-500' : stats.status === 'warning' ? 'bg-amber-500' : 'bg-red-500'}`}
                                style={{ width: `${stats.percent_day}%` }}
                            />
                        </div>
                        <div className="flex justify-between mt-1 text-[8px] text-slate-500 font-mono">
                            <span>MIN: {stats.minute_used}/{stats.minute_limit}</span>
                            <span>DAY: {stats.day_used}/{stats.day_limit}</span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="quota-meter__footer">
                <div className="flex items-center gap-2 text-[9px] text-emerald-500">
                    <CheckCircle size={10} />
                    <span>Auto-failover enabled</span>
                </div>
                <button 
                    onClick={fetchQuotas} 
                    className="text-[9px] text-slate-500 hover:text-white transition-colors"
                >
                    REFRESH
                </button>
            </div>
        </div>
    );
};

export default QuotaHealthMeter;
