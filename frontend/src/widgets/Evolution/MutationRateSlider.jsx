import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './MutationRateSlider.css';

const MutationRateSlider = () => {
  const [rate, setRate] = useState(0.1);
  const [status, setStatus] = useState('running'); // running, paused, accelerated
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to backend WebSocket
    const newSocket = io('http://localhost:5050', { transports: ['polling'] });
    setSocket(newSocket);

    newSocket.on('mutation_rate_changed', (data) => {
      console.log('Mutation rate synced:', data.rate);
    });

    return () => newSocket.close();
  }, []);

  const handleRateChange = (e) => {
    const newRate = parseFloat(e.target.value);
    setRate(newRate);
    if (socket) {
      socket.emit('update_mutation_rate', { rate: newRate });
    }
  };

  const handleCommand = (cmd, val = null) => {
    setStatus(cmd === 'speed' ? 'accelerated' : cmd);
    if (socket) {
      socket.emit('evolution_control', { command: cmd, value: val });
    }
  };

  return (
    <div className="mutation-rate-container">
      <div className="mutation-rate-header">
        <h3>Mutation Pulse</h3>
        <div className="rate-display">{(rate * 100).toFixed(1)}%</div>
      </div>

      <div className="slider-wrapper">
        <input 
          type="range" 
          min="0.01" 
          max="0.5" 
          step="0.01" 
          value={rate} 
          onChange={handleRateChange} 
        />
      </div>

      <div className="mutation-rate-controls">
        <button 
          className={`ctrl-btn ${status === 'paused' ? 'active' : ''}`}
          onClick={() => handleCommand('pause')}
        >
          PAUSE
        </button>
        <button 
          className={`ctrl-btn ${status === 'running' ? 'active' : ''}`}
          onClick={() => handleCommand('resume')}
        >
          RESUME
        </button>
        <button 
          className={`ctrl-btn ${status === 'accelerated' ? 'active' : ''}`}
          onClick={() => handleCommand('speed', 2.0)}
        >
          TURBO
        </button>
      </div>
    </div>
  );
};

export default MutationRateSlider;
