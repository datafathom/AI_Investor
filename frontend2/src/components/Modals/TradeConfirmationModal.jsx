import React, { useEffect, useState } from 'react';
import { Shield, AlertTriangle, X, Check, Info } from 'lucide-react';
import './TradeConfirmationModal.css';

const TradeConfirmationModal = ({
    isOpen,
    onClose,
    onConfirm,
    tradeDetails = { symbol: 'SPY', side: 'BUY', quantity: 10, price: 480.00 }
}) => {
    const [riskAnalysis, setRiskAnalysis] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen && tradeDetails) {
            fetchRiskAnalysis();
        }
    }, [isOpen, tradeDetails]);

    const fetchRiskAnalysis = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/v1/risk/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(tradeDetails)
            });
            const data = await response.json();
            setRiskAnalysis(data);
        } catch (error) {
            console.error('Risk analysis failed:', error);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    const getRatingColor = (rating) => {
        switch (rating) {
            case 'DANGER': return '#ef4444';
            case 'CAUTION': return '#f59e0b';
            case 'SAFE': return '#22c55e';
            default: return 'var(--dim-text)';
        }
    };

    return (
        <div className="modal-overlay">
            <div className="trade-confirm-modal glass">
                <div className="modal-header">
                    <Shield size={18} className="text-cyan-400" />
                    <h3>Pre-Trade Risk Preview</h3>
                    <button className="close-btn" onClick={onClose}><X size={18} /></button>
                </div>

                <div className="modal-body">
                    <div className="trade-summary">
                        <div className="trade-side-badge" style={{ backgroundColor: tradeDetails.side === 'BUY' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)', color: tradeDetails.side === 'BUY' ? '#22c55e' : '#ef4444' }}>
                            {tradeDetails.side}
                        </div>
                        <div className="trade-main-info">
                            <span className="symbol">{tradeDetails.symbol}</span>
                            <span className="details">{tradeDetails.quantity} Shares @ ${tradeDetails.price}</span>
                        </div>
                        <div className="notional-value">
                            <span className="label">EST. COST</span>
                            <span className="value">${(tradeDetails.quantity * tradeDetails.price).toLocaleString()}</span>
                        </div>
                    </div>

                    <div className="risk-rating-section">
                        {loading ? (
                            <div className="risk-loading">Analyzing Risk Vectors...</div>
                        ) : riskAnalysis ? (
                            <>
                                <div className="rating-gauge">
                                    <div className="rating-label">AI SAFETY RATING</div>
                                    <div className="rating-value" style={{ color: getRatingColor(riskAnalysis.rating) }}>
                                        {riskAnalysis.rating}
                                    </div>
                                </div>

                                {riskAnalysis.sentiment && (
                                    <div className="sentiment-context">
                                        <div className="sentiment-bar-container">
                                            <div className="sentiment-label">
                                                MARKET SENTIMENT: <span className="label-text">{riskAnalysis.sentiment.label}</span>
                                            </div>
                                            <div className="sentiment-track">
                                                <div
                                                    className="sentiment-thumb"
                                                    style={{ left: `${riskAnalysis.sentiment.score}%` }}
                                                />
                                            </div>
                                            <div className="sentiment-multiplier">
                                                {riskAnalysis.sentiment.multiplier !== 1 && (
                                                    <span>Sizing Adj: {(riskAnalysis.sentiment.multiplier * 100).toFixed(0)}%</span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {riskAnalysis.reasons.length > 0 && (
                                    <div className="risk-warnings">
                                        {riskAnalysis.reasons.map((reason, i) => (
                                            <div key={i} className="warning-item">
                                                <AlertTriangle size={14} />
                                                <span>{reason}</span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </>
                        ) : (
                            <div className="risk-error">Risk Engine Offline</div>
                        )}
                    </div>

                    <div className="margin-impact">
                        <Info size={14} />
                        <span>Margin required: ${(tradeDetails.quantity * tradeDetails.price * 0.25).toLocaleString()} (Standard Reg-T)</span>
                    </div>
                </div>

                <div className="modal-actions">
                    <button className="btn-cancel" onClick={onClose}>ABORT</button>
                    <button
                        className="btn-confirm"
                        disabled={riskAnalysis?.rating === 'DANGER'}
                        onClick={() => onConfirm(tradeDetails)}
                    >
                        CONFIRM EXECUTION
                    </button>
                </div>
            </div>
        </div>
    );
};

export default TradeConfirmationModal;
