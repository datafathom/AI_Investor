import React, { useEffect, useState } from 'react';

const Pipometer = () => {
  const [velocity, setVelocity] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
        // Mock data update
      setVelocity((Math.random() - 0.5) * 10); 
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 bg-gray-800 rounded-lg text-center">
      <h3 className="text-gray-400 text-sm uppercase">Market Velocity</h3>
      <div className={`text-4xl font-bold ${velocity > 0 ? 'text-green-500' : 'text-red-500'}`}>
        {velocity.toFixed(2)} pips/s
      </div>
    </div>
  );
};

export default Pipometer;
