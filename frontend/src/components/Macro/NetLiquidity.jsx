import React from 'react';

const NetLiquidity = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4 uppercase">Central Bank Net Liquidity</h3>
      <div className="h-48 border-l border-b border-gray-700 relative">
        {/* Fed Bal Sheet - TGA - RRP line */}
        <div className="absolute inset-0 flex items-end">
            <svg viewBox="0 0 100 50" className="w-full h-full overflow-visible">
                <path d="M0 40 Q 25 35 50 30 T 100 10" fill="none" stroke="#60A5FA" strokeWidth="2" />
                <path d="M0 50 L 100 45" fill="none" stroke="#DB2777" strokeWidth="1" strokeDasharray="2" />
            </svg>
        </div>
        <div className="absolute top-2 right-4 text-[10px] text-blue-400 font-mono">NET_LIQ: $6.24T (Rising)</div>
      </div>
    </div>
  );
};

export default NetLiquidity;
