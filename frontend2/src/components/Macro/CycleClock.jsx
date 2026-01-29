import React from 'react';

const CycleClock = () => {
  return (
    <div className="p-8 bg-gray-900 rounded-full border-4 border-gray-800 h-64 w-64 mx-auto relative flex items-center justify-center">
      <div className="absolute top-4 font-bold text-gray-500 uppercase text-[10px]">Expansion</div>
      <div className="absolute right-4 font-bold text-gray-500 uppercase text-[10px]">Slowdown</div>
      <div className="absolute bottom-4 font-bold text-gray-500 uppercase text-[10px]">Contraction</div>
      <div className="absolute left-4 font-bold text-gray-500 uppercase text-[10px]">Recovery</div>
      
      {/* Clock Hand */}
      <div className="h-24 w-1 bg-blue-500 origin-bottom transform rotate-45 rounded-full shadow-neon-blue"></div>
      <div className="h-4 w-4 bg-gray-700 rounded-full border-2 border-blue-400 z-10"></div>
    </div>
  );
};

export default CycleClock;
