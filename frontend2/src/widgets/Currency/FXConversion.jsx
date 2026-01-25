import React, { useState, useEffect } from 'react';
import { ArrowRightLeft, TrendingUp, AlertTriangle, Loader2 } from 'lucide-react';
import useCashStore from '../../stores/cashStore';
import './FXConversion.css';

const FXConversion = () => {
    const { 
        fxRates, 
        supportedCurrencies, 
        executeFxConversion, 
        fetchFxRates, 
        isExposureExceeded,
        isLoading 
    } = useCashStore();

    const [fromCurrency, setFromCurrency] = useState('USD');
    const [toCurrency, setToCurrency] = useState('EUR');
    const [amount, setAmount] = useState(1000);
    
    // Derived state
    const pair = `${fromCurrency}/${toCurrency}`;
    const inversePair = `${toCurrency}/${fromCurrency}`;
    const directRate = fxRates[pair]?.rate;
    const inverseRate = fxRates[inversePair]?.rate;
    
    const currentRate = directRate || (inverseRate ? 1 / inverseRate : 1.0);
    const spread = fxRates[pair]?.spread || (fxRates[inversePair]?.spread || 1.2);

    useEffect(() => {
        fetchFxRates();
    }, [fetchFxRates]);

    const handleConvert = async () => {
        try {
            await executeFxConversion(fromCurrency, toCurrency, amount);
            alert(`Successfully converted ${amount} ${fromCurrency} to ${toCurrency}`);
        } catch (err) {
            alert(`Conversion failed: ${err.message}`);
        }
    };

    const isLimitExceeded = isExposureExceeded(toCurrency);

    return (
        <div className={`fx-conversion-widget ${isLoading ? 'loading-opacity' : ''}`}>
            <div className="widget-header">
                <h3><ArrowRightLeft size={18} /> FX Conversion</h3>
                <div className="spread-badge">Spread: {spread.toFixed(1)}bps</div>
            </div>

            <div className="conversion-form">
                <div className="input-group">
                    <label>From</label>
                    <div className="currency-input">
                        <select value={fromCurrency} onChange={e => setFromCurrency(e.target.value)}>
                            {supportedCurrencies.map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                        <input 
                            type="number" 
                            value={amount} 
                            onChange={e => setAmount(Number(e.target.value))} 
                        />
                    </div>
                </div>

                <div className="rate-display">
                    <div className="rate-line"></div>
                    <span className="rate-value">1 {fromCurrency} = {currentRate.toFixed(4)} {toCurrency}</span>
                    <div className="rate-line"></div>
                </div>

                <div className="input-group">
                    <label>To (Estimated)</label>
                    <div className="currency-input">
                        <select value={toCurrency} onChange={e => setToCurrency(e.target.value)}>
                            {supportedCurrencies.map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                        <input 
                            type="number" 
                            value={(amount * currentRate).toFixed(2)} 
                            readOnly 
                        />
                    </div>
                </div>

                <div className="order-types">
                    <button className="order-type active">Market</button>
                    <button className="order-type">Limit</button>
                    <button className="order-type">Iceberg</button>
                </div>

                <button 
                    className="convert-btn" 
                    onClick={handleConvert}
                    disabled={isLoading || amount <= 0}
                >
                    {isLoading ? <Loader2 className="spinning" size={16} /> : 'Execute Trade'}
                </button>
            </div>
            
            <div className={`risk-warning ${isLimitExceeded ? 'danger' : ''}`}>
                <AlertTriangle size={12} />
                <span>Exceeds daily unauthorized exposure limit? {isLimitExceeded ? 'YES' : 'No.'}</span>
            </div>
        </div>
    );
};

export default FXConversion;
