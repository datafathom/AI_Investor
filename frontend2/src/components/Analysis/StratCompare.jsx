import React from 'react';

const StratCompare = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">All Weather vs Benchmark</h3>
      <div className="space-y-4">
        <div className="flex items-center gap-4">
            <div className="flex-1 text-xs text-gray-400 font-mono">GROWTH (60/40)</div>
            <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 w-3/4"></div>
            </div>
            <div className="text-xs font-bold font-mono">1.25 SR</div>
        </div>
        <div className="flex items-center gap-4">
            <div className="flex-1 text-xs text-green-400 font-mono">ALL WEATHER (PARITY)</div>
            <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-full"></div>
            </div>
            <div className="text-xs font-bold font-mono">1.85 SR</div>
        </div>
      </div>
    </div>
  );
};

export default StratCompare;
