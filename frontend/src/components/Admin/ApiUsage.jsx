import React from 'react';

const ApiUsage = () => {
  return (
    <div className="p-6 bg-gray-900 rounded border border-blue-500/20">
      <h2 className="text-xl font-bold text-white mb-6 font-mono">GATEWAY_METRICS</h2>
      <div className="space-y-4">
        <div className="flex justify-between items-center bg-black/30 p-3 rounded">
            <span className="text-sm font-bold text-gray-400">TradingView API</span>
            <span className="text-green-400 font-mono">1,452 / 10,000</span>
        </div>
        <div className="flex justify-between items-center bg-black/30 p-3 rounded border border-red-500/30">
            <span className="text-sm font-bold text-gray-400">OpenAI Tokens</span>
            <span className="text-red-500 font-mono">89% QUOTA REACHED</span>
        </div>
      </div>
      <button className="mt-6 w-full py-2 bg-gray-800 text-xs font-bold uppercase hover:bg-gray-700">Flush Gateway Cache</button>
    </div>
  );
};

export default ApiUsage;
