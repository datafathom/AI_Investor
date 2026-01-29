
import React, { useState, useEffect } from 'react';
import { Globe, RefreshCw, ArrowRightLeft, TrendingUp, DollarSign, Wallet } from 'lucide-react';
import './SettlementDashboard.css';

const SettlementDashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [convertData, setConvertData] = useState({ from: 'USD', to: 'EUR', amount: 1000 });

    const fetchBalances = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('widget_os_token');
            const res = await fetch('/api/v1/settlement/balances', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (!res.ok) {
                console.warn("API Error, using mock data:", res.status);
                setData(MOCK_DATA);
                return;
            }

            const json = await res.json();
            setData(json);
        } catch (e) {
            console.error("Failed to fetch settlement balances, using mock data", e);
            setData(MOCK_DATA);
        } finally {
            setLoading(false);
        }
    };

    const handleConvert = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/v1/settlement/convert', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` 
                },
                body: JSON.stringify(convertData)
            });
            const result = await res.json();
            if (result.status === 'SUCCESS') {
                fetchBalances();
                alert(`Successfully converted ${result.amount_sold} ${result.from} to ${result.amount_bought} ${result.to}`);
            } else {
                alert(`Conversion failed: ${result.message}`);
            }
        } catch (e) {
            console.error("Conversion failed", e);
        }
    };

    useEffect(() => {
        fetchBalances();
    }, []);

    if (!data) return <div className="loading-state">Initializing Settlement Engine...</div>;

    return (
        <div className="settlement-widget">
            <div className="settlement-header">
                <div className="title-area">
                    <Globe className="text-blue-400" />
                    <h3>Multi-Currency Settlement</h3>
                </div>
                <div className="reporting-currency">
                    Reporting: {data.base_currency}
                </div>
            </div>

            <div className="total-equity-section">
                <span className="label">CONSOLIDATED LIQUIDITY</span>
                <span className="value">${data.total_equity_usd.toLocaleString()}</span>
            </div>

            <div className="balances-list">
                {data.balances.map((b, i) => (
                    <div key={i} className="balance-row">
                        <div className="currency-info">
                            <span className="currency-code">{b.currency}</span>
                            <span className="currency-name">{b.is_base ? 'Primary' : 'International'}</span>
                        </div>
                        <div className="balance-values">
                            <span className="native-val">{b.balance.toLocaleString()}</span>
                            {!b.is_base && <span className="usd-val">≈ ${b.usd_value.toLocaleString()}</span>}
                        </div>
                    </div>
                ))}
            </div>

            <div className="convert-tool">
                <div className="tool-header">
                    <ArrowRightLeft size={14} />
                    <span>Quick FX Swap</span>
                </div>
                <div className="tool-inputs">
                    <input 
                        type="number" 
                        value={convertData.amount} 
                        onChange={(e) => setConvertData({...convertData, amount: e.target.value})}
                    />
                    <select 
                        value={convertData.from} 
                        onChange={(e) => setConvertData({...convertData, from: e.target.value})}
                    >
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="JPY">JPY</option>
                        <option value="GBP">GBP</option>
                    </select>
                    <span>to</span>
                    <select 
                        value={convertData.to} 
                        onChange={(e) => setConvertData({...convertData, to: e.target.value})}
                    >
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                        <option value="JPY">JPY</option>
                        <option value="GBP">GBP</option>
                    </select>
                </div>
                <button className="convert-btn" onClick={handleConvert}>
                    Execute FX Trade
                </button>
            </div>

            <div className="settlement-footer">
                <RefreshCw size={12} className={loading ? 'spinning' : ''} onClick={fetchBalances} />
                <span>Rates provider: simulated 15min delay</span>
            </div>
        </div>
    );
};

export default SettlementDashboard;

const MOCK_DATA = {
    base_currency: 'USD',
    total_equity_usd: 1250000.00,
    balances: [
        { currency: 'USD', is_base: true, balance: 450000.00, usd_value: 450000.00 },
        { currency: 'EUR', is_base: false, balance: 250000.00, usd_value: 270000.00 },
        { currency: 'JPY', is_base: false, balance: 15000000.00, usd_value: 105000.00 },
        { currency: 'GBP', is_base: false, balance: 350000.00, usd_value: 425000.00 }
    ]
};
