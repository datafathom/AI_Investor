import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Layers, Activity, AlertTriangle } from 'lucide-react';

const WalkForwardAnalyzer = () => {
    const [running, setRunning] = useState(false);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Layers className="text-indigo-500" /> Walk-Forward Analyzer
                </h1>
                <p className="text-slate-500">Robustness Testing via Rolling Window Optimization</p>
            </header>
            
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-center h-[400px]">
                <Activity size={64} className="text-slate-700 mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Optimization Matrix</h2>
                <p className="text-slate-500 max-w-md">
                    Configure In-Sample (IS) and Out-of-Sample (OOS) windows to verify strategy stability across changing market regimes.
                </p>
                <button className="mt-6 bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-3 rounded-full font-bold">
                    CONFIGURE WALK-FORWARD
                </button>
            </div>
        </div>
    );
};

export default WalkForwardAnalyzer;
