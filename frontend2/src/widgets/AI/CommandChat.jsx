/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/AI/CommandChat.jsx
 * ROLE: Natural Language Command Interface
 * PURPOSE: Allows users to type natural language commands (e.g., "Buy 10 shares
 *          of AAPL") and execute generated Python code via the Autocoder agent.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/ai/autocoder/generate: Backend API endpoint
 *     - AutocoderAgent: Code generation and execution
 *     
 * FEATURES:
 *     - Natural language command parsing
 *     - Code generation and preview
 *     - Execution confirmation before running
 *     - Chat history persistence (last 20 messages)
 *     - Streaming response display
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import apiClient from '../../services/apiClient';
import { StorageService } from '../../utils/storageService';
import './CommandChat.css';

const API_BASE = '/ai/autocoder';

/**
 * CommandChat Component
 */
const CommandChat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [streaming, setStreaming] = useState(false);
    const [streamingContent, setStreamingContent] = useState('');
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Load chat history from storage
    useEffect(() => {
        const loadHistory = async () => {
            const saved = await StorageService.get('autocoder_chat_history');
            if (saved) {
                setMessages(saved.slice(-20)); // Keep last 20 messages
            }
        };
        loadHistory();
    }, []);

    // Save chat history to storage
    useEffect(() => {
        if (messages.length > 0) {
            StorageService.set('autocoder_chat_history', messages.slice(-20));
        }
    }, [messages]);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, streamingContent]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');
        setLoading(true);

        // Add user message
        const newUserMessage = {
            id: Date.now(),
            role: 'user',
            content: userMessage,
            timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, newUserMessage]);

        try {
            // Call backend API
            const response = await apiClient.post(`${API_BASE}/generate`, {
                prompt: userMessage,
                execute: false // Don't execute automatically, show preview first
            });

            const data = response.data;

            // Add assistant response
            const assistantMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                content: data.code || 'No code generated',
                code: data.code,
                execution_result: data.execution_result,
                tokens_used: data.tokens_used,
                timestamp: new Date().toISOString()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Command chat error:', error);
            const errorMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                content: `Error: ${error.message}`,
                error: true,
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleExecute = async (code, messageId) => {
        if (!code) return;

        setLoading(true);

        try {
            const response = await apiClient.post(`${API_BASE}/execute`, {
                code: code
            });

            const data = response.data;

            // Update message with execution result
            setMessages(prev => prev.map(msg => 
                msg.id === messageId
                    ? { ...msg, execution_result: data }
                    : msg
            ));
        } catch (error) {
            console.error('Execution error:', error);
            setMessages(prev => prev.map(msg => 
                msg.id === messageId
                    ? { ...msg, execution_error: error.message }
                    : msg
            ));
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const clearHistory = async () => {
        setMessages([]);
        await StorageService.remove('autocoder_chat_history');
    };

    return (
        <div className="command-chat">
            <div className="command-chat__header">
                <h3 className="command-chat__title">🤖 Autocoder Agent</h3>
                <button 
                    className="command-chat__clear-btn"
                    onClick={clearHistory}
                    title="Clear chat history"
                >
                    Clear
                </button>
            </div>

            <div className="command-chat__messages">
                {messages.length === 0 && (
                    <div className="command-chat__empty">
                        <p>💡 Try commands like:</p>
                        <ul>
                            <li>"Calculate the moving average of AAPL stock prices"</li>
                            <li>"Generate a simple buy/sell signal based on RSI"</li>
                            <li>"Analyze portfolio correlation matrix"</li>
                        </ul>
                    </div>
                )}

                {messages.map((msg) => (
                    <div 
                        key={msg.id} 
                        className={`command-chat__message command-chat__message--${msg.role}`}
                    >
                        <div className="command-chat__message-header">
                            <span className="command-chat__role">
                                {msg.role === 'user' ? '👤 You' : '🤖 Autocoder'}
                            </span>
                            <span className="command-chat__timestamp">
                                {new Date(msg.timestamp).toLocaleTimeString()}
                            </span>
                        </div>

                        <div className="command-chat__content">
                            {msg.role === 'user' ? (
                                <p>{msg.content}</p>
                            ) : (
                                <>
                                    {msg.error ? (
                                        <div className="command-chat__error">
                                            ⚠️ {msg.content}
                                        </div>
                                    ) : (
                                        <>
                                            {msg.code && (
                                                <div className="command-chat__code-block">
                                                    <pre><code>{msg.code}</code></pre>
                                                    {!msg.execution_result && (
                                                        <button
                                                            className="command-chat__execute-btn"
                                                            onClick={() => handleExecute(msg.code, msg.id)}
                                                            disabled={loading}
                                                        >
                                                            ▶ Execute Code
                                                        </button>
                                                    )}
                                                </div>
                                            )}

                                            {msg.execution_result && (
                                                <div className={`command-chat__execution-result ${
                                                    msg.execution_result.success ? 'success' : 'error'
                                                }`}>
                                                    <div className="command-chat__execution-header">
                                                        <span>
                                                            {msg.execution_result.success ? '✅' : '❌'} 
                                                            Execution {msg.execution_result.success ? 'Success' : 'Failed'}
                                                        </span>
                                                        <span className="command-chat__execution-time">
                                                            {msg.execution_result.execution_time_ms}ms
                                                        </span>
                                                    </div>
                                                    {msg.execution_result.output && (
                                                        <pre className="command-chat__output">
                                                            {msg.execution_result.output}
                                                        </pre>
                                                    )}
                                                    {msg.execution_result.error && (
                                                        <pre className="command-chat__error-output">
                                                            {msg.execution_result.error}
                                                        </pre>
                                                    )}
                                                </div>
                                            )}

                                            {msg.tokens_used && (
                                                <div className="command-chat__meta">
                                                    Tokens used: {msg.tokens_used}
                                                </div>
                                            )}
                                        </>
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                ))}

                {streaming && (
                    <div className="command-chat__message command-chat__message--assistant">
                        <div className="command-chat__content">
                            <div className="command-chat__streaming">
                                <span className="command-chat__typing-indicator">●</span>
                                {streamingContent}
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className="command-chat__input-container">
                <textarea
                    ref={inputRef}
                    className="command-chat__input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type a natural language command..."
                    rows={2}
                    disabled={loading}
                />
                <button
                    className="command-chat__send-btn"
                    onClick={handleSend}
                    disabled={!input.trim() || loading}
                >
                    {loading ? '⏳' : '📤'}
                </button>
            </div>
        </div>
    );
};

export default CommandChat;
