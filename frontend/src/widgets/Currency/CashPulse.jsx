import React, { useState, useEffect } from 'react';
import { RefreshCw, TrendingUp, DollarSign, Euro, PoundSterling } from 'lucide-react';
import useCashStore from '../../stores/cashStore';
import './CashPulse.css';

/**
 * Global Cash Balance Widget (Phase 13 -> 56)
 * 
 * Multi-currency cash management with FX rates and interest heat indicators.
 */
const CashPulse = () => {
    const { 
        balances, 
        baseCurrency, 
        setBaseCurrency, 
        isLoading, 
        fetchCashData,
        getTotalInBaseCurrency,
        getIdleCash,
        lastUpdated
    } = useCashStore();

    useEffect(() => {
        fetchCashData();
    }, [fetchCashData]);

    const getHeatColor = (rate) => {
        if (rate >= 4) return '#f87171'; // Hot
        if (rate >= 2) return '#fbbf24'; // Warm
        return '#60a5fa'; // Cool
    };

    const getCurrencyIcon = (code) => {
        switch(code) {
            case 'USD': return <DollarSign size={16} />;
            case 'EUR': return <Euro size={16} />;
            case 'GBP': return <PoundSterling size={16} />;
            default: return code.slice(0, 1);
        }
    };

    const idleCash = getIdleCash();
    const totalInBase = getTotalInBaseCurrency();

    return (
        <div className={`cash-pulse ${isLoading ? 'loading' : ''}`}>
            <div className="widget-header">
                <h3>Global Cash Pulse</h3>
                <div className="header-controls">
                    <select value={baseCurrency} onChange={(e) => setBaseCurrency(e.target.value)}>
                        {['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD'].map(c => (
                            <option key={c} value={c}>{c}</option>
                        ))}
                    </select>
                    <button className={`refresh-btn ${isLoading ? 'spinning' : ''}`} onClick={fetchCashData}>
                        <RefreshCw size={14} />
                    </button>
                </div>
            </div>

            {lastUpdated && (
                <div className="last-updated">Updated: {new Date(lastUpdated).toLocaleTimeString()}</div>
            )}

            <div className="total-balance">
                <span className="label">Total Holdings ({baseCurrency})</span>
                <span className="value">{baseCurrency === 'USD' ? '$' : ''}{totalInBase.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </div>

            <div className="currency-list">
                {balances.map(currency => (
                    <div key={currency.currency} className="currency-card">
                        <div className="currency-info">
                            <div className="currency-icon">
                                {getCurrencyIcon(currency.currency)}
                            </div>
                            <div>
                                <span className="currency-code">{currency.currency}</span>
                                <span className="currency-name">{currency.currency} Ledger</span>
                            </div>
                        </div>
                        <div className="currency-balance">
                            <span className="balance">{currency.amount.toLocaleString()}</span>
                            <span className="usd-value">${currency.amountUSD.toLocaleString()}</span>
                        </div>
                        <div 
                            className="heat-indicator"
                            style={{ background: getHeatColor(currency.interestRate) }}
                            title={`Overnight Rate: ${currency.interestRate}%`}
                        >
                            {currency.interestRate}%
                        </div>
                    </div>
                ))}
            </div>

            {idleCash > 100000 && (
                <div className="idle-cash-alert">
                    <TrendingUp size={12} />
                    <span>${(idleCash/1000).toFixed(0)}K idle cash earning below market rate</span>
                </div>
            )}
        </div>
    );
};

export default CashPulse;
