import React from 'react';

const FlowHeat = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg border border-purple-500/20">
      <h3 className="text-purple-400 font-bold mb-4 text-xs">OPTION FLOW HEATMAP</h3>
      <div className="grid grid-cols-4 gap-2">
        {['TSLA', 'SPY', 'NVDA', 'AMD', 'AAPL', 'GOOG', 'AMZN', 'META'].map(t => (
            <div key={t} className={`h-12 flex items-center justify-center rounded font-bold text-xs ${
                Math.random() > 0.5 ? 'bg-green-600/40 border border-green-500' : 'bg-red-600/20 border border-red-500/40 text-red-500'
            }`}>
                {t}
            </div>
        ))}
      </div>
    </div>
  );
};

export default FlowHeat;
