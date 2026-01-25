import React, { useState } from 'react';
import { Key, Eye, EyeOff, Copy, ShieldCheck } from 'lucide-react';
import './KeyVault.css';

const KeyVault = () => {
    const [visibleKey, setVisibleKey] = useState(null);

    const toggleKey = (id) => {
        if (visibleKey === id) {
            setVisibleKey(null);
        } else {
            // Simulate auth challenge here
            setVisibleKey(id);
            setTimeout(() => setVisibleKey(null), 5000); // Auto-hide
        }
    };

    return (
        <div className="key-vault-widget">
            <div className="widget-header">
                <h3><Key size={18} className="text-yellow-400" /> API Key Vault (Encrypted)</h3>
                <div className="security-badge">
                     <ShieldCheck size={12} /> HashiCorp Vault
                </div>
            </div>

            <div className="keys-list">
                <div className="key-item">
                    <div className="key-meta">
                        <span className="key-name">OpenAI GPT-4</span>
                        <span className="expiry">Exp: 30 days</span>
                    </div>
                    <div className="key-val-row">
                        <div className="key-input">
                            {visibleKey === 'openai' ? 'sk-proj-89s7df987s9d8f7s9d8f' : 'sk-proj-••••••••••••••••••••'}
                        </div>
                        <button className="icon-btn" onClick={() => toggleKey('openai')}>
                            {visibleKey === 'openai' ? <EyeOff size={14} /> : <Eye size={14} />}
                        </button>
                        <button className="icon-btn"><Copy size={14} /></button>
                    </div>
                </div>

                 <div className="key-item">
                    <div className="key-meta">
                        <span className="key-name">Polygon.io Live</span>
                         <span className="expiry text-red-400">Exp: 2 days</span>
                    </div>
                    <div className="key-val-row">
                        <div className="key-input">
                            {visibleKey === 'poly' ? 'pk_live_89s7df987s9d8f7s9d8f' : 'pk_live_••••••••••••••••••••'}
                        </div>
                         <button className="icon-btn" onClick={() => toggleKey('poly')}>
                            {visibleKey === 'poly' ? <EyeOff size={14} /> : <Eye size={14} />}
                        </button>
                        <button className="icon-btn"><Copy size={14} /></button>
                    </div>
                </div>
            </div>

            <div className="audit-log">
                <h4>Access Audit Log</h4>
                <div className="log-entry">
                    <span className="ts">14:02:11</span>
                    <span className="user">Admin</span>
                    <span className="action text-green-400">REVEALED</span>
                    <span className="resource">OpenAI GPT-4</span>
                </div>
                 <div className="log-entry">
                    <span className="ts">10:45:00</span>
                    <span className="user">System</span>
                    <span className="action text-blue-400">ROTATED</span>
                    <span className="resource">Polygon.io Live</span>
                </div>
            </div>
        </div>
    );
};

export default KeyVault;
