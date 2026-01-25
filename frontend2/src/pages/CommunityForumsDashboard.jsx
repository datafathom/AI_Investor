/**
 * ==============================================================================
 * FILE: frontend2/src/pages/CommunityForumsDashboard.jsx
 * ROLE: Community Forums Dashboard
 * PURPOSE: Phase 20 - Community Forums & Discussion
 *          Displays forum threads, replies, and expert Q&A.
 * 
 * INTEGRATION POINTS:
 *    - CommunityAPI: /api/v1/community endpoints
 * 
 * FEATURES:
 *    - Forum thread management
 *    - Replies and upvoting
 *    - Expert Q&A
 *    - Moderation
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CommunityForumsDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const CommunityForumsDashboard = () => {
  const [threads, setThreads] = useState([]);
  const [selectedThread, setSelectedThread] = useState(null);
  const [expertQuestions, setExpertQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newThread, setNewThread] = useState({ title: '', content: '', category: 'general' });
  const [newReply, setNewReply] = useState('');

  useEffect(() => {
    loadThreads();
    loadExpertQuestions();
  }, []);

  const loadThreads = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/community/threads`, {
        params: { limit: 20 }
      });
      setThreads(res.data.data || []);
    } catch (error) {
      console.error('Error loading threads:', error);
    }
  };

  const loadExpertQuestions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/community/expert/questions`, {
        params: { user_id: userId }
      });
      setExpertQuestions(res.data.data || []);
    } catch (error) {
      console.error('Error loading expert questions:', error);
    }
  };

  const createThread = async () => {
    if (!newThread.title || !newThread.content) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/community/thread/create`, {
        user_id: userId,
        title: newThread.title,
        content: newThread.content,
        category: newThread.category
      });
      setNewThread({ title: '', content: '', category: 'general' });
      loadThreads();
    } catch (error) {
      console.error('Error creating thread:', error);
    } finally {
      setLoading(false);
    }
  };

  const addReply = async (threadId) => {
    if (!newReply) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/community/thread/${threadId}/reply`, {
        user_id: userId,
        content: newReply
      });
      setNewReply('');
      if (selectedThread?.thread_id === threadId) {
        loadThreads();
      }
    } catch (error) {
      console.error('Error adding reply:', error);
    } finally {
      setLoading(false);
    }
  };

  const upvoteThread = async (threadId) => {
    try {
      await axios.post(`${API_BASE}/api/v1/community/thread/${threadId}/upvote`, {
        user_id: userId
      });
      loadThreads();
    } catch (error) {
      console.error('Error upvoting thread:', error);
    }
  };

  return (
    <div className="community-forums-dashboard">
      <div className="dashboard-header">
        <h1>Community Forums</h1>
        <p className="subtitle">Phase 20: Community Forums & Discussion</p>
      </div>

      <div className="dashboard-content">
        {/* Create Thread */}
        <div className="create-thread-panel">
          <h2>Create New Thread</h2>
          <div className="thread-form">
            <input
              type="text"
              placeholder="Thread Title"
              value={newThread.title}
              onChange={(e) => setNewThread({ ...newThread, title: e.target.value })}
              className="form-input"
            />
            <select
              value={newThread.category}
              onChange={(e) => setNewThread({ ...newThread, category: e.target.value })}
              className="form-input"
            >
              <option value="general">General</option>
              <option value="trading">Trading</option>
              <option value="investing">Investing</option>
              <option value="education">Education</option>
            </select>
            <textarea
              placeholder="Thread Content"
              value={newThread.content}
              onChange={(e) => setNewThread({ ...newThread, content: e.target.value })}
              className="form-textarea"
              rows="4"
            />
            <button onClick={createThread} disabled={loading} className="create-button">
              Create Thread
            </button>
          </div>
        </div>

        {/* Threads List */}
        <div className="threads-panel">
          <h2>Recent Threads</h2>
          {threads.length > 0 ? (
            <div className="threads-list">
              {threads.map((thread) => (
                <div
                  key={thread.thread_id}
                  className={`thread-card ${selectedThread?.thread_id === thread.thread_id ? 'selected' : ''}`}
                  onClick={() => setSelectedThread(thread)}
                >
                  <div className="thread-header">
                    <h3>{thread.title}</h3>
                    <span className="category">{thread.category}</span>
                  </div>
                  <p className="thread-preview">{thread.content?.substring(0, 150)}...</p>
                  <div className="thread-meta">
                    <span>By: {thread.author_name || 'Anonymous'}</span>
                    <span>{thread.reply_count || 0} replies</span>
                    <span>{thread.upvotes || 0} upvotes</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        upvoteThread(thread.thread_id);
                      }}
                      className="upvote-button"
                    >
                      ↑
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No threads yet</div>
          )}
        </div>

        {/* Thread Details */}
        {selectedThread && (
          <div className="thread-details-panel">
            <h2>{selectedThread.title}</h2>
            <div className="thread-content">
              <p>{selectedThread.content}</p>
            </div>
            {selectedThread.replies && selectedThread.replies.length > 0 && (
              <div className="replies-section">
                <h3>Replies ({selectedThread.replies.length})</h3>
                {selectedThread.replies.map((reply, idx) => (
                  <div key={idx} className="reply-card">
                    <div className="reply-header">
                      <span className="reply-author">{reply.author_name || 'Anonymous'}</span>
                      <span className="reply-date">
                        {new Date(reply.created_date).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="reply-content">{reply.content}</p>
                  </div>
                ))}
              </div>
            )}
            <div className="reply-form">
              <textarea
                placeholder="Write a reply..."
                value={newReply}
                onChange={(e) => setNewReply(e.target.value)}
                className="form-textarea"
                rows="3"
              />
              <button
                onClick={() => addReply(selectedThread.thread_id)}
                disabled={loading || !newReply}
                className="reply-button"
              >
                Post Reply
              </button>
            </div>
          </div>
        )}

        {/* Expert Q&A */}
        <div className="expert-qa-panel">
          <h2>Expert Q&A</h2>
          {expertQuestions.length > 0 ? (
            <div className="questions-list">
              {expertQuestions.map((question) => (
                <div key={question.question_id} className="question-card">
                  <h3>{question.question}</h3>
                  {question.answer && (
                    <div className="answer-section">
                      <div className="answer-header">
                        <span className="expert-badge">Expert Answer</span>
                      </div>
                      <p className="answer-content">{question.answer}</p>
                    </div>
                  )}
                  {!question.answer && (
                    <div className="pending-answer">Awaiting expert response...</div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No expert questions</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CommunityForumsDashboard;
