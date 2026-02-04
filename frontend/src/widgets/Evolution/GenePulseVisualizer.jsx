/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Evolution/GenePulseVisualizer.jsx
 * ROLE: Micro-Genomic Vitality Monitor
 * PURPOSE: Visualizes the activation pulse and mutation instability 
 *          of an AI Agent's specific gene markers.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { Activity, ShieldAlert, Zap, TrendingUp, Info, Dna } from 'lucide-react';
import useEvolutionStore from '../../stores/evolutionStore';
import './GenePulseVisualizer.css';

const GenePulseVisualizer = ({ agentId = 'AGENT-MOCK', genes = {} }) => {
    const { genePulse, fetchGenePulse } = useEvolutionStore();

    useEffect(() => {
        if (agentId && Object.keys(genes).length > 0) {
            fetchGenePulse(agentId, genes);
            const interval = setInterval(() => fetchGenePulse(agentId, genes), 5000);
            return () => clearInterval(interval);
        }
    }, [agentId, genes, fetchGenePulse]);

    if (!genePulse) {
        return (
            <div className="gene-pulse flex items-center justify-center">
                <span className="text-slate-500 text-[10px] animate-pulse">SEQUENCING...</span>
            </div>
        );
    }

    return (
        <div className="gene-pulse">
            <div className="gene-pulse__header">
                <div className="flex items-center gap-2">
                    <Dna size={16} className="text-emerald-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Gene Pulse</h3>
                </div>
                <div className="text-[10px] font-mono text-emerald-400">
                    Vitality: <span className="text-white">{(genePulse.overall_vitality * 100).toFixed(1)}%</span>
                </div>
            </div>

            <div className="gene-pulse__stream">
                {genePulse.pulse.map((p, idx) => (
                    <div key={idx} className="gene-pulse__marker">
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-[9px] text-slate-500 uppercase font-bold">{p.gene}</span>
                            <span className={`text-[9px] font-mono ${p.status === 'stable' ? 'text-emerald-500' : 'text-amber-500'}`}>
                                {p.status}
                            </span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="gene-pulse__sparkline">
                                <Activity 
                                    size={14} 
                                    className={`text-emerald-400/30 transition-all duration-300`}
                                    style={{ 
                                        transform: `scale(${1 + p.activation})`,
                                        opacity: 0.2 + p.activation 
                                    }}
                                />
                            </div>
                            <div className="flex-1">
                                <div className="text-[10px] text-white font-mono">{p.value}</div>
                                <div className="gene-pulse__instability-bg">
                                    <div 
                                        className={`gene-pulse__instability-fill ${p.status === 'stable' ? 'bg-emerald-500' : 'bg-amber-500'}`}
                                        style={{ width: `${p.instability * 200}%` }}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="gene-pulse__footer">
                <div className="flex items-center gap-1.5 text-[8px] text-slate-600">
                    <Info size={10} />
                    <span>MUTATION ANNOTATION: VER {genePulse.timestamp}</span>
                </div>
            </div>
        </div>
    );
};

export default GenePulseVisualizer;
