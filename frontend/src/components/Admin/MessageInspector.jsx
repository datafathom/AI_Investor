import React, { useState, useEffect, useRef } from 'react';

const MessageInspector = ({ topic, messages }) => {
    const [selectedMessage, setSelectedMessage] = useState(null);
    const scrollRef = useRef(null);
    const [isAutoScrollEnabled, setIsAutoScrollEnabled] = useState(true);

    // Auto-scroll logic
    useEffect(() => {
        if (isAutoScrollEnabled && scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isAutoScrollEnabled]);

    const handleScroll = (e) => {
        const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
        const isAtBottom = scrollHeight - scrollTop <= clientHeight + 50;
        setIsAutoScrollEnabled(isAtBottom);
    };

    const getPriorityColor = (priority) => {
        switch (priority?.toUpperCase()) {
            case 'CRITICAL': return '#ff4757';
            case 'HIGH': return '#ffa502';
            case 'MEDIUM': return '#eccc68';
            case 'LOW': return '#00f2ff';
            default: return '#888';
        }
    };

    return (
        <div className="inspector-container">
            <header className="inspector-header">
                <h3>MESSAGE_LOG {topic ? `[${topic}]` : '[ALL_TOPICS]'}</h3>
                {isAutoScrollEnabled && <span className="auto-scroll-badge">AUTO_SCROLL_LOCKED</span>}
            </header>
            
            <div className="log-area">
                <div 
                    className="log-list custom-scrollbar-cyber" 
                    ref={scrollRef}
                    onScroll={handleScroll}
                >
                    {messages.map((msg, i) => {
                        const priority = msg.payload?.priority || "LOW";
                        const pColor = getPriorityColor(priority);
                        
                        return (
                            <div 
                                key={i} 
                                className={`log-entry ${selectedMessage === msg ? 'active' : ''}`}
                                onClick={() => setSelectedMessage(msg)}
                                style={{ borderLeft: `2px solid ${pColor}` }}
                            >
                                <span className="priority-indicator" style={{ background: pColor }} />
                                <span className="timestamp">[{new Date(msg.timestamp).toLocaleTimeString()}]</span>
                                <span className="topic" style={{ color: pColor }}>[{msg.topic}]</span>
                                <span className="payload-preview">{JSON.stringify(msg.payload).slice(0, 80)}...</span>
                            </div>
                        );
                    })}
                </div>
                
                <div className="payload-view custom-scrollbar-cyber">
                    {selectedMessage ? (
                        <pre>{JSON.stringify(selectedMessage.payload, null, 2)}</pre>
                    ) : (
                        <div className="empty-state">SELECT_MESSAGE_TO_INSPECT</div>
                    )}
                </div>
            </div>

            <style jsx="true">{`
                .inspector-container {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .inspector-header {
                    padding: 8px 15px;
                    border-bottom: 1px solid #1a1a1a;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .auto-scroll-badge {
                    font-size: 0.6rem;
                    color: #00f2ff;
                    border: 1px solid #00f2ff;
                    padding: 1px 4px;
                    border-radius: 2px;
                    background: rgba(0, 242, 255, 0.1);
                    font-weight: 800;
                }
                .inspector-header h3 {
                    font-size: 0.75rem;
                    color: #fff;
                    margin: 0;
                    letter-spacing: 0.05em;
                }
                .log-area {
                    display: grid;
                    grid-template-columns: 1fr 400px;
                    flex: 1;
                    min-height: 0; /* Remove fixed 500px height to allow flex growth */
                    overflow: hidden;
                }
                .log-list {
                    border-right: 1px solid #1a1a1a;
                    overflow-y: auto;
                    padding: 5px;
                }
                .log-entry {
                    padding: 5px 10px;
                    font-size: 0.75rem;
                    cursor: pointer;
                    display: flex;
                    gap: 10px;
                    align-items: flex-start;
                    white-space: nowrap;
                    overflow: hidden;
                }
                .priority-indicator {
                    width: 7px;
                    height: 7px;
                    min-width: 7px;
                    border-radius: 50%;
                    margin-top: 4px;
                    box-shadow: 0 0 6px rgba(255, 255, 255, 0.4);
                    flex-shrink: 0;
                }
                .log-entry:hover {
                    background: rgba(255, 255, 255, 0.05);
                }
                .log-entry.active {
                    background: rgba(0, 242, 255, 0.1);
                    color: #00f2ff;
                }
                .timestamp { color: #555; }
                .topic { color: #888; font-weight: bold; }
                .payload-preview { color: #aaa; }
                
                .payload-view {
                    padding: 15px;
                    overflow-y: auto;
                    background: #020202;
                }
                .payload-view pre {
                    font-size: 0.75rem;
                    color: #00ff88;
                }
                .empty-state {
                    display: flex;
                    height: 100%;
                    justify-content: center;
                    align-items: center;
                    color: #444;
                    font-size: 0.8rem;
                }
            `}</style>
        </div>
    );
};

export default MessageInspector;
