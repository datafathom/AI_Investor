import React, { useState, useEffect, useMemo, useRef } from 'react';
import './OptionsChain.css';
import useSymbolLink from '../../hooks/useSymbolLink';
import apiClient from '../../services/apiClient';
// React-Window Import Strategy (Fix for Vite/CJS interop)
import * as ReactWindow from 'react-window';
const List = ReactWindow.FixedSizeList || ReactWindow.default?.FixedSizeList || ReactWindow.default;

const Row = ({ index, style, data }) => {
  const item = data[index];

  if (item.type === 'header') {
    return (
      <div style={style} className="expiry-header-row">
        <span>📅 Expiration: {item.date}</span>
      </div>
    );
  }

  // Data Row
  const { strike, call, put } = item;
  return (
    <div style={style} className="strike-row-virtual">
       <div className="virtual-cell call-bid">{call?.price || '-'}</div>
       <div className="virtual-cell call-ask">{call?.price ? (call.price * 1.01).toFixed(2) : '-'}</div>
       <div className="virtual-cell call-delta">{call?.greeks?.delta || '-'}</div>
       <div className="virtual-cell strike-center">{strike}</div>
       <div className="virtual-cell put-delta">{put?.greeks?.delta || '-'}</div>
       <div className="virtual-cell put-bid">{put?.price || '-'}</div>
       <div className="virtual-cell put-ask">{put?.price ? (put.price * 1.01).toFixed(2) : '-'}</div>
    </div>
  );
};

const OptionsChainWidget = ({ linkingGroup = 'none' }) => {
  const { currentSymbol } = useSymbolLink(linkingGroup);
  const [chain, setChain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const fetchChain = async () => {
      if (!currentSymbol) return;
      setLoading(true);
      try {
        const response = await apiClient.get(`/market/options/${currentSymbol}`);
        setChain(response.data);
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

  // Resize Observer
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver(entries => {
      for (let entry of entries) {
        setDimensions({
          width: entry.contentRect.width,
          height: entry.contentRect.height
        });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Flatten Data
  const flattenedData = useMemo(() => {
    const groups = {};
    chain.forEach(c => {
      if (!groups[c.expiration]) groups[c.expiration] = [];
      groups[c.expiration].push(c);
    });

    const items = [];
    Object.entries(groups).forEach(([expiry, contracts]) => {
      items.push({ type: 'header', date: expiry });
      
      const strikes = Array.from(new Set(contracts.map(c => c.strike))).sort((a,b) => a-b);
      strikes.forEach(strike => {
        const call = contracts.find(c => c.strike === strike && c.type === 'call');
        const put = contracts.find(c => c.strike === strike && c.type === 'put');
        items.push({ type: 'row', strike, call, put });
      });
    });
    return items;
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
    <div className="options-chain-container" ref={containerRef} style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div className="oc-header" style={{ flexShrink: 0 }}>
        <div className="oc-symbol-info">
          <h3>{currentSymbol} Options Chain</h3>
          <span className="oc-badge">Real-time Pulse</span>
        </div>
      </div>

      <div className="oc-table-header-virtual" style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', padding: '8px 16px', background: 'rgba(255,255,255,0.05)', fontSize: '10px', fontWeight: 'bold', color: '#888' }}>
         <div>CALL BID</div>
         <div>CALL ASK</div>
         <div>DELTA</div>
         <div style={{ textAlign: 'center', color: 'white' }}>STRIKE</div>
         <div style={{ textAlign: 'right' }}>DELTA</div>
         <div style={{ textAlign: 'right' }}>PUT BID</div>
         <div style={{ textAlign: 'right' }}>PUT ASK</div>
      </div>

      <div style={{ flex: 1 }}>
        {loading && chain.length === 0 ? (
          <div className="oc-loading">Loading Chain...</div>
        ) : error ? (
          <div className="oc-error">{error}</div>
        ) : (
          <List
            height={Math.max(200, dimensions.height - 80)}
            itemCount={flattenedData.length}
            itemSize={35}
            width={'100%'}
            itemData={flattenedData}
          >
            {Row}
          </List>
        )}
      </div>
    </div>
  );
};

export default OptionsChainWidget;
