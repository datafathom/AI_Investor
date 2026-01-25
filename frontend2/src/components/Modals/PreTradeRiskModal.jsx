
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, AlertTriangle, CheckCircle, BarChart2, Activity } from 'lucide-react';
import './PreTradeRiskModal.css';

const RiskBadge = ({ level, reason }) => {
    const colors = {
        SAFE: { bg: 'rgba(46, 213, 115, 0.2)', text: '#2ed573', icon: CheckCircle },
        CAUTION: { bg: 'rgba(255, 165, 2, 0.2)', text: '#ffa502', icon: AlertTriangle },
        DANGER: { bg: 'rgba(255, 71, 87, 0.2)', text: '#ff4757', icon: Shield }
    };

    const style = colors[level] || colors.CAUTION;
    const Icon = style.icon;

    return (
        <div className="risk-badge" style={{ background: style.bg, borderColor: style.text, color: style.text }}>
            <div className="badge-header">
                <Icon size={16} style={{ marginRight: 6 }} />
                <span>RISK LEVEL: <strong>{level}</strong></span>
            </div>
            {reason && <div className="badge-reason">{reason}</div>}
        </div>
    );
};

const NancyPelosiIndex = ({ ticker }) => {
    // Mock data based on ticker
    const data = {
        'NVDA': { action: 'BUY', volume: '$1M - $5M', date: '2024-03-12', rep: 'Pelosi' },
        'TSLA': { action: 'SELL', volume: '$500k', date: '2024-01-15', rep: 'Crenshaw' },
        'SPY': { action: 'BUY', volume: '$250k', date: '2024-02-28', rep: 'Cruz' }
    };

    const entry = data[ticker];
    if (!entry) return null;

    return (
        <div className="pelosi-index">
            <div className="pi-header">
                <Activity size={14} className="mr-2 text-purple-400" />
                <span className="text-xs uppercase tracking-wider text-purple-300">Political Alpha Signal</span>
            </div>
            <div className="pi-content">
                Rep. {entry.rep} <strong>{entry.action}</strong> {entry.volume} on {entry.date}
            </div>
        </div>
    );
};

const PreTradeRiskModal = ({ isOpen, onClose, tradeDetails, onConfirm }) => {
    const [riskAnalysis, setRiskAnalysis] = useState(null);

    useEffect(() => {
        if (isOpen && tradeDetails) {
            // Simulate AI Risk Analysis
            const calculateRisk = () => {
                const { size, price, ticker } = tradeDetails;
                const totalValue = size * price;
                const marginUsed = totalValue * 0.5; // Assume 50% margin
                
                let level = 'SAFE';
                let reason = 'Trade is within normal parameters.';
                
                if (totalValue > 50000) {
                    level = 'DANGER';
                    reason = `Position size ($${totalValue.toLocaleString()}) exceeds concentration limits for ${ticker}.`;
                } else if (totalValue > 20000) {
                    level = 'CAUTION';
                    reason = 'This trade uses >20% of available day trading buying power.';
                }

                return {
                    level,
                    reason,
                    marginImpact: marginUsed,
                    sectorExposure: '28% (Tech)' // Mocked
                };
            };

            setRiskAnalysis(calculateRisk());
        }
    }, [isOpen, tradeDetails]);

    if (!isOpen || !tradeDetails) return null;

    return (
        <AnimatePresence>
            <div className="modal-backdrop">
                <motion.div 
                    className="modal-container"
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.9, opacity: 0 }}
                >
                    <div className="modal-header">
                        <h2><Shield size={20} className="inline mr-2" /> EXECUTION SHIELD</h2>
                        <div className="ticker-tag">{tradeDetails.ticker}</div>
                    </div>

                    <div className="modal-body">
                        {riskAnalysis && (
                            <RiskBadge level={riskAnalysis.level} reason={riskAnalysis.reason} />
                        )}

                        <div className="trade-summary">
                            <div className="summary-row">
                                <span>Action</span>
                                <span className={tradeDetails.side === 'BUY' ? 'text-green-400' : 'text-red-400'}>
                                    {tradeDetails.side} {tradeDetails.size} @ ${tradeDetails.price}
                                </span>
                            </div>
                            <div className="summary-row">
                                <span>Est. Total</span>
                                <span>${(tradeDetails.size * tradeDetails.price).toLocaleString()}</span>
                            </div>
                            <div className="summary-row highlight">
                                <span>Margin Impact</span>
                                <span>-${riskAnalysis?.marginImpact?.toLocaleString()}</span>
                            </div>
                        </div>

                        <NancyPelosiIndex ticker={tradeDetails.ticker} />

                        <div className="compliance-check">
                            <input type="checkbox" id="compliance" />
                            <label htmlFor="compliance">I acknowledge the AI Risk Rating and accept full liability.</label>
                        </div>
                    </div>

                    <div className="modal-footer">
                        <button className="btn-cancel" onClick={onClose}>ABORT</button>
                        <button 
                            className={`btn-confirm ${riskAnalysis?.level === 'DANGER' ? 'danger' : ''}`} 
                            onClick={onConfirm}
                        >
                            EXECUTE TRADE
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
};

export default PreTradeRiskModal;
