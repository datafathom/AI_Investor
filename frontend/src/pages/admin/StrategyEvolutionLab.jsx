import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Dna, Play, Pause, RefreshCw, GitBranch } from 'lucide-react';

const StrategyEvolutionLab = () => {
    const [generation, setGeneration] = useState(0);
    const [population, setPopulation] = useState([]);
    const [evolutionActive, setEvolutionActive] = useState(false);

    const startEvolution = async () => {
        setEvolutionActive(true);
        try {
            const res = await apiClient.post('/evolution/start');
            if (res.data.success) {
                setGeneration(res.data.data.current_generation);
                loadStatus();
            }
        } catch (e) {
            console.error(e);
        }
    };

    const loadStatus = async () => {
        try {
            const res = await apiClient.get('/evolution/status');
            if (res.data.success) {
                setPopulation(res.data.data.history || []); // Using history as proxy for population visualization
            }
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Dna className="text-pink-500" /> Strategy Evolution Lab
                    </h1>
                    <p className="text-slate-500">Genetic Algorithms & Evolutionary Strategy Design</p>
                </div>
                <div className="flex gap-4">
                    <div className="text-right">
                        <div className="text-xs text-slate-500 uppercase">Generation</div>
                        <div className="text-2xl font-mono font-bold text-white">#{generation}</div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Control Panel */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-4">Evolution Controls</h3>
                    <div className="space-y-4">
                         <div className="flex justify-between text-sm">
                            <span className="text-slate-400">Population Size</span>
                            <span className="text-white">100</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-slate-400">Mutation Rate</span>
                            <span className="text-white">0.05</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-slate-400">Survival Rate</span>
                            <span className="text-white">0.20</span>
                        </div>
                        <button 
                            onClick={startEvolution}
                            disabled={evolutionActive}
                            className={`w-full py-3 rounded font-bold flex items-center justify-center gap-2 transition-colors ${
                                evolutionActive ? 'bg-slate-800 text-slate-500' : 'bg-pink-600 hover:bg-pink-500 text-white'
                            }`}
                        >
                            {evolutionActive ? <RefreshCw className="animate-spin" size={18} /> : <Play size={18} />}
                            {evolutionActive ? 'EVOLVING...' : 'START EVOLUTION'}
                        </button>
                    </div>
                </div>

                {/* Top Performers */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-4">Fitness Landscape</h3>
                    <div className="h-48 bg-slate-950 rounded flex items-center justify-center border border-slate-800/50 text-slate-600">
                        [3D Fitness Surface Widget Mockup]
                    </div>
                </div>
            </div>

            {/* Genome Viewer */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                    <GitBranch size={16} /> Recent Mutations
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="bg-slate-950 p-4 rounded border border-slate-800/50">
                            <div className="flex justify-between mb-2">
                                <span className="text-xs text-slate-500">Genome #{4920 + i}</span>
                                <span className="text-xs text-green-400 font-mono">Fit: 0.9{i}</span>
                            </div>
                            <div className="w-full h-1 bg-slate-800 rounded overflow-hidden flex">
                                <div className="bg-red-500 w-1/4" />
                                <div className="bg-blue-500 w-1/4" />
                                <div className="bg-green-500 w-1/4" />
                                <div className="bg-yellow-500 w-1/4" />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default StrategyEvolutionLab;
