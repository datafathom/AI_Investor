import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BrainCircuit, GitCompare, AlertOctagon } from 'lucide-react';

const ModelValidator = () => {
    const [models, setModels] = useState([]);
    const [selectedDrift, setSelectedDrift] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/validation/models');
            if (res.data.success) setModels(res.data.data);
        };
        load();
    }, []);

    const checkDrift = async (id) => {
        const res = await apiClient.get(`/validation/models/${id}/drift`);
        if (res.data.success) setSelectedDrift(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BrainCircuit className="text-purple-500" /> AI Model Validator
                </h1>
                <p className="text-slate-500">Concept Drift Detection & Performance Monitoring</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Model Name</th>
                                <th className="p-4">Accuracy</th>
                                <th className="p-4">Status</th>
                                <th className="p-4">Drift</th>
                                <th className="p-4">Action</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {models.map(m => (
                                <tr key={m.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 font-bold text-white">{m.name}</td>
                                    <td className="p-4 font-mono text-cyan-400">{(m.accuracy * 100).toFixed(1)}%</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded text-xs font-bold ${
                                            m.status === 'PASSING' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-yellow-500/20 text-yellow-400'
                                        }`}>
                                            {m.status}
                                        </span>
                                    </td>
                                    <td className="p-4 text-slate-400">{m.drift}</td>
                                    <td className="p-4">
                                        <button 
                                            onClick={() => checkDrift(m.id)}
                                            className="text-slate-500 hover:text-white transition-colors"
                                        >
                                            <GitCompare size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <AlertOctagon className="text-orange-500" /> Drift Analysis
                    </h3>
                    {selectedDrift ? (
                        <div className="space-y-4">
                            <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                <span className="text-slate-300">PSI (Population Stability Index)</span>
                                <span className="text-white font-mono font-bold">{selectedDrift.psi}</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                <span className="text-slate-300">KL Divergence</span>
                                <span className="text-white font-mono font-bold">{selectedDrift.kl_divergence}</span>
                            </div>
                            <div className="mt-4 p-3 bg-blue-900/20 border border-blue-900/50 rounded text-center text-blue-200">
                                Model Status: <strong>{selectedDrift.status}</strong>
                            </div>
                        </div>
                    ) : (
                        <div className="text-slate-500 text-center py-12">Select a model to view drift metrics.</div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ModelValidator;
