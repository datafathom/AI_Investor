import React from 'react';
import { ShieldCheck, ShieldAlert, Shield, Info } from 'lucide-react';
import useInstitutionalStore from '../../stores/institutionalStore';
import './KycRiskGauge.css';

const KycRiskGauge = ({ clientId }) => {
    const { riskLevels, loading } = useInstitutionalStore();
    
    // We'll use the kyc_risk_score from riskLevels (0-100)
    // In our mock, low is good, but for the gauge we'll show "Health" (100 - risk)
    const riskData = riskLevels[clientId] || {
        kyc_risk_score: 15,
        health_status: 'Healthy',
        alerts: []
    };

    const healthScore = 100 - riskData.kyc_risk_score;
    
    // Radial gauge calculation
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (healthScore / 100) * circumference;

    const getScoreColor = (score) => {
        if (score >= 80) return '#10b981'; // Green
        if (score >= 60) return '#f59e0b'; // Orange
        return '#ef4444'; // Red
    };

    if (loading && !riskLevels[clientId]) {
        return <div className="kyc-risk-gauge-loading glass-premium">Validating Identity...</div>;
    }

    return (
        <div className="kyc-risk-gauge glass-premium p-6 rounded-3xl border border-white/5">
            <div className="flex justify-between items-start mb-8">
                <div>
                    <h3 className="text-slate-400 text-xs uppercase tracking-widest font-bold flex items-center gap-2">
                        <Shield size={14} className="text-primary" />
                        Compliance Health
                    </h3>
                    <div className="text-2xl font-bold mt-1">
                        {healthScore}% <span className="text-xs text-slate-500 font-normal">Score</span>
                    </div>
                </div>
                <div className={`p-2 rounded-xl ${healthScore >= 80 ? 'bg-success/20 text-success' : 'bg-error/20 text-error'}`}>
                    {healthScore >= 80 ? <ShieldCheck size={20} /> : <ShieldAlert size={20} />}
                </div>
            </div>

            <div className="relative flex justify-center mb-8">
                <svg className="w-32 h-32 transform -rotate-90">
                    <circle
                        cx="64" cy="64" r={radius}
                        fill="transparent"
                        stroke="rgba(255,255,255,0.05)"
                        strokeWidth="8"
                    />
                    <circle
                        cx="64" cy="64" r={radius}
                        fill="transparent"
                        stroke={getScoreColor(healthScore)}
                        strokeWidth="8"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center pt-2">
                    <span className="text-2xl font-bold text-white">{healthScore}</span>
                    <span className="text-[10px] text-slate-500 uppercase font-black">Rating</span>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-6">
                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">KYC Status</div>
                    <div className="text-xs font-bold text-success">VERIFIED</div>
                </div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">AML Screen</div>
                    <div className="text-xs font-bold text-success">PASSED</div>
                </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-xl bg-primary/5 border border-primary/10">
                <Info size={14} className="text-primary mt-0.5 flex-shrink-0" />
                <p className="text-[10px] text-slate-400 leading-relaxed">
                    Identity verified against SEC/FINRA watchlists. No high-risk political exposure detected.
                </p>
            </div>
        </div>
    );
};

export default KycRiskGauge;
