import React from 'react';

const HealthStatus = () => {
  const nodes = [
    { name: 'Matrix (Postgres)', status: 'UP' },
    { name: 'Flow (Redpanda)', status: 'UP' },
    { name: 'Graph (Neo4j)', status: 'UP' },
    { name: 'LLM Gateway', status: 'STRESSED' },
    { name: 'Broker Stream', status: 'UP' },
  ];

  return (
    <div className="p-6 bg-gray-900 rounded-lg">
      <h3 className="text-gray-500 font-bold text-xs mb-6 uppercase">System Node Mesh</h3>
      <div className="grid grid-cols-2 gap-4">
        {nodes.map(n => (
            <div key={n.name} className="flex items-center gap-3">
                <div className={`h-2 w-2 rounded-full ${
                    n.status === 'UP' ? 'bg-green-500 shadow-neon-green' : 'bg-red-500 shadow-neon-red animate-pulse'
                }`}></div>
                <div className="text-xs font-mono text-gray-300">{n.name}</div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default HealthStatus;
