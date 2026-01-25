import React, { useState, useRef, useEffect } from 'react';
import { Send, RotateCcw, Download, MessageSquare } from 'lucide-react';
import useDebateStore from '../../stores/debateStore';
import './AgentChat.css';

/**
 * AgentChat - Multi-Agent Debate Chat Interface
 * 
 * Phase 55: Real-time chat interface showing Bull vs Bear persona debates
 * with typing indicators, sentiment glow, and user argument injection.
 */
const AgentChat = ({ ticker = 'SPY' }) => {
    const [userInput, setUserInput] = useState('');
    const messagesEndRef = useRef(null);
    
    const {
        messages,
        personas,
        typingPersona,
        isDebating,
        isLoading,
        currentTicker,
        triggerDebate,
        injectArgument,
        exportDebate,
        reset
    } = useDebateStore();
    
    // Auto-scroll to bottom on new messages
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, typingPersona]);
    
    const handleStartDebate = () => {
        triggerDebate(ticker);
    };
    
    const handleInjectArgument = (e) => {
        e.preventDefault();
        if (userInput.trim() && !isLoading) {
            injectArgument(userInput.trim());
            setUserInput('');
        }
    };
    
    const handleExport = () => {
        const data = exportDebate();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `debate_${currentTicker}_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    };
    
    const getSentimentClass = (sentiment) => {
        switch (sentiment) {
            case 'bull': return 'sentiment-bull';
            case 'bear': return 'sentiment-bear';
            default: return 'sentiment-neutral';
        }
    };
    
    const getPersonaAvatar = (personaId) => {
        const persona = personas.find(p => p.id === personaId);
        return persona?.avatar || '🤖';
    };
    
    const getPersonaName = (personaId) => {
        const persona = personas.find(p => p.id === personaId);
        return persona?.name || personaId;
    };
    
    return (
        <div className="agent-chat-widget">
            <div className="chat-header">
                <div className="header-title">
                    <MessageSquare size={16} />
                    <h3>Debate Chamber</h3>
                    {currentTicker && <span className="ticker-badge">{currentTicker}</span>}
                </div>
                <div className="header-actions">
                    <button 
                        className="action-btn" 
                        onClick={handleStartDebate}
                        disabled={isLoading}
                        title="Start New Debate"
                    >
                        <RotateCcw size={14} />
                    </button>
                    <button 
                        className="action-btn" 
                        onClick={handleExport}
                        disabled={messages.length === 0}
                        title="Export Debate"
                    >
                        <Download size={14} />
                    </button>
                </div>
            </div>
            
            <div className="persona-bar">
                {personas.map(persona => (
                    <div 
                        key={persona.id} 
                        className={`persona-chip ${persona.type} ${typingPersona === persona.id ? 'typing' : ''}`}
                    >
                        <span className="avatar">{persona.avatar}</span>
                        <span className="name">{persona.name}</span>
                        {persona.currentVote && (
                            <span className={`vote-badge ${persona.currentVote.toLowerCase()}`}>
                                {persona.currentVote}
                            </span>
                        )}
                    </div>
                ))}
            </div>
            
            <div className="messages-container">
                {messages.length === 0 && !isDebating && (
                    <div className="empty-state">
                        <MessageSquare size={48} />
                        <p>Start a debate to see AI personas discuss {ticker}</p>
                        <button className="start-btn" onClick={handleStartDebate}>
                            Start Debate
                        </button>
                    </div>
                )}
                
                {messages.map((msg, idx) => (
                    <div 
                        key={msg.id || idx} 
                        className={`message ${getSentimentClass(msg.sentiment)} ${msg.personaId === 'user' ? 'user-message' : ''}`}
                    >
                        <div className="message-avatar">
                            {msg.personaId === 'user' ? '👤' : getPersonaAvatar(msg.personaId)}
                        </div>
                        <div className="message-content">
                            <div className="message-header">
                                <span className="persona-name">
                                    {msg.personaId === 'user' ? 'You' : msg.personaName}
                                </span>
                                <span className="message-signal">{msg.signal}</span>
                                <span className="confidence">
                                    {Math.round(msg.confidence * 100)}% confidence
                                </span>
                            </div>
                            <p className="message-text">{msg.content}</p>
                        </div>
                    </div>
                ))}
                
                {typingPersona && (
                    <div className="message typing-indicator">
                        <div className="message-avatar">{getPersonaAvatar(typingPersona)}</div>
                        <div className="message-content">
                            <div className="typing-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                )}
                
                <div ref={messagesEndRef} />
            </div>
            
            <form className="input-area" onSubmit={handleInjectArgument}>
                <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    placeholder="Inject a counter-argument..."
                    disabled={isLoading || messages.length === 0}
                />
                <button 
                    type="submit" 
                    disabled={!userInput.trim() || isLoading}
                    title="Branch debate with your argument"
                >
                    <Send size={16} />
                </button>
            </form>
        </div>
    );
};

export default AgentChat;
