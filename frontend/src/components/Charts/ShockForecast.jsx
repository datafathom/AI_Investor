import React from 'react';

const ShockForecast = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-xl border border-blue-500/10">
      <h3 className="text-lg font-bold text-white mb-6">Scenario: Black Swan Recovery</h3>
      
      <div className="h-48 w-full bg-black/40 rounded flex items-end justify-center gap-1 p-2 border border-gray-800">
        {/* Simple recovery trajectory bars */}
        {[80, 75, 70, 72, 78, 85, 95, 105, 110].map((v, i) => (
          <div key={i} className="flex-1 bg-blue-500/40 border border-blue-500/50 rounded-t" style={{ height: `${v}%` }}></div>
        ))}
      </div>
      
      <div className="mt-4 flex justify-between text-[10px] text-gray-400 font-mono">
        <span>T-SHOCK</span>
        <span>RECOVERY: 8 MONTHS</span>
      </div>
    </div>
  );
};

export default ShockForecast;
