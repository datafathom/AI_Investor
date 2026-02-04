import React, { useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Activity, ShieldAlert } from 'lucide-react';
import useScenarioStore from '../../stores/scenarioStore';

/**
 * MonteCarloRefined - Post-shock path visualizer.
 * Phase 60: 10k path visualization for scenario shocks.
 */
const MonteCarloRefined = () => {
    const { recoveryProjection, impactResults, runRefinedMonteCarlo, activeScenario } = useScenarioStore();

    useEffect(() => {
        if (impactResults?.new_value && !recoveryProjection?.mcPaths) {
            runRefinedMonteCarlo(activeScenario?.id || 'shock', impactResults.new_value);
        }
    }, [impactResults]);

    if (!recoveryProjection?.mcPaths) return <div className="mc-loading">Initializing Post-Shock Simulation...</div>;

    const { p5, p50, p95 } = recoveryProjection.mcPaths;
    const data = p5.map((_, i) => ({
        day: i,
        p5: p5[i],
        p50: p50[i],
        p95: p95[i],
    }));

    return (
        <div className="monte-carlo-refined-widget">
            <div className="widget-header">
                <h3><Activity size={18} className="text-purple-400" /> Post-Shock Recovery Paths</h3>
                <Badge variant="outline">Confidence Interv. 95%</Badge>
            </div>

            <div style={{ width: '100%', height: 260 }}>
                <ResponsiveContainer>
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorMC" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                        <XAxis dataKey="day" hide />
                        <YAxis domain={['auto', 'auto']} hide />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#111', borderColor: '#333' }}
                            labelStyle={{ color: '#888' }}
                        />
                        <Area type="monotone" dataKey="p95" stroke="none" fill="#8b5cf6" fillOpacity={0.1} />
                        <Area type="monotone" dataKey="p5" stroke="none" fill="#111" fillOpacity={1} />
                        <Line type="monotone" dataKey="p50" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <div className="mc-footer-metrics">
                <div className="metric">
                    <span>Bull Case (P95)</span>
                    <strong className="text-green-400">${(p95[p95.length-1]/1000000).toFixed(2)}M</strong>
                </div>
                <div className="metric">
                    <span>Bear Case (P5)</span>
                    <strong className="text-red-400">${(p5[p5.length-1]/1000000).toFixed(2)}M</strong>
                </div>
            </div>
        </div>
    );
};

const Badge = ({ children, variant }) => (
    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${variant === 'outline' ? 'border-purple-500/50 text-purple-400' : 'bg-purple-500 text-white'}`}>
        {children}
    </span>
);

export default MonteCarloRefined;
