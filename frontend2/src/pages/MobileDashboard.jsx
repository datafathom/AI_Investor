import React, { useState } from 'react';
import { StorageService } from '../utils/storageService';
import { Smartphone } from 'lucide-react';
import BiometricKill from '../widgets/Mobile/BiometricKill';
import TradeAuth from '../widgets/Mobile/TradeAuth';
import HapticAlerts from '../widgets/Mobile/HapticAlerts';
import MFAVerificationModal from '../components/MFAVerificationModal';
import useMobileStore from '../stores/mobileStore';
import '../widgets/Mobile/BiometricKill.css'; 

const MobileDashboard = () => {
    const [isMfaOpen, setIsMfaOpen] = useState(false);
    const { activateKillSwitch, killSwitchActive } = useMobileStore();

    // This function will be called AFTER MFA success
    const handleKillSwitchAction = async () => {
        try {
            console.log("MFA Confirmed. Kill Switch Activated.");
            await activateKillSwitch("MFA_PROVED");
            if (!killSwitchActive) {
                alert("EMERGENCY KILL SWITCH ACTIVATED!");
            }
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="full-bleed-page mobile-dashboard-page">
            <header className="mb-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-zinc-800 rounded-xl border border-zinc-700">
                        <Smartphone size={32} className="text-zinc-100" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold">Warden: Mobile Quick-Actions</h1>
                        <p className="text-zinc-500 text-sm">Emergency protocols and biometric authentication simulator.</p>
                    </div>
                </div>
            </header>
            
            <MFAVerificationModal 
                isOpen={isMfaOpen} 
                onClose={() => setIsMfaOpen(false)} 
                onSuccess={handleKillSwitchAction}
                actionName="Global Kill Switch"
            />

            <div className="scrollable-content-wrapper">
                <div className="flex flex-wrap gap-8 justify-center py-8">
                {/* Simulator Containers for Mobile Widgets */}
                <div 
                    style={{ width: '300px', height: '600px', border: '10px solid #333', borderRadius: '30px', overflow: 'hidden', background: '#000', position: 'relative', cursor: 'pointer' }}
                    onClick={() => setIsMfaOpen(true)} // Hijacking click for demo purposes to trigger MFA
                >
                    <div style={{ position: 'absolute', top: '0', left: '0', right: '0', padding: '10px', background: '#333', color: '#fff', textAlign: 'center', fontSize: '10px', pointerEvents: 'none' }}>
                        Device 1: Kill Switch (Click to Trigger)
                    </div>
                    <div style={{ marginTop: '30px', height: 'calc(100% - 30px)', background: 'var(--bg-primary)', pointerEvents: 'none' }}>
                        <BiometricKill />
                    </div>
                </div>

                <div style={{ width: '300px', height: '600px', border: '10px solid #333', borderRadius: '30px', overflow: 'hidden', background: '#000', position: 'relative' }}>
                    <div style={{ position: 'absolute', top: '0', left: '0', right: '0', padding: '10px', background: '#333', color: '#fff', textAlign: 'center', fontSize: '10px' }}>
                        Device 2: Trade Auth
                    </div>
                     <div style={{ marginTop: '30px', height: 'calc(100% - 30px)', background: 'var(--bg-primary)' }}>
                         <TradeAuth />
                    </div>
                </div>

                <div style={{ width: '300px', height: '600px', border: '10px solid #333', borderRadius: '30px', overflow: 'hidden', background: '#000', position: 'relative' }}>
                     <div style={{ position: 'absolute', top: '0', left: '0', right: '0', padding: '10px', background: '#333', color: '#fff', textAlign: 'center', fontSize: '10px' }}>
                        Device 3: Alerts
                    </div>
                     <div style={{ marginTop: '30px', height: 'calc(100% - 30px)', background: 'var(--bg-primary)' }}>
                         <HapticAlerts />
                    </div>
                </div>
            </div>
            </div>
            
            <div className="scroll-buffer-100" />
        </div>
    );
};

export default MobileDashboard;
