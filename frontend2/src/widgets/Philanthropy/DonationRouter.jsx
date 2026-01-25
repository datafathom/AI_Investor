import React, { useState } from 'react';
import { Heart, Gift, Wallet, ArrowRight } from 'lucide-react';
import './DonationRouter.css';

const DonationRouter = () => {
    const [alphaThreshold, setAlphaThreshold] = useState(15); // %
    
    const charities = [
        { id: 1, name: 'Effective Altruism Fund', category: 'Global Health', rating: 'A+' },
        { id: 2, name: 'Climate Clean-Up', category: 'Environment', rating: 'A' },
        { id: 3, name: 'Tech Education Initiative', category: 'Education', rating: 'A-' },
    ];

    return (
        <div className="donation-router-widget">
            <div className="widget-header">
                <h3><Heart size={18} className="text-pink-500" /> Excess Alpha Donation Router</h3>
                <div className="header-status">
                    <span className="label">YTD Impact:</span>
                    <span className="val">$14,250</span>
                </div>
            </div>

            <div className="threshold-config">
                <div className="config-row">
                    <label>Define "Enough" Threshold (Annual Return %):</label>
                    <div className="input-group">
                        <input 
                            type="number" 
                            value={alphaThreshold} 
                            onChange={(e) => setAlphaThreshold(e.target.value)}
                        />
                        <span className="percent">%</span>
                    </div>
                </div>
                <div className="config-desc">
                    Profits exceeding <strong>{alphaThreshold}%</strong> APY will be automatically routed to selected charities quarterly.
                </div>
            </div>

            <div className="charity-selection">
                <h4>Active Allocations</h4>
                <div className="charity-list">
                    {charities.map(charity => (
                        <div key={charity.id} className="charity-item">
                            <div className="charity-info">
                                <span className="name">{charity.name}</span>
                                <span className="cat">{charity.category} • Grade {charity.rating}</span>
                            </div>
                            <div className="allocation-share">
                                <span>33%</span>
                            </div>
                        </div>
                    ))}
                </div>
                <button className="add-charity-btn">+ Add Charity</button>
            </div>

            <div className="impact-pulse">
                <div className="pulse-header"><Gift size={14} /> Real-World Impact Pulse</div>
                <div className="pulse-metrics">
                    <div className="metric">
                        <span className="val">205</span>
                        <span className="lbl">Trees Planted</span>
                    </div>
                    <div className="metric">
                        <span className="val">1,400</span>
                        <span className="lbl">Meals Funded</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DonationRouter;
