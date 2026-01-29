import React, { useEffect, useState } from 'react';
import { Sprout, ArrowRight, Heart, DollarSign, History } from 'lucide-react';
import useImpactStore from '../../stores/impactStore';
import './DonationRouter.css';

const DonationRouter = () => {
    const { 
        enoughThreshold, currentNetWorth, allocations, donationHistory,
        fetchDonationHistory, triggerDonation, isLoading
    } = useImpactStore();

    const [isHovering, setIsHovering] = useState(null);

    useEffect(() => {
        fetchDonationHistory();
    }, []);

    const excessAlpha = Math.max(0, currentNetWorth - enoughThreshold);
    const hasExcess = excessAlpha > 0;

    const handleDonate = () => {
        if (hasExcess && !isLoading) {
            triggerDonation(excessAlpha);
        }
    };

    return (
        <div className="donation-router">
            <div className="router-header">
                <h3><Sprout size={18} className="text-green-400" /> Excess Alpha Router</h3>
                <div className="text-xs text-gray-500">PHILANTHROPY ENGINE</div>
            </div>

            <div className="wealth-metrics">
                <div className="metric-row">
                    <label>"Enough" Threshold</label>
                    <span>${((enoughThreshold || 0) / 1000000).toFixed(2)}M</span>
                </div>
                <div className="metric-row text-right">
                    <label>Current Net Worth</label>
                    <span className="text-white">${((currentNetWorth || 0) / 1000000).toFixed(3)}M</span>
                </div>
            </div>

            <div className="excess-alpha">
                <div className="flex items-center gap-2">
                    <DollarSign size={16} className="text-green-500" />
                    <span className="text-sm text-gray-400">Distributable Alpha:</span>
                </div>
                <span className="amount">${(excessAlpha || 0).toLocaleString()}</span>
            </div>

            <div className="allocation-pipeline">
                <div className="pipeline-header">Allocation Pipeline</div>
                <div className="pipeline-visual">
                    {(allocations || []).map((alloc, idx) => (
                        <div 
                            key={idx} 
                            className="pipe-segment" 
                            style={{ flex: alloc.percentage }}
                            onMouseEnter={() => setIsHovering(idx)}
                            onMouseLeave={() => setIsHovering(null)}
                        >
                            <span>{alloc.category}</span>
                            <small>{alloc.percentage}%</small>
                            {isHovering === idx && (
                                <div className="absolute -top-8 bg-black/80 px-2 py-1 rounded text-xs">
                                    ${(excessAlpha * (alloc.percentage / 100)).toLocaleString()} estimate
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <div className="donation-history">
                <div className="font-semibold mb-2 text-xs uppercase text-gray-600 flex items-center gap-1">
                    <History size={10} /> Recent Activity
                </div>
                {(donationHistory || []).length === 0 ? (
                    <div className="text-center text-xs text-gray-600 py-2">No donations recorded yet.</div>
                ) : (
                    (donationHistory || []).slice(0, 3).map((record) => (
                        <div key={record.id} className="history-item">
                            <span>{new Date(record.date).toLocaleDateString()}</span>
                            <span className="text-green-400">+${record.total.toLocaleString()}</span>
                        </div>
                    ))
                )}
            </div>

            <div className="action-area">
                <button 
                    className={`donate-btn ${!hasExcess || isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    onClick={handleDonate}
                    disabled={!hasExcess || isLoading}
                >
                    <Heart size={16} />
                    {isLoading ? 'Processing...' : 'Trigger Donation'}
                </button>
            </div>
        </div>
    );
};

export default DonationRouter;
