import React, { useState } from 'react';

const MessageInspector = ({ topic, messages }) => {
    const [selectedMessage, setSelectedMessage] = useState(null);

    return (
        <div className="inspector-container">
            <header className="inspector-header">
                <h3>MESSAGE_LOG {topic ? `[${topic}]` : '[ALL_TOPICS]'}</h3>
            </header>
            
            <div className="log-area">
                <div className="log-list">
                    {messages.map((msg, i) => (
                        <div 
                            key={i} 
                            className={`log-entry ${selectedMessage === msg ? 'active' : ''}`}
                            onClick={() => setSelectedMessage(msg)}
                        >
                            <span className="timestamp">[{new Date(msg.timestamp).toLocaleTimeString()}]</span>
                            <span className="topic">[{msg.topic}]</span>
                            <span className="payload-preview">{JSON.stringify(msg.payload).slice(0, 100)}...</span>
                        </div>
                    ))}
                </div>
                
                <div className="payload-view">
                    {selectedMessage ? (
                        <pre>{JSON.stringify(selectedMessage.payload, null, 2)}</pre>
                    ) : (
                        <div className="empty-state">SELECT_MESSAGE_TO_INSPECT</div>
                    )}
                </div>
            </div>

            <style jsx>{`
                .inspector-container {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .inspector-header {
                    padding: 10px 15px;
                    border-bottom: 1px solid #1a1a1a;
                }
                .inspector-header h3 {
                    font-size: 0.8rem;
                    color: #fff;
                    margin: 0;
                }
                .log-area {
                    display: grid;
                    grid-template-columns: 1fr 400px;
                    flex: 1;
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
                    white-space: nowrap;
                    overflow: hidden;
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
