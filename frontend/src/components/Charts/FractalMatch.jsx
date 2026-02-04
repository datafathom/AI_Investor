import React from 'react';

const FractalMatch = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">Macro Fractal Overlay (Current vs 1974)</h3>
      <div className="h-48 border border-gray-800 relative bg-black/40 rounded overflow-hidden">
        {/* Current Path */}
        <div className="absolute inset-0 flex items-center">
            <div className="w-full h-1 bg-blue-500/50 shadow-neon-blue"></div>
        </div>
        {/* Ghost (Fractal) Path */}
        <div className="absolute inset-0 flex items-center translate-y-4">
            <div className="w-full h-[2px] bg-red-500/20 border-t-2 border-dashed border-red-500/30"></div>
        </div>
        <div className="absolute top-2 right-4 text-[10px] text-red-400 font-mono italic">92% FRACTIONAL CORRELATION</div>
      </div>
    </div>
  );
};

export default FractalMatch;
