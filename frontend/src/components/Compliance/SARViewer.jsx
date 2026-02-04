import React from 'react';

const SARViewer = () => {
  return (
    <div className="p-4 bg-gray-900 border border-red-500/20 rounded-lg">
      <h3 className="text-red-400 font-bold mb-4 flex items-center gap-2">
        <span>SUSPICIOUS ACTIVITY FEED</span>
        <span className="bg-red-500 text-white text-[8px] px-1 rounded animate-pulse">LIVE</span>
      </h3>
      
      <div className="space-y-4">
        {[1, 2].map(i => (
          <div key={i} className="p-3 bg-black border-l-2 border-red-500">
            <div className="text-[10px] text-gray-500 mb-1">2026-01-26 04:22:15</div>
            <div className="text-sm font-mono text-gray-300">SPOOFING_PATTERN_DETECTED: Agent_04</div>
            <div className="mt-2 flex gap-4">
              <button className="text-[10px] bg-gray-800 px-2 py-1 rounded">CLEAR</button>
              <button className="text-[10px] bg-red-900/40 text-red-500 px-2 py-1 rounded font-bold">ESCALATE</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SARViewer;
