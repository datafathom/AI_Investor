import React, { useState } from 'react';
import './SplicingConflictResolver.css';

const SplicingConflictResolver = ({ parent1, parent2, onResolve }) => {
  const [resolvedGenes, setResolvedGenes] = useState({});

  const p1Genes = parent1?.genes || { rsi_period: 14, rsi_buy: 30, rsi_sell: 70, leverage: 1.5 };
  const p2Genes = parent2?.genes || { rsi_period: 21, rsi_buy: 25, rsi_sell: 75, leverage: 2.0 };

  const allKeys = Array.from(new Set([...Object.keys(p1Genes), ...Object.keys(p2Genes)]));

  const handleResolve = (key, value) => {
    setResolvedGenes(prev => ({ ...prev, [key]: value }));
  };

  const autoResolve = (strategy) => {
    const newResolved = {};
    allKeys.forEach(key => {
      if (strategy === 'dominant') {
         newResolved[key] = p1Genes[key] || p2Genes[key];
      } else if (strategy === 'average') {
         const v1 = p1Genes[key] || 0;
         const v2 = p2Genes[key] || 0;
         newResolved[key] = typeof v1 === 'number' ? (v1 + v2) / 2 : v1;
      }
    });
    setResolvedGenes(newResolved);
  };

  return (
    <div className="splicing-resolver-container">
      <div className="splicing-resolver-header">
        <h3>Genomic Conflict Resolver</h3>
      </div>

      <div className="diff-grid">
        <div className="diff-header">GENE</div>
        <div className="diff-header">{parent1?.id || 'PARENT A'}</div>
        <div className="diff-header">{parent2?.id || 'PARENT B'}</div>

        {allKeys.map(key => {
          const isConflict = p1Genes[key] !== p2Genes[key];
          const isResolved = resolvedGenes[key] !== undefined;
          
          return (
            <div key={key} className="diff-row">
              <div className="diff-cell gene-name">{key.toUpperCase()}</div>
              <div 
                className={`diff-cell ${isConflict && !isResolved ? 'conflict' : ''} ${resolvedGenes[key] === p1Genes[key] ? 'resolved' : ''}`}
                onClick={() => handleResolve(key, p1Genes[key])}
              >
                {p1Genes[key]}
              </div>
              <div 
                className={`diff-cell ${isConflict && !isResolved ? 'conflict' : ''} ${resolvedGenes[key] === p2Genes[key] ? 'resolved' : ''}`}
                onClick={() => handleResolve(key, p2Genes[key])}
              >
                {p2Genes[key]}
              </div>
            </div>
          );
        })}
      </div>

      <div className="splicing-actions">
        <button className="action-btn secondary" onClick={() => autoResolve('dominant')}>DOMINANT AUTO</button>
        <button className="action-btn secondary" onClick={() => autoResolve('average')}>AVERAGE AUTO</button>
        <button className="action-btn" onClick={() => onResolve?.(resolvedGenes)}>SPLICING START</button>
      </div>
    </div>
  );
};

export default SplicingConflictResolver;
