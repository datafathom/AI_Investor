import React, { useEffect } from 'react';
import { Skull, AlertOctagon, TrendingDown, Loader2 } from 'lucide-react';
import useMarginStore from '../../stores/marginStore';
import './LiquidationEditor.css';

const LiquidationEditor = () => {
    const { 
        marginBuffer, 
        deleveragePlan, 
        fetchMarginData, 
        generateDeleveragePlan, 
        loading, 
        dangerZone 
    } = useMarginStore();

    useEffect(() => {
        fetchMarginData();
        // Generate a default plan if none exists or buffer is low
        generateDeleveragePlan(25);
    }, []);

    const handleDeleverage = () => {
        // In real system, this would trigger actual execution
        alert("Executing de-leverage plan. Orders dispatched to broker.");
    };

    return (
        <div className={`liquidation-editor-widget ${dangerZone ? 'danger-active' : ''}`}>
             <div className="widget-header">
                <h3><Skull size={18} className={dangerZone ? "text-red-500 animate-pulse" : "text-gray-400"} /> Automated Margin Call Liquidation Editor</h3>
                <div className="model-status">
                    <span className={`status-badge ${dangerZone ? 'urgent' : ''}`}>
                        {loading ? <Loader2 size={12} className="animate-spin" /> : 'Real-Time Mode'}
                    </span>
                </div>
            </div>

            <div className="margin-summary-mini">
                <div className="stat">
                    <span className="label">Current Buffer</span>
                    <span className={`val ${marginBuffer < 20 ? 'text-red-500' : 'text-green-500'}`}>
                        {marginBuffer.toFixed(2)}%
                    </span>
                </div>
            </div>

            <div className="ghost-order-viz">
                <h4>Projected Broker Liquidation ("Ghost Market Order")</h4>
                <div className="order-preview">
                    <div className="order-row header">
                        <span>Action</span>
                        <span>Asset</span>
                        <span>Amount</span>
                        <span>Port.</span>
                    </div>
                    {deleveragePlan?.positions_to_close?.length > 0 ? (
                        deleveragePlan.positions_to_close.map((order, idx) => (
                            <div key={idx} className="order-row sell">
                                <span className="action">SELL MARKET</span>
                                <span className="asset">{order.ticker}</span>
                                <span className="amt">{order.shares} Shares (${order.value.toLocaleString()})</span>
                                <span className="port text-xs opacity-70">{order.portfolio}</span>
                            </div>
                        ))
                    ) : (
                        <div className="no-orders">No liquidation required at current levels.</div>
                    )}
                </div>
                {deleveragePlan && (
                    <div className="total-impact">
                        <span>Total De-leverage Target:</span>
                        <span className="loss-val">${deleveragePlan.total_to_sell.toLocaleString()}</span>
                    </div>
                )}
            </div>

             <div className="deleverage-action">
                <h4>Emergency De-leverage (Restore 25% Buffer)</h4>
                <p>System will execute optimized limit orders to reduce exposure efficiently.</p>
                <div className="action-btns">
                    <button 
                        className={`execute-deleverage ${dangerZone ? 'urgent' : ''}`}
                        onClick={handleDeleverage}
                        disabled={loading || !deleveragePlan?.total_to_sell}
                    >
                        {loading ? <Loader2 size={14} className="animate-spin" /> : <TrendingDown size={14} />} 
                        Execute Optimized De-leverage
                    </button>
                    <button className="cancel-sim" onClick={() => generateDeleveragePlan(25)}>Refresh Plan</button>
                </div>
            </div>
            
            <div className="audit-log-preview">
                <AlertOctagon size={12} className={dangerZone ? "text-red-400" : ""} />
                <span>
                    {dangerZone 
                        ? `Critical: Margin buffer at ${marginBuffer.toFixed(2)}%. High liquidation risk.` 
                        : `System Healthy: Margin buffer at ${marginBuffer.toFixed(2)}%.`}
                </span>
            </div>
        </div>
    );
};

export default LiquidationEditor;
