import React, { useState, useEffect, useMemo } from 'react';
import './SurvivalProbabilityMeter.css';

const SurvivalProbabilityMeter = ({ agentGenes, marketVolatility = 0.2 }) => {
  const [probability, setProbability] = useState(0.85);
  const [isSimulating, setIsSimulating] = useState(false);

  const runMonteCarlo = () => {
    setIsSimulating(true);
    
    // Simulate 1000 paths
    setTimeout(() => {
      const passes = 1000;
      let survivors = 0;
      
      const leverage = agentGenes?.leverage || 1.0;
      const stopLoss = agentGenes?.stop_loss || 0.05;

      for (let i = 0; i < passes; i++) {
        let capital = 1.0;
        let isBankrupt = false;
        
        // 365 days simulation
        for (let day = 0; day < 365; day++) {
          const dailyRet = (Math.random() - 0.5) * marketVolatility;
          capital += capital * dailyRet * leverage;
          
          if (capital < (1.0 - stopLoss * 2)) { // Rough bankruptcy thresh
            isBankrupt = true;
            break;
          }
        }
        
        if (!isBankrupt) survivors++;
      }
      
      setProbability(survivors / passes);
      setIsSimulating(false);
    }, 1500);
  };

  useEffect(() => {
    runMonteCarlo();
  }, [agentGenes, marketVolatility]);

  const needleRotation = useMemo(() => {
    // 0 probability = -90deg, 1 probability = 90deg
    return (probability * 180) - 90;
  }, [probability]);

  return (
    <div className="survival-meter-container">
      <div className="survival-meter-header">
        <h3>Survival Probability (Monte Carlo)</h3>
      </div>

      <div className="gauge-wrapper">
        <div className="gauge-background" />
        <div className="gauge-needle" style={{ transform: `rotate(${needleRotation}deg)` }} />
        <div className="gauge-center" />
      </div>

      <div className="probability-value">
        {(probability * 100).toFixed(1)}%
      </div>

      <div className="mc-stats">
        1000 Iterations | Vol: {(marketVolatility * 100).toFixed(0)}%
      </div>

      {isSimulating && <div className="mc-status">Rerunning Simulation...</div>}
    </div>
  );
};

export default SurvivalProbabilityMeter;
