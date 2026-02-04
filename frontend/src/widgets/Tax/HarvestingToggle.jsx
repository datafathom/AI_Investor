import React, { useState } from 'react';
import { Shield, ShieldAlert, Fingerprint, Lock, CheckCircle2 } from 'lucide-react';
import { useTaxStore } from '../../stores/taxStore';
import './HarvestingToggle.css';

const HarvestingToggle = () => {
    const { autoHarvestEnabled, toggleAutoHarvest } = useTaxStore();
    const [isAuthenticating, setIsAuthenticating] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);

    const handleToggle = () => {
        if (!autoHarvestEnabled) {
            // Activate flow (mock biometric)
            setIsAuthenticating(true);
            setTimeout(() => {
                setIsAuthenticating(false);
                setShowSuccess(true);
                toggleAutoHarvest(true);
                setTimeout(() => setShowSuccess(false), 2000);
            }, 1000);
        } else {
            // Deactivate immediately
            toggleAutoHarvest(false);
        }
    };

    return (
        <div className={`harvesting-toggle-widget h-full flex items-center justify-between px-6 py-2 ${autoHarvestEnabled ? 'active' : ''}`}>
            <div className="shield-status flex items-center gap-4">
                {autoHarvestEnabled ? (
                    <div className="p-3 bg-green-500/20 rounded-full text-green-500 animate-pulse relative">
                        <Shield size={32} />
                        <div className="absolute inset-0 bg-green-500/20 rounded-full animate-ping"></div>
                    </div>
                ) : (
                    <div className="p-3 bg-slate-800 rounded-full text-slate-500">
                        <ShieldAlert size={32} />
                    </div>
                )}
                
                <div className="flex flex-col">
                    <h3 className="text-white font-bold text-sm tracking-wide">AUTO-HARVEST PROTOCOL</h3>
                    <p className={`text-xs font-mono font-medium ${autoHarvestEnabled ? 'text-green-400' : 'text-slate-500'}`}>
                        {autoHarvestEnabled ? 'PROTECTION ACTIVE' : 'SYSTEM IDLE'}
                    </p>
                </div>
            </div>
            
            <div className="toggle-controls">
                <button 
                    className={`
                        relative overflow-hidden group px-6 py-2.5 rounded-lg font-bold text-xs tracking-wider transition-all duration-300 flex items-center gap-2
                        ${autoHarvestEnabled 
                            ? 'bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30' 
                            : 'bg-green-500/10 hover:bg-green-500/20 text-green-400 border border-green-500/30'}
                        ${isAuthenticating ? 'cursor-wait opacity-80' : ''}
                    `}
                    onClick={handleToggle}
                    disabled={isAuthenticating}
                >
                    {isAuthenticating ? (
                        <>
                            <Fingerprint size={16} className="animate-pulse" /> SCANNING...
                        </>
                    ) : showSuccess ? (
                        <>
                            <CheckCircle2 size={16} /> CONFIRMED
                        </>
                    ) : (
                        autoHarvestEnabled ? 'DEACTIVATE' : 'ACTIVATE SHIELD'
                    )}
                </button>
            </div>
        </div>
    );
};

export default HarvestingToggle;
