/**
 * Chat Page
 * 
 * Socket.io real-time chat interface with secure rooms.
 * Uses SocketContext for persistent connection (no reconnection on navigation).
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { useColorPalette } from '../hooks/useColorPalette';
import { useSocket } from '../contexts/SocketContext';
import '../App.css';

const ROOM_LIST = [
  { id: 'general', name: '#general', secure: false },
  { id: 'tech', name: '#tech', secure: false },
  { id: 'secure', name: '#secure ', secure: true },
  { id: 'top-secret', name: '#top-secret ', secure: true }
];

function Chat() {
  const { palette } = useColorPalette();
  const [inputMessage, setInputMessage] = useState('');
  
  // Use Socket Context (singleton pattern - no reconnection on navigation)
  const {
    connected: socketConnected,
    socketId,
    clientCount,
    currentRoom,
    messages: socketMessages,
    typingStatus,
    joinRoom,
    sendMessage,
    emitTyping,
    emitStopTyping,
  } = useSocket();
  
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [socketMessages]);

  const handleJoinRoom = (targetRoomObj) => {
    const targetRoom = targetRoomObj.id;
    if (targetRoom === currentRoom) return;
    
    let password = null;
    if (targetRoomObj.secure) {
      password = prompt(`Enter password for ${targetRoomObj.name}:`);
      if (password === null) return;
    }
    
    joinRoom(targetRoom, password, (response) => {
      if (response?.status === 'ok') {
        toast.success(`Joined ${targetRoomObj.name}`);
      } else {
        toast.error(response?.message || 'Failed to join room');
      }
    });
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
    emitTyping();
    if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
    typingTimeoutRef.current = setTimeout(() => {
      emitStopTyping();
    }, 1000);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      sendMessage(inputMessage.trim(), (response) => {
        if (response?.status !== 'ok') {
          toast.error(response?.message || 'Failed to send message');
        }
      });
      setInputMessage('');
      emitStopTyping();
    }
  };

  return (
    <div 
      className="chat-container" 
      style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        width: '100%',
        height: '100%',
        minHeight: 0, // Critical for flex child
      }}
    >
      {/* Connection Status */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '1rem', 
        marginBottom: '1rem',
        padding: '1rem',
        backgroundColor: palette?.backgrounds?.card || '#fefae8',
        borderRadius: 'var(--radius-card)',
        border: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div 
            style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor: socketConnected ? '#10b981' : '#ef4444',
              boxShadow: socketConnected ? '0 0 8px rgba(16, 185, 129, 0.6)' : 'none',
              animation: socketConnected ? 'pulse 2s infinite' : 'none'
            }}
          />
          <span style={{ fontWeight: 600 }}>
            {socketConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        {socketId && <span style={{ fontSize: '0.875rem', opacity: 0.7 }}>ID: {socketId.substring(0, 8)}...</span>}
        <span style={{ marginLeft: 'auto', fontSize: '0.875rem' }}>
          <strong>{clientCount}</strong> client{clientCount !== 1 ? 's' : ''} online
        </span>
      </div>

      {/* Room Switcher */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
        {ROOM_LIST.map((room) => (
          <motion.button
            key={room.id}
            onClick={() => handleJoinRoom(room)}
            className={`btn ${currentRoom === room.id ? 'btn-primary' : 'btn-secondary'}`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!socketConnected}
          >
            {room.name}
          </motion.button>
        ))}
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '1rem',
        backgroundColor: palette?.backgrounds?.main || '#fffef0',
        borderRadius: 'var(--radius-card)',
        border: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
        marginBottom: '1rem',
      }}>
        <AnimatePresence>
          {socketMessages.map((message, index) => {
            const isSystem = message.author === 'System';
            const isSelf = socketId && message.author.includes(socketId.substring(0, 4));
            
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
                style={{
                  padding: '0.75rem',
                  marginBottom: '0.5rem',
                  borderRadius: 'var(--radius-chip)',
                  backgroundColor: isSystem 
                    ? 'rgba(255, 237, 213, 0.5)' 
                    : isSelf 
                    ? 'rgba(59, 130, 246, 0.15)' 
                    : 'rgba(255, 255, 255, 0.5)',
                  borderLeft: `3px solid ${isSystem ? '#f59e0b' : isSelf ? '#3b82f6' : '#6b7280'}`,
                  textAlign: isSelf ? 'right' : 'left'
                }}
              >
                <div style={{ fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.25rem', opacity: 0.8 }}>
                  {message.author} <span style={{ opacity: 0.6 }}>({message.timestamp})</span>
                </div>
                <div style={{ fontSize: '0.875rem' }}>{message.text}</div>
              </motion.div>
            );
          })}
        </AnimatePresence>
        {typingStatus && (
          <div style={{ fontSize: '0.75rem', fontStyle: 'italic', opacity: 0.7, marginTop: '0.5rem' }}>
            {typingStatus}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '0.5rem' }}>
        <input
          type="text"
          value={inputMessage}
          onChange={handleInputChange}
          placeholder={`Message #${currentRoom}...`}
          disabled={!socketConnected}
          style={{
            flex: 1,
            padding: '0.75rem',
            border: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
            borderRadius: 'var(--radius-chip)',
            fontSize: '0.875rem',
            backgroundColor: palette?.backgrounds?.card || '#fefae8',
          }}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={!socketConnected || !inputMessage.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default Chat;

