import React from 'react';

const ParamSliders = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg space-y-6">
      <h3 className="text-gray-400 font-bold mb-4 tracking-tighter">10k PATH SIM CORE</h3>
      
      <div>
        <label className="flex justify-between text-xs mb-2">
          <span>Drift (Mu)</span>
          <span className="text-blue-400">0.08</span>
        </label>
        <input type="range" className="w-full h-1 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-blue-500" />
      </div>

      <div>
        <label className="flex justify-between text-xs mb-2">
          <span>Vol (Sigma)</span>
          <span className="text-purple-400">0.15</span>
        </label>
        <input type="range" className="w-full h-1 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-purple-500" />
      </div>
      
      <button className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-xs font-mono rounded transition-colors">RE-SEED ENGINE</button>
    </div>
  );
};

export default ParamSliders;
