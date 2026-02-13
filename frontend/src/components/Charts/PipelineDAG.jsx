import React from 'react';

const PipelineDAG = ({ pipeline }) => {
  // Simple Mock DAG visualization
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 relative overflow-hidden min-h-[300px] flex items-center justify-center">
      <div className="absolute top-4 left-4 text-xs font-mono text-slate-500">DAG VISUALIZATION: {pipeline?.name}</div>
      
      <div className="flex items-center gap-8">
        <div className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-full bg-cyan-900/40 border border-cyan-500/50 flex items-center justify-center text-cyan-400">
                Src
            </div>
            <span className="text-xs text-slate-400">Source</span>
        </div>

        <div className="h-[2px] w-16 bg-slate-700 relative">
            <div className="absolute -top-1 left-1/2 w-2 h-2 bg-slate-500 rounded-full animate-ping"></div>
        </div>

        <div className="flex flex-col items-center gap-2">
             <div className="w-12 h-12 rounded-full bg-indigo-900/40 border border-indigo-500/50 flex items-center justify-center text-indigo-400">
                Proc
            </div>
            <span className="text-xs text-slate-400">Processing</span>
        </div>

        <div className="h-[2px] w-16 bg-slate-700"></div>

        <div className="flex flex-col items-center gap-2">
             <div className="w-12 h-12 rounded-full bg-emerald-900/40 border border-emerald-500/50 flex items-center justify-center text-emerald-400">
                DB
            </div>
            <span className="text-xs text-slate-400">Storage</span>
        </div>
      </div>
    </div>
  );
};

export default PipelineDAG;
