import React, { useState } from 'react';
import { useWealthStore } from '../../stores/wealthStore';
import AssetCategories from './AssetCategories';
import { Plus, DollarSign, FileText } from 'lucide-react';
import './ManualEntry.css';

export default function ManualEntry() {
  const addAsset = useWealthStore((state) => state.addAsset);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    value: '',
    location: '',
    notes: '',
    purchaseDate: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedCategory || !formData.name || !formData.value) return;

    addAsset({
      ...formData,
      category: selectedCategory,
      value: parseFloat(formData.value),
    });

    // Reset
    setFormData({ name: '', value: '', location: '', notes: '', purchaseDate: '' });
    setSelectedCategory(null);
  };

  return (
    <div className="manual-entry-widget glass-panel">
      <h3 className="widget-title">Illiquid Asset Entry</h3>
      
      <AssetCategories 
        selectedCategory={selectedCategory} 
        onSelect={setSelectedCategory} 
      />

      <form className="asset-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Asset Name / Description</label>
          <input
            type="text"
            className="form-input"
            placeholder="e.g. Downtown Penthouse, 1967 Mustang..."
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
          />
        </div>

        <div className="form-group grid-half">
          <label>Estimated Value (USD)</label>
          <div className="input-with-icon">
            <input
              type="number"
              className="form-input"
              placeholder="0.00"
              value={formData.value}
              onChange={(e) => setFormData({...formData, value: e.target.value})}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Location / Jurisdiction</label>
          <input
            type="text"
            className="form-input"
            placeholder="e.g. New York, NY"
            value={formData.location}
            onChange={(e) => setFormData({...formData, location: e.target.value})}
          />
        </div>
        
        <div className="form-group">
            <label>Purchase Date (Optional)</label>
            <input 
                type="date" 
                className="form-input"
                value={formData.purchaseDate}
                onChange={(e) => setFormData({...formData, purchaseDate: e.target.value})}
            />
        </div>

        <button type="submit" className="submit-btn" disabled={!selectedCategory}>
          <Plus size={18} />
          Add Asset to Registry
        </button>
      </form>
    </div>
  );
}
