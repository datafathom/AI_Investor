import React, { useState, useEffect } from 'react';
import './DOM.css';
import useSymbolLink from '../../hooks/useSymbolLink';

const DOMWidget = ({ linkingGroup = 'none' }) => {
  const { currentSymbol } = useSymbolLink(linkingGroup);
  const [depth, setDepth] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchDepth = async () => {
      if (!currentSymbol) return;
      try {
        const response = await fetch(`http://localhost:5050/api/v1/market/dom/${currentSymbol}`);
        const data = await response.json();
        setDepth(data);
      } catch (err) {
        console.error("DOM Fetch error:", err);
      }
    };

    fetchDepth();
    const interval = setInterval(fetchDepth, 2000); // Fast pulse for DOM
    return () => clearInterval(interval);
  }, [currentSymbol]);

  if (!currentSymbol) {
    return (
      <div className="dom-empty">
        <p>Link to a symbol group for Level 2 Depth</p>
      </div>
    );
  }

  return (
    <div className="dom-container">
      <div className="dom-header">
        <div className="ticker-badge">{currentSymbol}</div>
        <div className="dom-title">Market Depth (L2)</div>
      </div>

      <div className="dom-ladder-header">
        <div className="col-size">Size</div>
        <div className="col-price">Price</div>
        <div className="col-size">Size</div>
      </div>

      <div className="dom-scroller">
        {/* ASKS (Sells) - Top down from highest price down to best ask */}
        <div className="depth-group asks">
          {depth?.asks.slice().reverse().map((ask, i) => (
            <div key={i} className="dom-row ask-row">
              <div className="col-size empty"></div>
              <div className="col-price">{ask.price}</div>
              <div className="col-size">
                <div 
                  className="size-bar ask-bar" 
                  style={{ width: `${Math.min(ask.size / 50, 100)}%` }}
                />
                <span className="size-label">{ask.size}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Midpoint / The Gap */}
        <div className="dom-midpoint">
          <div className="mid-label">S P R E A D : {depth?.spread || '0.05'}</div>
        </div>

        {/* BIDS (Buys) - Best bid down to lowest price */}
        <div className="depth-group bids">
          {depth?.bids.map((bid, i) => (
            <div key={i} className="dom-row bid-row">
              <div className="col-size">
                <div 
                  className="size-bar bid-bar" 
                  style={{ width: `${Math.min(bid.size / 50, 100)}%` }}
                />
                <span className="size-label">{bid.size}</span>
              </div>
              <div className="col-price">{bid.price}</div>
              <div className="col-size empty"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DOMWidget;
