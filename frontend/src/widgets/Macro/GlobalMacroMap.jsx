import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Ship, Landmark, TrendingUp, TrendingDown } from 'lucide-react';
import useMacroStore from '../../stores/macroStore';
import './GlobalMacro.css';

/**
 * Global Macro World Map Widget
 * 
 * Displays global shipping routes, political alpha signals,
 * and commodity flow visualization.
 * Connected to MacroService via macroStore.
 */
const GlobalMacroMap = () => {
    const containerRef = useRef(null);
    const [selectedRegion, setSelectedRegion] = useState(null);
    const { 
        shippingRoutes, 
        politicalSignals, 
        commodities, 
        fetchMacroData, 
        isLoading 
    } = useMacroStore();

    useEffect(() => {
        fetchMacroData();
    }, []);

    // Use store data or fallback to empty array to prevent map errors
    const shippingData = shippingRoutes || [];
    const signals = politicalSignals || [];
    const commodityIndicators = commodities || [];

    return (
        <div className="global-macro-widget" ref={containerRef}>
            <div className="widget-header">
                <h3>Global Macro Dashboard</h3>
            </div>

            <div className="macro-grid">
                {/* Shipping Routes Panel */}
                <div className="panel shipping-panel">
                    <div className="panel-header">
                        <Ship size={14} />
                        <span>Shipping Routes</span>
                    </div>
                    <div className="routes-list">
                        {shippingData.map((route, idx) => (
                            <div key={idx} className={`route-item ${route.status}`}>
                                <span className="route-name">{route.route}</span>
                                <div className="route-stats">
                                    <span className="volume">{route.volume.toLocaleString()} TEU</span>
                                    <span className={`change ${route.change >= 0 ? 'positive' : 'negative'}`}>
                                        {route.change >= 0 ? '+' : ''}{route.change}%
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Political Signals Panel */}
                <div className="panel political-panel">
                    <div className="panel-header">
                        <Landmark size={14} />
                        <span>Political Alpha</span>
                    </div>
                    <div className="signals-list">
                        {signals.map((sig, idx) => (
                            <div key={idx} className="signal-item">
                                <div className="signal-header">
                                    <span className="region">{sig.region}</span>
                                    <span className={`signal-badge ${sig.signal.toLowerCase()}`}>
                                        {sig.signal}
                                    </span>
                                </div>
                                <span className="reason">{sig.reason}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Commodities Panel */}
                <div className="panel commodities-panel">
                    <div className="panel-header">
                        <TrendingUp size={14} />
                        <span>Commodities</span>
                    </div>
                    <div className="commodities-list">
                        {commodityIndicators.map((com, idx) => (
                            <div key={idx} className="commodity-item">
                                <span className="commodity-name">{com.commodity}</span>
                                <div className="commodity-data">
                                    <span className="price">${com.price.toLocaleString()}</span>
                                    <span className={`change ${com.change >= 0 ? 'positive' : 'negative'}`}>
                                        {com.change >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                                        {Math.abs(com.change)}%
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GlobalMacroMap;
