/**
 * ==============================================================================
 * FILE: frontend2/src/components/ViralAlertBadge.jsx
 * ROLE: Visual Indicator
 * PURPOSE: Displays a pulsing badge when social sentiment velocity exceeds 
 *          standard deviation thresholds (Viral Event).
 * ==============================================================================
 */
import React from 'react';
import './ViralAlertBadge.css';

const ViralAlertBadge = ({ type = 'viral' }) => {
    return (
        <span className={`viral-badge ${type}`}>
            <span className="vb-icon">🔥</span>
            <span className="vb-text">VIRAL</span>
            <span className="vb-ring"></span>
        </span>
    );
};

export default ViralAlertBadge;
