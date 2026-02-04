import React from 'react';

const FundRotation = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">Hedge Fund Sector Rotation</h3>
      <div className="h-48 border-l border-b border-gray-700 relative flex items-center justify-around">
        <div className="text-center">
            <div className="h-32 w-8 bg-blue-500 rounded-t"></div>
            <div className="text-[10px] text-gray-500 mt-2">TECH</div>
        </div>
        <div className="text-center">
            <div className="h-12 w-8 bg-red-500 rounded-t"></div>
            <div className="text-[10px] text-gray-500 mt-2">FIN</div>
        </div>
        <div className="text-center">
            <div className="h-24 w-8 bg-green-500 rounded-t"></div>
            <div className="text-[10px] text-gray-500 mt-2">ENERGY</div>
        </div>
        <div className="absolute -left-6 top-0 h-full flex flex-col justify-between text-[8px] text-gray-600">
            <span>+20%</span>
            <span>0%</span>
            <span>-20%</span>
        </div>
      </div>
    </div>
  );
};

export default FundRotation;
