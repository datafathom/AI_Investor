import React from 'react';

const HotZones = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg h-64 border border-orange-500/20 flex flex-col">
      <h3 className="text-white font-bold text-sm mb-4 uppercase">Geopolitical Hot Zones</h3>
      <div className="flex-1 bg-black rounded relative">
        {/* Abstract World Map with Glows */}
        <div className="absolute top-1/3 left-1/4 h-8 w-8 bg-orange-500/20 rounded-full animate-ping"></div>
        <div className="absolute top-1/2 right-1/4 h-12 w-12 bg-red-500/20 rounded-full animate-pulse"></div>
      </div>
      <div className="mt-4 flex gap-4 text-[10px] uppercase font-bold">
        <span className="text-red-500">Conflict</span>
        <span className="text-orange-500">Sanctions</span>
        <span className="text-green-500">Stable</span>
      </div>
    </div>
  );
};

export default HotZones;
