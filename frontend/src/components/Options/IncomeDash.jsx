import React from 'react';

const IncomeDash = () => {
  return (
    <div className="p-4 bg-gray-900 border border-green-500/10 rounded-lg">
      <h3 className="text-green-400 font-bold text-sm mb-4">Derivatives Income Boost</h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 bg-black/40 rounded">
            <span className="text-[10px] text-gray-500 block">THETA HARVESTED</span>
            <span className="text-xl font-bold text-white">+$1,450</span>
        </div>
        <div className="p-3 bg-black/40 rounded">
            <span className="text-[10px] text-gray-500 block">EXTRA YIELD %</span>
            <span className="text-xl font-bold text-green-500">+1.2%</span>
        </div>
      </div>
      <button className="mt-4 w-full py-2 bg-green-900/20 border border-green-500/30 text-green-400 text-xs rounded font-bold">
        SCAN ACTIVE OPPORTUNITIES
      </button>
    </div>
  );
};

export default IncomeDash;
