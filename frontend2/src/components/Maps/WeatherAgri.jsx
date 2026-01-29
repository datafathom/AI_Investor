import React from 'react';

const WeatherAgri = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4 uppercase">Agricultural Moisture Map</h3>
      <div className="h-48 border border-gray-800 relative bg-green-900/10 rounded overflow-hidden">
        {/* Heatmap overlay on growing regions */}
        <div className="absolute top-1/4 left-1/3 h-16 w-16 bg-red-500/30 rounded-full blur-xl"></div>
        <div className="absolute top-2/3 right-1/4 h-24 w-24 bg-green-500/20 rounded-full blur-2xl"></div>
        
        <div className="absolute bottom-2 left-4 text-[10px] text-red-400 font-bold">DROUGHT: MATO GROSSO, BRAZIL</div>
      </div>
    </div>
  );
};

export default WeatherAgri;
