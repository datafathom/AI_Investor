import React from 'react';
import './MiddlewareStep.css';

const MiddlewareStep = ({ step, index, onToggle, onMove }) => {
    // Basic drag and drop logic could be added with react-dnd, 
    // but for simplicity here we'll use manual move buttons or just UI markers.
    
    return (
        <div className={`middleware-step ${step.enabled ? 'enabled' : 'disabled'}`}>
            <div className="step-order">0{index + 1}</div>
            <div className="step-info">
                <span className="step-name">{step.name}</span>
                <span className="step-id">{step.id.toUpperCase()}</span>
            </div>
            <div className="step-perf">
                <label>AVG_PROC</label>
                <span>{step.avg_ms}ms</span>
            </div>
            <div className="step-controls">
                <label className="switch">
                    <input 
                        type="checkbox" 
                        checked={step.enabled} 
                        onChange={(e) => onToggle(step.id, e.target.checked)}
                    />
                    <span className="slider"></span>
                </label>
            </div>
            <div className="step-drag-handle">⋮⋮</div>
        </div>
    );
};

export default MiddlewareStep;
