/**
 * ==============================================================================
 * FILE: frontend2/src/components/Checkout/PayPalButton.jsx
 * ROLE: Payment Component
 * PURPOSE: Mock implementation of PayPal Smart Payment Button.
 *          Simulates popup -> approve -> capture flow.
 * ==============================================================================
 */

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './PayPalButton.css';

const PayPalButton = ({ amount, currency = "USD", onSuccess, onError, mock = true }) => {
    const [loading, setLoading] = useState(false);

    const handlePayPalClick = async () => {
        setLoading(true);
        try {
            // Step 1: Create Order
            const createRes = await fetch(`/api/v1/payment/paypal/create-order?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount, currency })
            });
            const order = await createRes.json();
            
            if (!createRes.ok) throw new Error(order.error || 'Failed to create order');

            // Step 2: Simulate User Approval (Popup)
            // In real integration, we'd use the PayPal JS SDK which handles the popup
            const userApproved = window.confirm(`[MOCK PAYPAL]\n\nPay $${amount} to AI Investor?\n\n(Click OK to Approve, Cancel to Reject)`);
            
            if (!userApproved) {
                setLoading(false);
                return;
            }

            // Step 3: Capture Order
            const captureRes = await fetch('/api/v1/payment/paypal/capture-order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: order.id })
            });
            const capture = await captureRes.json();

            if (!captureRes.ok) throw new Error(capture.error || 'Failed to capture order');

            if (onSuccess) onSuccess(capture);

        } catch (error) {
            console.error("PayPal Error:", error);
            if (onError) onError(error.message);
            alert(`Payment Failed: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <button 
            className={`paypal-button ${loading ? 'loading' : ''}`} 
            onClick={handlePayPalClick}
            disabled={loading}
        >
            {loading ? (
                <span className="spinner"></span>
            ) : (
                <div className="label">
                    <span className="pp-text">Pay with</span> 
                    <span className="pp-logo">PayPal</span>
                    {mock && <span className="mock-tag">(MOCK)</span>}
                </div>
            )}
        </button>
    );
};

PayPalButton.propTypes = {
    amount: PropTypes.number.isRequired,
    currency: PropTypes.string,
    onSuccess: PropTypes.func,
    onError: PropTypes.func,
    mock: PropTypes.bool
};

export default PayPalButton;
