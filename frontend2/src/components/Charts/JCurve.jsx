import React from 'react';

const JCurve = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">The Private Equity J-Curve</h3>
      <div className="h-48 border-l border-gray-700 relative">
        <svg className="h-full w-full" viewBox="0 0 400 200">
            {/* Draw J-Curve path */}
            <path 
                d="M 0 80 Q 50 180 150 120 T 350 40" 
                fill="none" 
                stroke="#3B82F6" 
                strokeWidth="3"
            />
            <line x1="0" y1="100" x2="400" y2="100" stroke="#374151" strokeDasharray="4" />
        </svg>
        <div className="absolute top-2 right-2 text-[8px] text-green-400 font-bold uppercase">Harvesting Phase</div>
        <div className="absolute bottom-2 left-10 text-[8px] text-red-400 font-bold uppercase">Management Fees / Startup Cost</div>
      </div>
      <div className="mt-2 text-center text-[10px] text-gray-600">Vintage Year 2018 -> 2028 Exit Projection</div>
    </div>
  );
};

export default JCurve;
