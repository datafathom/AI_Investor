import React from 'react';
import './PersonaAvatar.css';

/**
 * Persona Avatar Component 
 * 
 * Displays agent persona with sentiment glow.
 */
const PersonaAvatar = ({ persona, conviction = 0.7 }) => {
    const personas = {
        bull: { emoji: '🐂', color: '#4ade80', name: 'Bull' },
        bear: { emoji: '🐻', color: '#f87171', name: 'Bear' },
        neutral: { emoji: '⚖️', color: '#60a5fa', name: 'Neutral' },
        risk: { emoji: '🛡️', color: '#a78bfa', name: 'Risk Officer' },
    };

    const config = personas[persona] || personas.neutral;
    const glowIntensity = conviction * 20; // 0-20px glow

    return (
        <div 
            className="persona-avatar"
            style={{
                '--persona-color': config.color,
                '--glow-size': `${glowIntensity}px`
            }}
        >
            <div className="avatar-circle">
                <span className="avatar-emoji">{config.emoji}</span>
            </div>
            <span className="avatar-name">{config.name}</span>
        </div>
    );
};

export default PersonaAvatar;
