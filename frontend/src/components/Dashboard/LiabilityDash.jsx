import React from 'react';

const LiabilityDash = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-xl border border-red-500/10">
      <h2 className="text-xl font-bold text-white mb-6">Liability Management</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-gray-800 rounded border-l-4 border-green-500">
            <span className="text-[10px] text-gray-500 font-mono">FIXED MORTGAGE (2.8%)</span>
            <div className="text-xl font-bold">$450,000</div>
            <div className="text-[10px] text-green-400">BEATING INFLATION</div>
        </div>
        <div className="p-4 bg-gray-800 rounded border-l-4 border-red-500">
            <span className="text-[10px] text-gray-500 font-mono">CC BALANCE (19.5%)</span>
            <div className="text-xl font-bold">$12,400</div>
            <div className="text-[10px] text-red-400">MATH_DANGER: PAY DOWN NOW</div>
        </div>
      </div>
      
      <button className="w-full py-2 bg-blue-900/40 border border-blue-500/50 text-blue-300 rounded text-xs">
        CALCULATE SBLOC SWAP
      </button>
    </div>
  );
};

export default LiabilityDash;
