import React from 'react';
import { Dna, Share2, Copy } from 'lucide-react';

const AgentDNAViewer = () => {
    // Mock DNA Structure
    const dnaSegments = [
        { id: 'risk_tolerance', name: 'Risk Tolerance', value: '0.45', type: 'float' },
        { id: 'time_horizon', name: 'Time Horizon', value: '4h', type: 'string' },
        { id: 'asset_preference', name: 'Asset Class', value: ['CRYPTO', 'TECH'], type: 'array' },
        { id: 'stop_loss_tightness', name: 'Stop Loss', value: '0.02', type: 'float' },
        { id: 'take_profit_aggressiveness', name: 'Take Profit', value: '0.08', type: 'float' }
    ];

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Dna className="text-cyan-500" /> Agent DNA Viewer
                </h1>
                <p className="text-slate-500">Genetic Blueprint & Parameter Introspection</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-4xl">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="font-bold text-white">Genome Sequence: AGENT_ALPHA_V4</h3>
                    <button className="text-cyan-400 hover:text-cyan-300 flex items-center gap-2 text-sm font-bold">
                        <Share2 size={14} /> EXPORT DNA
                    </button>
                </div>

                <div className="space-y-1">
                    {dnaSegments.map((gene, i) => (
                        <div key={i} className="flex items-center p-3 hover:bg-slate-800 rounded transition-colors group">
                            <div className="w-12 h-12 rounded bg-slate-950 border border-slate-800 flex items-center justify-center mr-4 text-slate-600 font-mono text-xs">
                                {i.toString().padStart(2, '0')}
                            </div>
                            <div className="flex-1">
                                <div className="text-sm font-bold text-slate-300">{gene.name}</div>
                                <div className="text-xs text-slate-600 font-mono">{gene.id}</div>
                            </div>
                            <div className="text-right">
                                <span className="font-mono text-cyan-400 bg-cyan-950/30 px-2 py-1 rounded border border-cyan-900">
                                    {Array.isArray(gene.value) ? gene.value.join(', ') : gene.value}
                                </span>
                            </div>
                            <button className="ml-4 opacity-0 group-hover:opacity-100 transition-opacity text-slate-500 hover:text-white">
                                <Copy size={16} />
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AgentDNAViewer;
