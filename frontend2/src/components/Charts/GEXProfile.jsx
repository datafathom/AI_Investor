import React from 'react';

const GEXProfile = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">SPX GEX STRIKE PROFILE</h3>
      
      <div className="h-48 w-full flex items-end gap-1 px-4 border-b border-gray-800">
        {/* Mocked positive and negative gamma bars */}
        {[5, 12, 18, 45, 8, -5, -2, -15, -40, -12, -4].map((v, i) => (
          <div key={i} className="flex-1 relative group">
            <div 
              className={`w-full rounded-t ${v > 0 ? 'bg-green-500/60' : 'bg-red-500/60'}`} 
              style={{ height: `${Math.abs(v) * 2}%`, transform: v < 0 ? 'translateY(100%) scaleY(-1)' : 'none' }}
            ></div>
            <div className="absolute -top-6 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 text-[10px] text-gray-500">
              {4800 + (i * 25)}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 flex justify-between text-[10px] text-gray-400 font-mono">
        <span>STRIKES (PUTS)</span>
        <span className="text-yellow-500 font-bold">ZERO GAMMA: 4850</span>
        <span>STRIKES (CALLS)</span>
      </div>
    </div>
  );
};

export default GEXProfile;
