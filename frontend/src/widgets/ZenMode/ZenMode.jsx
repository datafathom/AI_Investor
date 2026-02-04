import React, { useState } from 'react';
import { Feather, Target, Clock, Power, Check } from 'lucide-react';
import './ZenMode.css';

/**
 * Homeostasis Zen Mode (Phase 24)
 * 
 * Minimalist goal tracking with autopilot master override.
 */
const ZenMode = () => {
    const [autopilotEnabled, setAutopilotEnabled] = useState(true);

    const enoughMetric = {
        target: 5000000,
        current: 3200000,
        percent: 64,
    };

    const retirementData = {
        targetAge: 55,
        currentAge: 38,
        yearsRemaining: 17,
        monthlyContribution: 8500,
        projectedValue: 6800000,
    };

    const goals = [
        { name: 'Financial Independence', target: '$5M', progress: 64, status: 'on-track' },
        { name: 'Passive Income', target: '$15K/mo', progress: 45, status: 'on-track' },
        { name: 'Zero Debt', target: '$0', progress: 100, status: 'achieved' },
    ];

    return (
        <div className="zen-mode">
            <div className="widget-header">
                <Feather size={16} />
                <h3>Zen Mode</h3>
            </div>

            <div className="enough-section">
                <div className="enough-circle">
                    <svg viewBox="0 0 100 100">
                        <circle
                            cx="50" cy="50" r="45"
                            fill="none"
                            stroke="var(--border-primary)"
                            strokeWidth="6"
                        />
                        <circle
                            cx="50" cy="50" r="45"
                            fill="none"
                            stroke="var(--color-success)"
                            strokeWidth="6"
                            strokeDasharray={`${enoughMetric.percent * 2.83} 283`}
                            strokeLinecap="round"
                            transform="rotate(-90 50 50)"
                        />
                    </svg>
                    <div className="enough-inner">
                        <span className="enough-percent">{enoughMetric.percent}%</span>
                        <span className="enough-label">to "Enough"</span>
                    </div>
                </div>
                <div className="enough-target">
                    <span className="current">${(enoughMetric.current / 1000000).toFixed(1)}M</span>
                    <span className="divider">/</span>
                    <span className="target">${(enoughMetric.target / 1000000).toFixed(0)}M</span>
                </div>
            </div>

            <div className="retirement-countdown">
                <Clock size={14} />
                <div className="countdown-info">
                    <span className="countdown-value">{retirementData.yearsRemaining} years</span>
                    <span className="countdown-label">to target retirement (age {retirementData.targetAge})</span>
                </div>
            </div>

            <div className="goals-section">
                <h4><Target size={12} /> Life Goals</h4>
                {goals.map((goal, i) => (
                    <div key={i} className={`goal-row ${goal.status}`}>
                        <div className="goal-info">
                            <span className="goal-name">{goal.name}</span>
                            <span className="goal-target">{goal.target}</span>
                        </div>
                        <div className="goal-progress">
                            <div className="progress-bar">
                                <div className="progress-fill" style={{ width: `${goal.progress}%` }}></div>
                            </div>
                            {goal.status === 'achieved' && <Check size={14} className="achieved-icon" />}
                        </div>
                    </div>
                ))}
            </div>

            <div className="autopilot-section" onClick={() => setAutopilotEnabled(!autopilotEnabled)}>
                <div className="autopilot-info">
                    <Power size={16} />
                    <div>
                        <span className="autopilot-label">System Autopilot</span>
                        <span className="autopilot-desc">AI manages portfolio automatically</span>
                    </div>
                </div>
                <div className={`autopilot-toggle ${autopilotEnabled ? 'on' : ''}`}>
                    <div className="toggle-knob"></div>
                </div>
            </div>
        </div>
    );
};

export default ZenMode;
