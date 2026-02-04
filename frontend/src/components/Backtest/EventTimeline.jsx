import React from 'react';

const EventTimeline = () => {
  const events = [
    { date: '2020-03', title: 'Covid Crash', impact: 'CRITICAL' },
    { date: '2022-06', title: 'Inflation Spike', impact: 'WARNING' },
    { date: '2024-01', title: 'AI Pivot', impact: 'POSITIVE' },
  ];

  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-purple-400 font-bold mb-4">Drawdown vs Macro Events</h3>
      <div className="space-y-4 relative">
        <div className="absolute left-2 top-0 bottom-0 w-[1px] bg-gray-800"></div>
        {events.map((e, i) => (
          <div key={i} className="pl-6 relative">
            <div className="absolute left-0 top-1 h-4 w-4 bg-gray-800 rounded-full border border-purple-500"></div>
            <div className="text-xs font-bold text-gray-300">{e.date}</div>
            <div className="text-sm text-white">{e.title}</div>
            <div className="text-[10px] text-gray-500">Impact: {e.impact}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventTimeline;
