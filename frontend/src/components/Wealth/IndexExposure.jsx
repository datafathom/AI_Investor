import React from 'react';

const IndexExposure = ({ beta, holdings }) => {
  return (
    <div className="p-4 bg-gray-800 rounded mt-4">
      <h3 className="text-blue-400 font-bold mb-2">Index Exposure</h3>
      <div className="flex items-center space-x-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-white">{beta.toFixed(2)}</div>
          <div className="text-xs text-gray-500">Portfolio Beta</div>
        </div>
        <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className={`h-full ${beta > 1.2 ? 'bg-red-500' : 'bg-green-500'}`} 
            style={{ width: `${Math.min(beta * 50, 100)}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default IndexExposure;
