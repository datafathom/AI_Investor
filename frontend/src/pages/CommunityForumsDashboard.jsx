/**
 * ==============================================================================
 * FILE: frontend2/src/pages/CommunityForumsDashboard.jsx
 * ROLE: Community Forums Dashboard
 * PURPOSE: Phase 20 - Community Forums & Discussion
 * 
 * INTEGRATION POINTS:
 *    - CommunityStore: Uses apiClient for all API calls (User Rule 6)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-30
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useCommunityStore from '../stores/communityStore';
import './CommunityForumsDashboard.css';

const CommunityForumsDashboard = () => {
  const userId = 'user_1'; // TODO: Get from authStore
  
  const {
    threads,
    expertQuestions,
    loading,
    fetchThreads,
    fetchExpertQuestions,
    createThread,
    replyToThread,
    upvoteThread
  } = useCommunityStore();

  const [selectedThread, setSelectedThread] = useState(null);
  const [newThread, setNewThread] = useState({ title: '', content: '', category: 'general' });
  const [newReply, setNewReply] = useState('');

  useEffect(() => {
    fetchThreads();
    fetchExpertQuestions(userId);
  }, [fetchThreads, fetchExpertQuestions]);

  const handleCreateThread = async () => {
    if (!newThread.title || !newThread.content) return;
    const success = await createThread({
      user_id: userId,
      title: newThread.title,
      content: newThread.content,
      category: newThread.category
    });
    if (success) {
      setNewThread({ title: '', content: '', category: 'general' });
    }
  };

  const handleAddReply = async (threadId) => {
    if (!newReply) return;
    const success = await replyToThread(threadId, { user_id: userId, content: newReply });
    if (success) {
      setNewReply('');
      fetchThreads();
    }
  };

  const handleUpvote = async (threadId) => {
    await upvoteThread(threadId, userId);
    fetchThreads();
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
            <button onClick={handleCreateThread} disabled={loading} className="create-button">
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
                      onClick={(e) => { e.stopPropagation(); handleUpvote(thread.thread_id); }}
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
                      <span className="reply-date">{new Date(reply.created_date).toLocaleDateString()}</span>
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
                onClick={() => handleAddReply(selectedThread.thread_id)}
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
