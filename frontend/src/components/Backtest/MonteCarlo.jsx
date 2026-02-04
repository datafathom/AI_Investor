import React from 'react';

const MonteCarlo = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg h-96 flex flex-col">
      <h3 className="text-white font-bold mb-2">10k Path Cloud Visualizer</h3>
      <div className="flex-1 bg-black rounded relative overflow-hidden">
        {/* Simplified path visualization using CSS gradients or pseudo-elements to simulate the cloud */}
        <div className="absolute inset-0 bg-gradient-to-tr from-green-500/10 via-transparent to-red-500/10 opacity-30"></div>
        <div className="absolute top-1/2 left-0 w-full h-[1px] bg-white/20"></div>
        <div className="absolute text-[10px] text-gray-600 bottom-2 right-2 italic">60 FPS Render Engine</div>
      </div>
      <div className="mt-2 flex justify-between text-xs text-gray-400">
        <span>-50% (Ruin)</span>
        <span className="text-green-500">+1200% (Target)</span>
      </div>
    </div>
  );
};

export default MonteCarlo;
