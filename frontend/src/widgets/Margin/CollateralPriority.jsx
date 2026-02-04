import React from 'react';
import { UnfoldVertical, Shield, AlertTriangle } from 'lucide-react';
import useMarginStore from '../../stores/marginStore';
import './CollateralPriority.css';

const CollateralPriority = () => {
    const { positions, collateralPriority, setCollateralPriority } = useMarginStore();

    // Mock initial priority if none set
    const mockPriority = [
        { ticker: 'TSLA', priority: 1, protected: false },
        { ticker: 'COIN', priority: 2, protected: false },
        { ticker: 'BTC', priority: 3, protected: true },
        { ticker: 'ETH', priority: 4, protected: false },
    ];

    const displayPriority = collateralPriority.length > 0 ? collateralPriority : mockPriority;

    return (
        <div className="collateral-priority-widget">
            <div className="widget-header">
                <h3><UnfoldVertical size={16} /> Liquidation Hierarchy</h3>
                <span className="info-tip">Drag to reorder</span>
            </div>

            <div className="priority-list">
                {displayPriority.map((item, index) => (
                    <div key={item.ticker} className={`priority-item ${item.protected ? 'protected' : ''}`}>
                        <div className="rank">{index + 1}</div>
                        <div className="asset-info">
                            <span className="ticker">{item.ticker}</span>
                            <span className="sub">
                                {item.protected ? 'Core Holding' : 'Collateral Asset'}
                            </span>
                        </div>
                        <div className="status-icons">
                            {item.protected ? (
                                <Shield size={14} className="text-green-500" />
                            ) : (
                                <AlertTriangle size={14} className="text-yellow-500 opacity-50" />
                            )}
                        </div>
                    </div>
                ))}
            </div>

            <div className="priority-footer">
                <p>Protected assets are excluded from automated "Ghost Order" generation until buffer &lt; 5%.</p>
            </div>
        </div>
    );
};

export default CollateralPriority;
