import React, { useState, useEffect, useMemo } from 'react';
import { StorageService } from '../utils/storageService';
import apiClient from '../services/apiClient';
import FitnessSurface3D from '../widgets/Evolution/FitnessSurface3D';
import LineageMap from '../widgets/Evolution/LineageMap';
import { useNotifications } from '../hooks/useNotifications';

const EvolutionDashboard = () => {
    const { notify } = useNotifications();
    const [status, setStatus] = useState('offline');
    const [stats, setStats] = useState(null);
    const [mutationRate, setMutationRate] = useState(0.1);
    const [labData, setLabData] = useState({
        fitnessLandscape: [], 
        lineage: []
    });

    useEffect(() => {
        const initLab = async () => {
            try {
                // Initialize Evolution Engine (Distillery)
                const startRes = await apiClient.post('/evolution/start');
                
                setStatus('online');
                const data = startRes.data;
                if (data) {
                    setStats(data);
                    setLabData(prev => ({ ...prev, fitnessLandscape: generateMockLandscape() }));
                } else {
                    setStatus('error');
                }
            } catch (e) {
                setStatus('error');
            }
        };
        
        initLab();
    }, []);

    const generateMockLandscape = () => Array.from({ length: 100 }, () => ({ x: Math.random(), y: Math.random(), fitness: Math.random() }));

    const handleSplice = async () => {
        // Mock parents matching API expectation
        const p1 = { id: 'agent_alpha', genes: { rsi_period: 14, rsi_buy: 30, rsi_sell: 70, stop_loss: 0.05 } };
        const p2 = { id: 'agent_beta', genes: { rsi_period: 21, rsi_buy: 25, rsi_sell: 75, stop_loss: 0.08 } };

        try {
            const res = await apiClient.post('/evolution/splice', { 
                parent1_id: p1.id, 
                parent2_id: p2.id,
                parent1_genes: p1.genes,
                parent2_genes: p2.genes
            });
            
            const result = res.data;
            if (result.status === 'success') {
                notify({ title: 'SPLICING SUCCESS', body: `Created Hybrid Genome`, type: 'success' });
                setLabData(prev => ({ 
                    ...prev, 
                    lineage: [...prev.lineage, { name: 'Hybrid', ...result.data }] 
                }));
            } else {
                notify({ title: 'SPLICING FAILED', body: result.message, type: 'error' });
            }
        } catch (e) {
            notify({ title: 'ERROR', body: 'Failed to splice', type: 'error' });
        }
    };

    const handleMutate = () => {
        notify({ title: 'MUTATION SIMULATED', body: 'Applying randomness to next generation...', type: 'info' });
        // Phase 37 API doesn't have an explicit 'mutate' endpoint exposed separate from 'evolve' loop
        // But we can simulate UI feedback
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-white">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tighter text-blue-400">EVOLUTION LAB <span className="text-xs align-top bg-blue-900 px-2 py-0.5 rounded text-white ml-2">PHASE 37</span></h1>
                    <p className="text-gray-400">Genetic Distillery & Hyperparameter Splicing</p>
                </div>
                <div className={`px-4 py-2 rounded ${status === 'online' ? 'bg-green-900/50 border border-green-500' : 'bg-red-900/50'}`}>
                    DISTILLERY: {status.toUpperCase()}
                </div>
            </header>

            <div className="grid grid-cols-12 gap-6">
                {/* Controls */}
                <div className="col-span-12 lg:col-span-4 space-y-6">
                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
                        <h3 className="text-xl font-bold mb-4">🧬 Splicing Bench (RSI Strategy)</h3>
                        <p className="text-sm text-gray-400 mb-4">Combining Alpha (14/30/70) & Beta (21/25/75)</p>
                        
                        <div className="flex gap-2 mb-4">
                            <div className="h-12 w-12 bg-blue-500/20 rounded-full border border-blue-400 flex items-center justify-center font-bold">α</div>
                            <div className="h-12 w-12 bg-purple-500/20 rounded-full border border-purple-400 flex items-center justify-center font-bold">β</div>
                        </div>

                        <button 
                            onClick={handleSplice}
                            className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded font-bold hover:brightness-110 transition-all shadow-[0_0_15px_rgba(59,130,246,0.5)]"
                        >
                            INITIATE CROSSOVER SEQUENCE
                        </button>
                    </div>

                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
                        <h3 className="text-xl font-bold mb-4">☢️ Mutation Rate</h3>
                        <div className="mb-6">
                             <div className="text-xs font-mono mb-2">CURRENT GEN: {stats?.current_generation || 0}</div>
                             <div className="text-xs font-mono text-green-400">BEST FITNESS: {stats?.best_performer?.fitness.toFixed(4) || '0.000'}</div>
                        </div>
                        <button 
                            onClick={handleMutate}
                            className="w-full py-2 border border-yellow-600 text-yellow-500 rounded font-bold hover:bg-yellow-600/10 transition-all"
                        >
                            TRIGGER NEXT GENERATION
                        </button>
                    </div>
                </div>

                {/* Visualization */}
                <div className="col-span-12 lg:col-span-8 space-y-6">
                    <div className="bg-gray-900/50 p-1 rounded-xl border border-gray-700 overflow-hidden relative">
                        <div className="absolute top-4 left-4 z-10 pointer-events-none">
                            <h3 className="font-bold bg-black/50 px-2 py-1 rounded backdrop-blur">FITNESS LANDSCAPE</h3>
                        </div>
                        <FitnessSurface3D data={labData.fitnessLandscape} />
                    </div>

                    <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700 h-[400px]">
                        <h3 className="text-lg font-bold mb-4">Lineage Tracking</h3>
                        <LineageMap data={labData.lineage} height={320} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EvolutionDashboard;
