import React from 'react';

const MainView = () => {
  return (
    <div className="fixed inset-0 bg-black text-white p-12 flex flex-col font-mono">
      <div className="flex justify-between items-start mb-12 border-b border-gray-800 pb-8">
        <div>
            <h1 className="text-6xl font-black tracking-tighter">AI INVESTMENT DIRECTORATE</h1>
            <p className="text-gray-500 text-sm mt-2 font-bold uppercase tracking-[10px]">Strategic Command Interface (v1.0)</p>
        </div>
        <div className="text-right">
            <div className="text-6xl font-bold text-green-400">$12,450,210</div>
            <div className="text-xs text-gray-600">TOTAL CONSOLIDATED NAV</div>
        </div>
      </div>
      
      <div className="flex-1 grid grid-cols-3 gap-12">
        <div className="border border-gray-800 p-8 rounded-2xl bg-gray-900/10">
            <h3 className="text-gray-600 mb-4 font-bold">REGIME_STATUS</h3>
            <div className="text-3xl text-orange-500 font-bold">INFLATIONARY_EXPANSION</div>
            <p className="mt-4 text-xs text-gray-400 italic leading-relaxed">Matrix detected structural ROC shift in CPI. Long commodities active. Gold hedges 15%.</p>
        </div>
        
        <div className="border border-gray-800 p-8 rounded-2xl bg-gray-900/10">
             <h3 className="text-gray-600 mb-4 font-bold">RISK_ENGINE</h3>
             <div className="text-3xl text-blue-400 font-bold">OPTIMAL_EQUILIBRIUM</div>
             <p className="mt-4 text-xs text-gray-400 italic">No hard guardrails triggered. Zero Gamma level at 4850. VIX stable at 14.5.</p>
        </div>

        <div className="border border-gray-800 p-8 rounded-2xl bg-gray-900/10 flex flex-col justify-between">
             <h3 className="text-gray-600 mb-4 font-bold">PANIC_DEFAULTS</h3>
             <button className="flex-1 bg-red-900/50 border-4 border-red-600 text-red-500 font-black text-4xl hover:bg-red-600 hover:text-white transition-all rounded-xl">
                FLATTEN_ALL
             </button>
        </div>
      </div>
      
      <div className="mt-12 h-16 bg-gray-900 border-t border-gray-800 flex items-center px-12 italic text-gray-400 text-xs">
         <ctrl94> LLM_SYNC: Market sentiment pivot detected in earnings calls ($XOM, $CVX). Structural rotation to energy continuing...
      </div>
    </div>
  );
};

export default MainView;
