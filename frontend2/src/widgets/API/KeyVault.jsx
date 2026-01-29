import React, { useState } from 'react';
import { Key, Eye, EyeOff, Copy, ShieldCheck } from 'lucide-react';
import useAPIStore from '../../stores/apiStore';
import './KeyVault.css';

const KeyVault = () => {
    const { apiKeys, revokeApiKey } = useAPIStore();
    const [visibleKey, setVisibleKey] = useState(null);

    const toggleKey = (id) => {
        if (visibleKey === id) {
            setVisibleKey(null);
        } else {
            // Simulate auth challenge here
            setVisibleKey(id);
            setTimeout(() => setVisibleKey(null), 10000); // Auto-hide
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
                {apiKeys.length > 0 ? apiKeys.map((key) => (
                    <div key={key.id} className="key-item">
                        <div className="key-meta">
                            <span className="key-name">{key.name}</span>
                            <span className={`expiry ${new Date(key.expires) < new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) ? 'text-red-400' : ''}`}>
                                Exp: {new Date(key.expires).toLocaleDateString()}
                            </span>
                        </div>
                        <div className="key-val-row">
                            <div className="key-input">
                                {visibleKey === key.id ? key.val_masked.replace(/•/g, '') : key.val_masked}
                            </div>
                            <button className="icon-btn" onClick={() => toggleKey(key.id)}>
                                {visibleKey === key.id ? <EyeOff size={14} /> : <Eye size={14} />}
                            </button>
                            <button className="icon-btn"><Copy size={14} /></button>
                            <button className="icon-btn text-red-500 hover:bg-red-500/10" onClick={() => revokeApiKey(key.id)}>Revoke</button>
                        </div>
                    </div>
                )) : (
                    <div className="p-4 text-center text-zinc-500 font-mono text-[10px] uppercase">
                        No active API keys in vault
                    </div>
                )}
            </div>

            <div className="audit-log">
                <h4>Access Audit Log</h4>
                <div className="log-entry">
                    <span className="ts">System</span>
                    <span className="action text-green-400">ACTIVE</span>
                    <span className="resource">Vault Synchronized</span>
                </div>
            </div>
        </div>
    );
};

export default KeyVault;
