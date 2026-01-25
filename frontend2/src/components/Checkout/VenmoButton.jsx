/**
 * ==============================================================================
 * FILE: frontend2/src/components/Checkout/VenmoButton.jsx
 * ROLE: Payment Component
 * PURPOSE: Mock implementation of Venmo Payment Button.
 *          Simulates mobile app switch -> approval.
 * ==============================================================================
 */

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './VenmoButton.css';

const VenmoButton = ({ amount, onSuccess, onError, mock = true }) => {
    const [loading, setLoading] = useState(false);

    const handleVenmoClick = async () => {
        setLoading(true);
        try {
            // Simulate User Approval (Mobile App Switch)
            // In real integration, this opens the Venmo app or web flow
            const userApproved = window.confirm(`[MOCK VENMO]\n\nOpen Venmo to pay $${amount}?\n\n(Click OK to Switch App & Approve)`);
            
            if (!userApproved) {
                setLoading(false);
                return;
            }

            const response = await fetch(`/api/v1/payment/venmo/pay?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount })
            });
            
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Venmo payment failed');

            if (onSuccess) onSuccess(result);

        } catch (error) {
            console.error("Venmo Error:", error);
            if (onError) onError(error.message);
            alert(`Payment Failed: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <button 
            className={`venmo-button ${loading ? 'loading' : ''}`} 
            onClick={handleVenmoClick}
            disabled={loading}
        >
            {loading ? (
                <span className="spinner"></span>
            ) : (
                <div className="label">
                    <span className="v-logo">venmo</span>
                    {mock && <span className="mock-tag">(MOCK)</span>}
                </div>
            )}
        </button>
    );
};

VenmoButton.propTypes = {
    amount: PropTypes.number.isRequired,
    onSuccess: PropTypes.func,
    onError: PropTypes.func,
    mock: PropTypes.bool
};

export default VenmoButton;
