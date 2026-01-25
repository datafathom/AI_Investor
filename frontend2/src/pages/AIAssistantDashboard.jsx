/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AIAssistantDashboard.jsx
 * ROLE: AI Assistant Dashboard
 * PURPOSE: Phase 26 - Personalized AI Assistant
 *          Conversational AI assistant with personalized investment advice.
 * 
 * INTEGRATION POINTS:
 *    - AIAssistantAPI: /api/ai-assistant endpoints
 * 
 * FEATURES:
 *    - Chat interface
 *    - Conversation history
 *    - Personalized recommendations
 *    - Context-aware responses
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './AIAssistantDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AIAssistantDashboard = () => {
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    createConversation();
    loadRecommendations();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const createConversation = async () => {
    try {
      const res = await axios.post(`${API_BASE}/api/ai-assistant/conversation/create`, {
        user_id: userId,
        title: 'Investment Assistant Chat'
      });
      setConversation(res.data.data);
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const loadRecommendations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/ai-assistant/recommendations/${userId}`);
      setRecommendations(res.data.data || []);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !conversation) return;
    
    const userMsg = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };
    
    setMessages([...messages, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await axios.post(
        `${API_BASE}/api/ai-assistant/conversation/${conversation.conversation_id}/message`,
        { message: inputMessage }
      );
      
      const assistantMsg = {
        role: 'assistant',
        content: res.data.data.content,
        timestamp: res.data.data.timestamp
      };
      
      setMessages([...messages, userMsg, assistantMsg]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMsg = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages([...messages, userMsg, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="ai-assistant-dashboard">
      <div className="dashboard-header">
        <h1>AI Investment Assistant</h1>
        <p className="subtitle">Phase 26: Personalized AI Assistant</p>
      </div>

      <div className="assistant-layout">
        {/* Chat Panel */}
        <div className="chat-panel">
          <div className="chat-header">
            <h2>Chat</h2>
            <div className="chat-status">Online</div>
          </div>

          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h3>Welcome to your AI Investment Assistant!</h3>
                <p>Ask me anything about investing, portfolio management, or financial planning.</p>
                <div className="example-questions">
                  <p>Try asking:</p>
                  <ul>
                    <li>"What should I invest in for retirement?"</li>
                    <li>"How can I diversify my portfolio?"</li>
                    <li>"Explain tax-loss harvesting"</li>
                  </ul>
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <div className="message-content">
                    {msg.content}
                  </div>
                  <div className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about investing..."
              className="chat-input"
              disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading || !inputMessage.trim()} className="send-button">
              Send
            </button>
          </div>
        </div>

        {/* Recommendations Panel */}
        <div className="recommendations-panel">
          <h2>Personalized Recommendations</h2>
          {recommendations.length > 0 ? (
            <div className="recommendations-list">
              {recommendations.map((rec) => (
                <div key={rec.recommendation_id} className="recommendation-card">
                  <div className="recommendation-header">
                    <h3>{rec.title}</h3>
                    <div className="confidence-badge">
                      {(rec.confidence * 100).toFixed(0)}% confidence
                    </div>
                  </div>
                  <p className="recommendation-description">{rec.description}</p>
                  <div className="recommendation-reasoning">
                    <strong>Reasoning:</strong> {rec.reasoning}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-recommendations">
              <p>No recommendations available yet.</p>
              <p>Start chatting to get personalized investment advice!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIAssistantDashboard;
