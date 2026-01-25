import React, { useState, useEffect, useMemo } from 'react';
import './OptionsChain.css';
import useSymbolLink from '../../hooks/useSymbolLink';

const OptionsChainWidget = ({ linkingGroup = 'none' }) => {
  const { currentSymbol } = useSymbolLink(linkingGroup);
  const [chain, setChain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChain = async () => {
      if (!currentSymbol) return;
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:5050/api/v1/market/options/${currentSymbol}`);
        if (!response.ok) throw new Error('Failed to fetch options chain');
        const data = await response.json();
        setChain(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChain();
    const interval = setInterval(fetchChain, 5000); // Pulse every 5s
    return () => clearInterval(interval);
  }, [currentSymbol]);

  // Group by expiration for the UI
  const expirations = useMemo(() => {
    const groups = {};
    chain.forEach(c => {
      if (!groups[c.expiration]) groups[c.expiration] = [];
      groups[c.expiration].push(c);
    });
    return groups;
  }, [chain]);

  if (!currentSymbol) {
    return (
      <div className="options-chain-empty">
        <div className="empty-content">
          <span className="empty-icon">⛓️</span>
          <p>Select a symbol group to load Options Chain</p>
        </div>
      </div>
    );
  }

  return (
    <div className="options-chain-container">
      <div className="oc-header">
        <div className="oc-symbol-info">
          <h3>{currentSymbol} Options Chain</h3>
          <span className="oc-badge">Real-time Pulse</span>
        </div>
      </div>

      {loading && chain.length === 0 ? (
        <div className="oc-loading">Loading Chain...</div>
      ) : error ? (
        <div className="oc-error">{error}</div>
      ) : (
        <div className="oc-scroller">
          {Object.entries(expirations).map(([expiry, contracts]) => (
            <div key={expiry} className="expiry-section">
              <div className="expiry-header">
                <span>📅 Expiration: {expiry}</span>
              </div>
              <table className="oc-table">
                <thead>
                  <tr>
                    <th colSpan="3" className="th-calls">CALLS</th>
                    <th className="th-strike">STRIKE</th>
                    <th colSpan="3" className="th-puts">PUTS</th>
                  </tr>
                  <tr className="sub-header">
                    <th>Bid</th>
                    <th>Ask</th>
                    <th>Δ</th>
                    <th></th>
                    <th>Δ</th>
                    <th>Bid</th>
                    <th>Ask</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Note: In a real app we'd align rows by strike */}
                  {/* For this MVP/Demo we'll display them paired if possible */}
                  {Array.from(new Set(contracts.map(c => c.strike))).sort((a,b) => a-b).map(strike => {
                    const call = contracts.find(c => c.strike === strike && c.type === 'call');
                    const put = contracts.find(c => c.strike === strike && c.type === 'put');
                    return (
                      <tr key={strike} className="strike-row">
                        <td className="price-cell bid">{call?.price || '-'}</td>
                        <td className="price-cell ask">{call?.price * 1.01 || '-'}</td>
                        <td className="greek-cell">{call?.greeks?.delta || '-'}</td>
                        <td className="strike-cell">{strike}</td>
                        <td className="greek-cell">{put?.greeks?.delta || '-'}</td>
                        <td className="price-cell bid">{put?.price || '-'}</td>
                        <td className="price-cell ask">{put?.price * 1.01 || '-'}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default OptionsChainWidget;
