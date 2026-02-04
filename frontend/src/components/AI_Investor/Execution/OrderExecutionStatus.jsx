
import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, Zap, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';
import './OrderExecutionStatus.css';

const OrderExecutionStatus = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);

    // Simulation: In a real app, this would listen to a WebSocket/EventStream
    useEffect(() => {
        // Initial mock order
        setOrders([
            {
                id: 'ord_1',
                symbol: 'AAPL',
                qty: 10,
                side: 'buy',
                status: 'FILLED',
                timestamp: new Date().toLocaleTimeString(),
                checks: ['KillSwitch: OK', 'RiskLimit: OK', 'Gateway: PASSED']
            }
        ]);
    }, []);

    return (
        <div className="order-execution-widget">
            <div className="exec-header">
                <div className="title-area">
                    <Zap className="icon-zap" />
                    <h3>Live Execution Router</h3>
                </div>
                <div className="active-shield">
                    <ShieldCheck size={14} />
                    <span>Guardian Protected</span>
                </div>
            </div>

            <div className="orders-list">
                {orders.length === 0 ? (
                    <div className="empty-state">No manual orders in current session</div>
                ) : (
                    orders.map(ord => (
                        <div key={ord.id} className={`order-card ${ord.status.toLowerCase()}`}>
                            <div className="order-main">
                                <div className="order-id">
                                    <span className="side-badge">{ord.side.toUpperCase()}</span>
                                    <span className="ticker">{ord.symbol}</span>
                                    <span className="id-tag">#{ord.id.slice(-4)}</span>
                                </div>
                                <div className="order-time">
                                    <Clock size={12} />
                                    {ord.timestamp}
                                </div>
                            </div>
                            
                            <div className="order-status-row">
                                <span className={`status-text ${ord.status.toLowerCase()}`}>{ord.status}</span>
                                <span className="order-qty">{ord.qty} Shares</span>
                            </div>

                            <div className="execution-checks">
                                {ord.checks.map((check, i) => (
                                    <div key={i} className="check-chip">
                                        <CheckCircle2 size={10} />
                                        {check}
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))
                )}
            </div>

            <div className="exec-footer">
                <div className="pulse-indicator">
                    <div className="pulse-dot"></div>
                    Engine Heartbeat: Operational
                </div>
                <div className="latency">45ms</div>
            </div>
        </div>
    );
};

export default OrderExecutionStatus;
