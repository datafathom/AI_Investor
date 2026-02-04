import React from 'react';
import { Cloud, ArrowUpRight } from 'lucide-react';
import './CarbonFootprint.css';

const CarbonFootprint = () => {
    return (
        <div className="carbon-footprint-widget">
            <div className="widget-header">
                <h3><Cloud size={18} className="text-slate-400" /> Carbon Footprint vs Returns Scatterplot</h3>
            </div>

            <div className="scatter-container">
                {/* Simulated Scatterplot */}
                <svg width="100%" height="100%" viewBox="0 0 600 200">
                    <line x1="50" y1="180" x2="580" y2="180" stroke="rgba(255,255,255,0.1)" strokeWidth="2"/>
                    <line x1="50" y1="20" x2="50" y2="180" stroke="rgba(255,255,255,0.1)" strokeWidth="2"/>
                    
                    <text x="320" y="195" fill="#666" fontSize="10" textAnchor="middle">Carbon Intensity (Tons/$M)</text>
                    <text x="15" y="100" fill="#666" fontSize="10" transform="rotate(-90 15,100)">Returns (%)</text>

                    {/* Data Points */}
                    <circle cx="100" cy="80" r="15" fill="#22c55e" opacity="0.6" />
                    <circle cx="200" cy="60" r="10" fill="#22c55e" opacity="0.6" />
                    <circle cx="350" cy="120" r="25" fill="#3b82f6" opacity="0.6" />
                    <circle cx="450" cy="140" r="18" fill="#ef4444" opacity="0.6" />
                    <circle cx="500" cy="90" r="30" fill="#ef4444" opacity="0.6" />

                    {/* Regression Line */}
                    <line x1="80" y1="70" x2="550" y2="130" stroke="#fbbf24" strokeWidth="2" strokeDasharray="4,4" />
                </svg>
            </div>

            <div className="offset-action">
                <div className="footprint-stats">
                    <span className="lbl">Total Footprint</span>
                    <span className="val">4,210 Tons CO2e</span>
                </div>
                <button className="offset-btn">
                    One-Click Carbon Offset ($1,250) <ArrowUpRight size={14} />
                </button>
            </div>
        </div>
    );
};

export default CarbonFootprint;
