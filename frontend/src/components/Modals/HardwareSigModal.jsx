/**
 * ==============================================================================
 * FILE: frontend2/src/components/Modals/HardwareSigModal.jsx
 * ROLE: Hardware Multi-Sig Signature UI
 * PURPOSE: Global modal that prompts users to connect and authorize 
 *          high-value transactions using physical devices.
 * ==============================================================================
 */

import React from 'react';
import { ShieldAlert, Cpu, CheckCircle, XCircle, RotateCcw, X } from 'lucide-react';
import useHardwareStore from '../../stores/hardwareStore';
import './HardwareSigModal.css';

const HardwareSigModal = () => {
    const { 
        isWaitingForSignature, 
        currentPayload, 
        status, 
        error, 
        executeSign, 
        cancelSignature 
    } = useHardwareStore();

    if (!isWaitingForSignature) return null;

    const getStatusContent = () => {
        switch (status) {
            case 'requesting':
                return {
                    icon: <Cpu className="text-blue-400 animate-pulse" />,
                    title: 'Hardware Signature Required',
                    desc: 'A high-value transaction has been detected. Please connect your Ledger or Trezor to authorize.'
                };
            case 'signing':
                return {
                    icon: <div className="spinner-border text-purple-400" />,
                    title: 'Waiting for Device',
                    desc: 'Verify the transaction details on your hardware screen and confirm the signature.'
                };
            case 'completed':
                return {
                    icon: <CheckCircle className="text-emerald-400" />,
                    title: 'Signature Verified',
                    desc: 'Transaction successfully signed by physical hardware.'
                };
            case 'failed':
                return {
                    icon: <XCircle className="text-red-400" />,
                    title: 'Signing Failed',
                    desc: error || 'An error occurred during communication with the device.'
                };
            default:
                return {};
        }
    };

    const content = getStatusContent();

    return (
        <div className="hw-modal-overlay">
            <div className="hw-modal">
                <div className="hw-modal__header">
                    <div className="flex items-center gap-2">
                        <ShieldAlert size={18} className="text-amber-500" />
                        <span className="text-xs font-black uppercase tracking-widest text-slate-400">Security Clearance Level 4</span>
                    </div>
                    <button onClick={cancelSignature} className="text-slate-500 hover:text-white">
                        <X size={20} />
                    </button>
                </div>

                <div className="hw-modal__body">
                    <div className="hw-modal__icon-box">
                        {content.icon}
                    </div>
                    <h2 className="hw-modal__title">{content.title}</h2>
                    <p className="hw-modal__desc">{content.desc}</p>

                    {/* Transaction Preview */}
                    {currentPayload && (
                        <div className="hw-modal__payload">
                            <div className="text-[10px] uppercase text-slate-500 mb-2">Transaction Details</div>
                            <div className="space-y-1">
                                <div className="flex justify-between text-xs">
                                    <span className="text-slate-400">Endpoint:</span>
                                    <span className="text-white font-mono">{currentPayload.endpoint || 'Withdrawal'}</span>
                                </div>
                                <div className="flex justify-between text-xs">
                                    <span className="text-slate-400">Amount:</span>
                                    <span className="text-emerald-400 font-bold">${currentPayload.amount?.toLocaleString() || '---'}</span>
                                </div>
                                <div className="flex justify-between text-xs">
                                    <span className="text-slate-400">Recipient:</span>
                                    <span className="text-white truncate max-w-[150px]">{currentPayload.to || 'Self'}</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                <div className="hw-modal__footer">
                    {status === 'failed' ? (
                        <button onClick={executeSign} className="hw-btn hw-btn--retry">
                            <RotateCcw size={16} /> Retry Signature
                        </button>
                    ) : (
                        <button 
                            onClick={executeSign} 
                            disabled={status === 'signing' || status === 'completed'}
                            className="hw-btn hw-btn--primary"
                        >
                            Authorize with Device
                        </button>
                    )}
                    <button onClick={cancelSignature} className="hw-btn hw-btn--cancel">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
};

export default HardwareSigModal;
