import React, { useState } from 'react';
import { Key, Link, Webhook, Plus, Lock, Check, X } from 'lucide-react';
import './APIMarketplace.css';

/**
 * API Marketplace Widget 
 * 
 * Third-party data connectors, API key management, and webhooks.
 */
const APIMarketplace = () => {
    const [showKeyModal, setShowKeyModal] = useState(false);

    const connectors = [
        { name: 'Alpaca', status: 'connected', type: 'broker' },
        { name: 'Polygon.io', status: 'connected', type: 'data' },
        { name: 'OpenAI', status: 'connected', type: 'ai' },
        { name: 'Bloomberg', status: 'pending', type: 'data' },
        { name: 'Finnhub', status: 'disconnected', type: 'data' },
    ];

    const apiKeys = [
        { name: 'Production Key', created: '2025-12-01', lastUsed: '2 min ago', masked: '****-****-****-7a3f' },
        { name: 'Development Key', created: '2025-11-15', lastUsed: '1 day ago', masked: '****-****-****-b2c1' },
    ];

    const webhooks = [
        { url: 'https://my-app.com/webhook/trades', events: ['trade.executed'], active: true },
        { url: 'https://my-app.com/webhook/alerts', events: ['alert.triggered'], active: true },
    ];

    return (
        <div className="api-marketplace">
            <div className="widget-header">
                <Link size={16} />
                <h3>API Integrations</h3>
                <button className="add-btn">
                    <Plus size={14} /> Add
                </button>
            </div>

            <div className="section">
                <h4>Data Connectors</h4>
                <div className="connectors-grid">
                    {connectors.map((c, i) => (
                        <div key={i} className={`connector-card ${c.status}`}>
                            <span className="connector-name">{c.name}</span>
                            <span className={`connector-status ${c.status}`}>
                                {c.status === 'connected' && <Check size={10} />}
                                {c.status === 'disconnected' && <X size={10} />}
                                {c.status}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="section">
                <h4><Key size={12} /> API Keys</h4>
                <div className="keys-list">
                    {apiKeys.map((key, i) => (
                        <div key={i} className="key-row">
                            <div className="key-info">
                                <Lock size={14} />
                                <div>
                                    <span className="key-name">{key.name}</span>
                                    <span className="key-masked">{key.masked}</span>
                                </div>
                            </div>
                            <span className="key-used">Last: {key.lastUsed}</span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="section">
                <h4><Webhook size={12} /> Webhooks</h4>
                <div className="webhooks-list">
                    {webhooks.map((wh, i) => (
                        <div key={i} className="webhook-row">
                            <span className="webhook-url">{wh.url}</span>
                            <div className="webhook-events">
                                {wh.events.map((e, j) => (
                                    <span key={j} className="event-tag">{e}</span>
                                ))}
                            </div>
                            <div className={`webhook-status ${wh.active ? 'active' : ''}`}>
                                {wh.active ? 'Active' : 'Inactive'}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default APIMarketplace;
