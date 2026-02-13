import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Beaker, BarChart2, CheckCircle } from 'lucide-react';

const PromptABTester = () => {
    const [variants, setVariants] = useState([{ name: 'A', content: '' }, { name: 'B', content: '' }]);
    const [testId, setTestId] = useState(null);
    const [results, setResults] = useState(null);

    const handleStartTest = async () => {
        try {
            const res = await apiClient.post('/meta/prompts/test', { variants });
            if (res.data.success) {
                setTestId(res.data.data.test_id);
                // Simulate results loading
                setTimeout(loadResults, 2000);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const loadResults = async () => {
        // Mock fetch results
        setResults({
            winner: 'Variant B',
            confidence: 0.95,
            metrics: { 'Variant A': 0.65, 'Variant B': 0.82 }
        });
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Beaker className="text-yellow-500" /> Prompt A/B Tester
                </h1>
                <p className="text-slate-500">optimize Agent Cognition</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {variants.map((v, i) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <label className="block text-white font-bold mb-2">Variant {v.name}</label>
                        <textarea
                            className="w-full h-48 bg-slate-950 border border-slate-800 rounded p-4 text-sm font-mono text-slate-300 focus:border-yellow-500 outline-none"
                            placeholder="Enter system prompt..."
                            value={v.content}
                            onChange={(e) => {
                                const newVars = [...variants];
                                newVars[i].content = e.target.value;
                                setVariants(newVars);
                            }}
                        />
                    </div>
                ))}
            </div>

            <div className="text-center mb-8">
                <button 
                    onClick={handleStartTest}
                    disabled={!!testId}
                    className="bg-yellow-600 hover:bg-yellow-500 text-black font-bold px-8 py-3 rounded-full transition-all hover:scale-105"
                >
                    {testId ? 'TEST RUNNING...' : 'START COMPARISON'}
                </button>
            </div>

            {results && (
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center animate-fade-in">
                    <h3 className="text-2xl font-bold text-white mb-4">Results</h3>
                    <div className="inline-flex items-center gap-2 bg-green-500/20 text-green-400 px-4 py-2 rounded-full border border-green-500/30 mb-6">
                        <CheckCircle size={20} /> Winner: {results.winner} ({(results.confidence * 100).toFixed(0)}% Confidence)
                    </div>

                    <div className="flex justify-center gap-12">
                        {Object.entries(results.metrics).map(([key, val]) => (
                            <div key={key} className="text-center">
                                <div className="text-slate-500 text-sm uppercase mb-1">{key} Score</div>
                                <div className="text-4xl font-mono font-bold text-white">{(val * 100).toFixed(1)}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default PromptABTester;
