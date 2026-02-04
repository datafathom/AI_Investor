import React from 'react';

const UnvestedValue = ({ totalValue }) => {
  return (
    <div className="p-6 bg-gradient-to-br from-yellow-900/20 to-orange-900/20 border border-yellow-500/20 rounded-xl">
      <h3 className="text-yellow-500 font-bold text-xs uppercase mb-2">Golden Handcuff Value</h3>
      <div className="text-3xl font-bold text-white mb-2">${totalValue?.toLocaleString()}</div>
      <p className="text-[10px] text-gray-500">Unvested RSUs & Founder Equity subject to cliffs.</p>
      
      <div className="mt-4 h-2 bg-gray-800 rounded-full overflow-hidden">
        <div className="h-full bg-yellow-500 w-1/3"></div>
      </div>
      <div className="mt-1 flex justify-between text-[8px] text-gray-500 uppercase">
        <span>Vested</span>
        <span>$4.2M Locked</span>
      </div>
    </div>
  );
};

export default UnvestedValue;
