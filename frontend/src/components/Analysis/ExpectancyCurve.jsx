import React, { useEffect, useState } from 'react';

const ExpectancyCurve = ({ data }) => {
  return (
    <div className="p-4 bg-gray-800 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold text-green-400 mb-4">Expectancy Curve</h3>
      <div className="h-64 flex items-center justify-center border border-gray-700">
        {/* Placeholder for Chart.js or Recharts */}
        <p className="text-gray-500">Expectancy: {data?.expectancy || 0}R / Trade</p>
      </div>
    </div>
  );
};

export default ExpectancyCurve;
