import React, { useState } from 'react';
import { useWealthStore } from '../../stores/wealthStore';
import { TrendingUp, TrendingDown, RefreshCw } from 'lucide-react';
import './ValuationSlider.css';

export default function ValuationSlider() {
  const { assets, updateAsset } = useWealthStore();
  const [selectedAssetId, setSelectedAssetId] = useState('');
  const [adjustment, setAdjustment] = useState(0); // Percentage

  const selectedAsset = (assets || []).find(a => a?.id === selectedAssetId);
  
  // Compute projected value
  const currentValue = (selectedAsset && selectedAsset.value) ? parseFloat(selectedAsset.value) : 0;
  const projectedValue = currentValue * (1 + adjustment / 100);
  const delta = projectedValue - currentValue;

  const handleSave = () => {
    if (selectedAsset) {
      updateAsset(selectedAsset.id, { value: projectedValue });
      setAdjustment(0);
    }
  };

  return (
    <div className="valuation-slider-widget glass-panel">
      <div className="widget-header">
         <h3>Valuation Adjuster</h3>
         <span className="subtitle">Scenario Modeling</span>
      </div>

      <div className="asset-selector">
        <select 
          value={selectedAssetId} 
          onChange={(e) => { setSelectedAssetId(e.target.value); setAdjustment(0); }}
          className="form-input"
        >
          <option value="">Select an asset...</option>
          {assets && assets.map(a => (
            <option key={a.id} value={a.id}>{a.name} ({a.category})</option>
          ))}
        </select>
      </div>

      {selectedAsset ? (
        <div className="valuation-content">
           <div className="current-stats">
              <div className="stat-row">
                 <span>Original Value</span>
                 <span className="mono">${currentValue.toLocaleString()}</span>
              </div>
              <div className="stat-row">
                 <span>Location</span>
                 <span>{selectedAsset.location || 'N/A'}</span>
              </div>
           </div>

           <div className="slider-container">
             <div className="slider-labels">
               <span>-20%</span>
               <span className={adjustment > 0 ? 'text-green' : adjustment < 0 ? 'text-red' : ''}>
                 {adjustment > 0 ? '+' : ''}{adjustment}%
               </span>
               <span>+20%</span>
             </div>
             <input 
               type="range" 
               min="-20" 
               max="20" 
               step="0.5"
               value={adjustment}
               onChange={(e) => setAdjustment(parseFloat(e.target.value))}
               className="range-input"
             />
           </div>

           <div className="projection-box">
             <div className="projection-label">New Estimated Value</div>
             <div className="projection-value">
                ${projectedValue.toLocaleString([], { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
             </div>
             <div className={`projection-delta ${delta >= 0 ? 'positive' : 'negative'}`}>
                {delta >= 0 ? <TrendingUp size={14}/> : <TrendingDown size={14}/>}
                ${Math.abs(delta).toLocaleString()} ({adjustment}%)
             </div>
           </div>

           <div className="actions">
             <button className="reset-btn" onClick={() => setAdjustment(0)} title="Reset">
               <RefreshCw size={16} />
             </button>
             <button className="confirm-btn" onClick={handleSave}>
               Update Valuation
             </button>
           </div>
        </div>
      ) : (
        <div className="empty-state">
           Select an asset to model its valuation changes based on market conditions.
        </div>
      )}
    </div>
  );
}
