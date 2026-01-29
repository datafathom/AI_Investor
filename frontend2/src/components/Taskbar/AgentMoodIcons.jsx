import React from 'react';
import { Smile, Meh, Frown, Flame, Zap } from 'lucide-react';
import useTaskbarStore from '../../stores/taskbarStore';
import './AgentMoodIcons.css';

const AgentMoodIcons = () => {
    const agentMoods = useTaskbarStore((state) => state.agentMoods);
    
    // Default moods if none are provided
    const displayMoods = Object.keys(agentMoods).length > 0 
        ? agentMoods 
        : { 'Alpha': 'happy', 'Beta': 'neutral', 'Gamma': 'stressed' };

    const getMoodIcon = (mood) => {
        switch (mood) {
            case 'happy': return <Smile size={16} color="#00ff88" />;
            case 'neutral': return <Meh size={16} color="#57606f" />;
            case 'stressed': return <Frown size={16} color="#ffa502" />;
            case 'panic': return <Flame size={16} color="#ff4757" className="animate-pulse" />;
            case 'aggressive': return <Zap size={16} color="#fffa65" className="animate-bounce" />;
            default: return <Meh size={16} color="#57606f" />;
        }
    };

    return (
        <div className="agent-mood-container">
            {Object.entries(displayMoods).map(([agentId, mood]) => (
                <div key={agentId} className={`agent-mood-item ${mood}`} title={`${agentId}: ${mood}`}>
                    {getMoodIcon(mood)}
                </div>
            ))}
        </div>
    );
};

export default AgentMoodIcons;
