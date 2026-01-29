import React from 'react';

const StopVisualizer = ({ entry, stop, currentPrice }) => {
  return (
    <div className="p-4 bg-gray-900 rounded border border-gray-700">
      <h4 className="text-white font-bold mb-2">Structure Visualizer</h4>
      <div className="relative h-20 w-full bg-gray-800 rounded">
        {/* Simple visual representation */}
        <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-600"></div>
        <div className="absolute top-1/2 left-1/4 w-2 h-4 bg-green-500" title="Entry"></div>
        <div className="absolute top-1/2 left-3/4 w-2 h-4 bg-red-500" title="Stop Loss"></div>
      </div>
      <div className="mt-2 text-sm text-gray-400 flex justify-between">
        <span>Entry: {entry}</span>
        <span>Stop: {stop}</span>
      </div>
    </div>
  );
};

export default StopVisualizer;
