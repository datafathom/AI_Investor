import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Clock } from 'lucide-react';
import './TradeAuth.css';

const TradeAuth = () => {
    const [timeLeft, setTimeLeft] = useState(60);
    const [status, setStatus] = useState('pending'); // pending, approved, rejected, expired

    useEffect(() => {
        if (status !== 'pending') return;
        const timer = setInterval(() => {
            setTimeLeft(t => {
                if (t <= 1) {
                    setStatus('expired');
                    return 0;
                }
                return t - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [status]);

    return (
        <div className="trade-auth-widget mobile-sim">
             <div className="status-bar">
                <span>9:42</span>
                <span>5G</span>
            </div>

            <div className="auth-content">
                <div className="notif-card">
                    <div className="notif-header">
                        <span className="app-name">AI INVESTOR</span>
                        <span className="time-ago">Now</span>
                    </div>
                    <h3>Trade Authorization Required</h3>
                    <p>High conviction trade >$10k detected.</p>
                </div>

                {status === 'pending' && (
                    <div className="trade-details-card">
                        <div className="timer-bar" style={{ width: `${(timeLeft / 60) * 100}%` }}></div>
                        <div className="details-header">
                            <span className="action buy">BUY</span>
                            <span className="ticker">TSLA</span>
                        </div>
                        <div className="details-body">
                            <div className="row">
                                <span>Quantity</span>
                                <span>50 Shares</span>
                            </div>
                            <div className="row">
                                <span>Price</span>
                                <span>$242.50</span>
                            </div>
                            <div className="row total">
                                <span>Total Est.</span>
                                <span>$12,125.00</span>
                            </div>
                        </div>
                        <div className="auth-actions">
                            <button className="btn reject" onClick={() => setStatus('rejected')}>
                                <XCircle size={20} /> Reject
                            </button>
                            <button className="btn approve" onClick={() => setStatus('approved')}>
                                <CheckCircle size={20} /> Approve
                            </button>
                        </div>
                        <div className="timer-text"><Clock size={12} /> Auto-Cancel in {timeLeft}s</div>
                    </div>
                )}

                {status === 'approved' && (
                    <div className="status-msg success">
                        <CheckCircle size={48} />
                        <h3>Trade Authorized</h3>
                        <p>Order submitted to broker.</p>
                    </div>
                )}

                {status === 'rejected' && (
                    <div className="status-msg error">
                        <XCircle size={48} />
                        <h3>Trade Rejected</h3>
                        <p>Order cancelled by user.</p>
                    </div>
                )}

                 {status === 'expired' && (
                    <div className="status-msg error">
                        <Clock size={48} />
                        <h3>Time Expired</h3>
                        <p>Trade auto-cancelled for safety.</p>
                    </div>
                )}

                {status !== 'pending' && (
                     <button onClick={() => { setStatus('pending'); setTimeLeft(60); }} className="reset-btn">Reset Simulator</button>
                )}
            </div>
        </div>
    );
};

export default TradeAuth;
