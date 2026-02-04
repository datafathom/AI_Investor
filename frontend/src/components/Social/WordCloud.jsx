import React from 'react';

const WordCloud = () => {
  const words = [
    { text: 'RECESSION', size: 'text-3xl', color: 'text-red-500' },
    { text: 'AI_PIVOT', size: 'text-4xl', color: 'text-blue-400' },
    { text: 'RATE_CUTS', size: 'text-5xl', color: 'text-green-500' },
    { text: 'INFLATION', size: 'text-2xl', color: 'text-gray-400' },
  ];

  return (
    <div className="p-6 bg-gray-900 rounded-lg flex flex-wrap gap-6 items-center justify-center min-h-[200px]">
      {words.map(w => (
        <span key={w.text} className={`${w.size} ${w.color} font-bold animate-pulse-slow`}>{w.text}</span>
      ))}
    </div>
  );
};

export default WordCloud;
