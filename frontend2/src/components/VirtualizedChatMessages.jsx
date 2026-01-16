/**
 * VirtualizedChatMessages Component
 * 
 * Uses react-window to virtualize chat messages for better performance
 * with large message lists.
 * 
 * Fallback to simple list if react-window is not available or causes issues.
 */
import React, { useEffect, useRef, useCallback } from 'react';

// Try to import react-window, but handle gracefully if not available
let List, FixedSizeList;
try {
  const reactWindow = require('react-window');
  List = reactWindow.List;
  FixedSizeList = reactWindow.FixedSizeList;
} catch (e) {
  console.warn('[VirtualizedChatMessages] react-window not available, using fallback');
}

export default function VirtualizedChatMessages({ messages, socketId, messagesEndRef, height = 300 }) {
  const listRef = useRef(null);
  const containerRef = useRef(null);

  // Debug logging
  useEffect(() => {
    console.log('[VirtualizedChatMessages] Messages prop updated:', messages.length, messages);
  }, [messages]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    try {
      if (listRef.current && messages.length > 0) {
        // Try different scroll methods depending on react-window version
        if (typeof listRef.current.scrollToItem === 'function') {
          listRef.current.scrollToItem(messages.length - 1, 'end');
        } else if (typeof listRef.current.scrollTo === 'function') {
          listRef.current.scrollTo(messages.length - 1);
        }
      }
      // Also scroll the container if using fallback
      if (containerRef.current && !List) {
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
      }
    } catch (error) {
      console.error('[VirtualizedChatMessages] Scroll error:', error);
    }
  }, [messages.length]);

  // Scroll messagesEndRef into view
  useEffect(() => {
    if (messagesEndRef?.current) {
      try {
        messagesEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
      } catch (error) {
        // Ignore scroll errors
      }
    }
  }, [messages, messagesEndRef]);

  // Row component for react-window
  const MessageRow = useCallback(({ index, style }) => {
    const message = messages[index];
    if (!message) return null;

    const isSystem = message.author === 'System';
    const isSelf = socketId && message.author && socketId.substring && message.author.includes(socketId.substring(0, 4));

    return (
      <div
        style={{
          ...style,
          padding: '0.75rem',
          borderRadius: 'var(--radius-chip)',
          backgroundColor: isSystem 
            ? 'rgba(255, 237, 213, 0.5)' 
            : isSelf 
            ? 'rgba(59, 130, 246, 0.15)' 
            : 'rgba(255, 255, 255, 0.5)',
          borderLeft: `3px solid ${isSystem ? '#f59e0b' : isSelf ? '#3b82f6' : '#6b7280'}`,
          textAlign: isSelf ? 'right' : 'left',
          marginBottom: '0.75rem'
        }}
      >
        <div style={{ fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.25rem', opacity: 0.8 }}>
          {message.author || 'Unknown'} <span style={{ opacity: 0.6 }}>({message.timestamp || ''})</span>
        </div>
        <div style={{ fontSize: '0.875rem' }}>{message.text || ''}</div>
      </div>
    );
  }, [messages, socketId]);

  // Fallback: Simple scrollable list if react-window is not available
  if (!List && !FixedSizeList) {
    return (
      <div 
        ref={containerRef}
        style={{ 
          position: 'relative', 
          height: `${height}px`,
          overflowY: 'auto',
          paddingRight: '0.5rem'
        }}
      >
        {messages.length === 0 ? (
          <p style={{ textAlign: 'center', opacity: 0.6, marginTop: '2rem' }}>
            No messages yet. Start chatting!
          </p>
        ) : (
          <>
            {messages.map((message, index) => {
              const isSystem = message.author === 'System';
              const isSelf = socketId && message.author && socketId.substring && message.author.includes(socketId.substring(0, 4));
              
              return (
                <div
                  key={index}
                  style={{
                    padding: '0.75rem',
                    borderRadius: 'var(--radius-chip)',
                    backgroundColor: isSystem 
                      ? 'rgba(255, 237, 213, 0.5)' 
                      : isSelf 
                      ? 'rgba(59, 130, 246, 0.15)' 
                      : 'rgba(255, 255, 255, 0.5)',
                    borderLeft: `3px solid ${isSystem ? '#f59e0b' : isSelf ? '#3b82f6' : '#6b7280'}`,
                    textAlign: isSelf ? 'right' : 'left',
                    marginBottom: '0.75rem'
                  }}
                >
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.25rem', opacity: 0.8 }}>
                    {message.author || 'Unknown'} <span style={{ opacity: 0.6 }}>({message.timestamp || ''})</span>
                  </div>
                  <div style={{ fontSize: '0.875rem' }}>{message.text || ''}</div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div style={{ position: 'relative', height: `${height}px` }}>
        <p style={{ textAlign: 'center', opacity: 0.6, marginTop: '2rem' }}>
          No messages yet. Start chatting!
        </p>
        <div ref={messagesEndRef} style={{ position: 'absolute', bottom: 0 }} />
      </div>
    );
  }

  // Use FixedSizeList if available (more stable API)
  if (FixedSizeList) {
    return (
      <div style={{ position: 'relative', height: `${height}px` }}>
        <FixedSizeList
          ref={listRef}
          height={height}
          itemCount={messages.length}
          itemSize={80} // Estimated height per message
          width="100%"
          style={{ paddingRight: '0.5rem' }}
        >
          {MessageRow}
        </FixedSizeList>
        <div ref={messagesEndRef} style={{ position: 'absolute', bottom: 0 }} />
      </div>
    );
  }

  // Fallback to List component
  return (
    <div style={{ position: 'relative', height: `${height}px` }}>
      <List
        ref={listRef}
        height={height}
        itemCount={messages.length}
        itemSize={80}
        width="100%"
        style={{ paddingRight: '0.5rem' }}
      >
        {MessageRow}
      </List>
      <div ref={messagesEndRef} style={{ position: 'absolute', bottom: 0 }} />
    </div>
  );
}

