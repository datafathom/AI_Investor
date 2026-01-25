import React, { useState } from 'react';
import { Home, Palette, Briefcase, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';
import './RealEstateTracker.css';

/**
 * Real Estate & Illiquid Asset Tracker (Phase 23)
 * 
 * Manual asset entry with appreciation/depreciation tracking.
 */
const RealEstateTracker = () => {
    const [showAddModal, setShowAddModal] = useState(false);

    const assets = [
        { name: 'Primary Residence', type: 'property', value: 850000, change: 5.2, cost: 650000 },
        { name: 'Investment Condo', type: 'property', value: 425000, change: 3.8, cost: 380000 },
        { name: 'Art Collection', type: 'art', value: 125000, change: 8.5, cost: 85000 },
        { name: 'PE Fund II LP', type: 'private', value: 250000, change: -2.1, cost: 275000 },
        { name: 'Vintage Car', type: 'collectible', value: 95000, change: 12.4, cost: 72000 },
    ];

    const totalValue = assets.reduce((sum, a) => sum + a.value, 0);
    const totalCost = assets.reduce((sum, a) => sum + a.cost, 0);
    const totalGain = ((totalValue - totalCost) / totalCost * 100).toFixed(1);

    const getIcon = (type) => {
        switch (type) {
            case 'property': return <Home size={16} />;
            case 'art': return <Palette size={16} />;
            case 'private': return <Briefcase size={16} />;
            default: return <DollarSign size={16} />;
        }
    };

    return (
        <div className="real-estate-tracker">
            <div className="widget-header">
                <Home size={16} />
                <h3>Illiquid Assets</h3>
            </div>

            <div className="net-worth-summary">
                <div className="summary-item">
                    <span className="label">Total Value</span>
                    <span className="value">${(totalValue / 1000000).toFixed(2)}M</span>
                </div>
                <div className="summary-item">
                    <span className="label">Total Gain</span>
                    <span className={`value ${parseFloat(totalGain) >= 0 ? 'positive' : 'negative'}`}>
                        {parseFloat(totalGain) >= 0 ? '+' : ''}{totalGain}%
                    </span>
                </div>
            </div>

            <div className="assets-list">
                {assets.map((asset, i) => (
                    <div key={i} className="asset-card">
                        <div className="asset-icon">
                            {getIcon(asset.type)}
                        </div>
                        <div className="asset-info">
                            <span className="asset-name">{asset.name}</span>
                            <span className="asset-type">{asset.type}</span>
                        </div>
                        <div className="asset-value">
                            <span className="current">${(asset.value / 1000).toFixed(0)}K</span>
                            <span className={`change ${asset.change >= 0 ? 'positive' : 'negative'}`}>
                                {asset.change >= 0 ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
                                {Math.abs(asset.change)}%
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <button className="add-asset-btn" onClick={() => setShowAddModal(true)}>
                + Add Asset
            </button>
        </div>
    );
};

export default RealEstateTracker;
