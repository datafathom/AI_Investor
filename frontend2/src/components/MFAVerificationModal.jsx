import React, { useState, useEffect, useRef } from 'react';
import { Shield, Key, CheckCircle, AlertCircle, X } from 'lucide-react';
import apiClient from '../services/apiClient';
import './MFAVerificationModal.css';

const MFAVerificationModal = ({ isOpen, onClose, onSuccess, onFail, actionName = "this action" }) => {
    const [code, setCode] = useState(['', '', '', '', '', '']);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const inputRefs = useRef([]);

    useEffect(() => {
        if (isOpen) {
            setCode(['', '', '', '', '', '']);
            setError(null);
            setSuccess(false);
            setTimeout(() => inputRefs.current[0]?.focus(), 100);
        }
    }, [isOpen]);

    const handleChange = (e, index) => {
        const value = e.target.value;
        if (!/^[0-9]?$/.test(value)) return;

        const newCode = [...code];
        newCode[index] = value;
        setCode(newCode);

        // Move to next input
        if (value && index < 5) {
            inputRefs.current[index + 1].focus();
        }
    };

    const handleKeyDown = (e, index) => {
        if (e.key === 'Backspace' && !code[index] && index > 0) {
            inputRefs.current[index - 1].focus();
        }
    };

    const handleVerify = async () => {
        const fullCode = code.join('');
        if (fullCode.length !== 6) {
            setError("Please enter all 6 digits.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // In dev/mock mode, we pass a dummy secret or the backend handles specific mock codes
            // Note: Using apiClient with full path since /auth is not prefixed with /api/v1
            const res = await apiClient.post('/auth/mfa/verify', { 
                code: fullCode,
                secret: 'DEMO_SECRET' // In production, this would be handled server-side via session
            });

            if (res.data.valid) {
                setSuccess(true);
                setTimeout(() => {
                    onSuccess?.(fullCode);
                    onClose();
                }, 1000);
            }
        } catch (err) {
            setError(err.response?.data?.error || "Invalid verification code.");
            onFail?.();
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="mfa-modal-overlay">
            <div className="mfa-modal-container animate-scale-in">
                <button className="mfa-close-btn" onClick={onClose}><X size={20} /></button>
                
                <div className="mfa-modal-header">
                    <div className="mfa-icon-shield">
                        <Shield size={32} className="text-cyan-400" />
                    </div>
                    <h2>Secure Verification</h2>
                    <p>Enter the 6-digit code to authorize <strong>{actionName}</strong>.</p>
                </div>

                <div className="mfa-code-inputs">
                    {code.map((digit, index) => (
                        <input
                            key={index}
                            ref={el => inputRefs.current[index] = el}
                            type="text"
                            maxLength="1"
                            value={digit}
                            onChange={(e) => handleChange(e, index)}
                            onKeyDown={(e) => handleKeyDown(e, index)}
                            className={error ? 'error' : success ? 'success' : ''}
                            disabled={loading || success}
                        />
                    ))}
                </div>

                {error && (
                    <div className="mfa-error-msg animate-shake">
                        <AlertCircle size={14} />
                        <span>{error}</span>
                    </div>
                )}

                {success && (
                    <div className="mfa-success-msg">
                        <CheckCircle size={14} />
                        <span>Authorization Granted</span>
                    </div>
                )}

                <div className="mfa-modal-footer">
                    <button 
                        className="mfa-verify-btn" 
                        onClick={handleVerify}
                        disabled={loading || success || code.join('').length < 6}
                    >
                        {loading ? "Verifying..." : "Confirm Identity"}
                    </button>
                    <p className="mfa-hint">
                        <Key size={12} /> Hardware token supported (e.g. YubiKey)
                    </p>
                </div>
            </div>
        </div>
    );
};

export default MFAVerificationModal;
