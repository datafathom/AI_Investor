import React from 'react';

const Claims = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4 uppercase text-xs">Initial Jobless Claims (Wkly)</h3>
      <div className="h-32 flex items-end gap-1 px-4 border-b border-gray-800">
        {[210, 215, 208, 225, 238, 245, 242, 255].map((v, i) => (
          <div 
            key={i} 
            className={`flex-1 rounded-t ${v > 240 ? 'bg-red-500/60' : 'bg-green-500/40'}`} 
            style={{ height: `${(v / 300) * 100}%` }}
          ></div>
        ))}
      </div>
      <div className="mt-2 flex justify-between text-[8px] text-gray-500 font-mono">
        <span>T-8 WKS</span>
        <span className="text-red-400 font-bold">TREND: RISING</span>
        <span>CURRENT: 255k</span>
      </div>
    </div>
  );
};

export default Claims;
