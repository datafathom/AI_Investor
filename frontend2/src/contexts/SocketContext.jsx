/**
 * Socket.IO Context Provider
 * 
 * Singleton pattern for Socket.IO connection.
 * Initializes once at app root and provides socket instance to all components.
 * Prevents reconnection on navigation.
 */

import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import { toast } from 'sonner';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '3002';
const SOCKET_SERVER_URL = `http://localhost:${BACKEND_PORT}`;

const SocketContext = createContext(null);

export function SocketProvider({ children }) {
  const socketRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [socketId, setSocketId] = useState(null);
  const [clientCount, setClientCount] = useState(0);
  const [currentRoom, setCurrentRoom] = useState('general');
  const [messages, setMessages] = useState([]);
  const [typingStatus, setTypingStatus] = useState('');

  useEffect(() => {
    // Initialize socket connection once - this should only run once when provider mounts
    if (!socketRef.current) {
      console.log('[SocketContext] Initializing Socket.IO connection...');
      
      socketRef.current = io(SOCKET_SERVER_URL, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: Infinity, // Keep trying to reconnect
        reconnectionDelayMax: 5000,
        timeout: 20000,
      });

      const socket = socketRef.current;

      // Connection events
      socket.on('connect', () => {
        console.log(`[SocketContext] Connected with ID: ${socket.id}`);
        setConnected(true);
        setSocketId(socket.id);
        
        // Join default room on connect
        socket.emit('joinRoom', { room: 'general', password: null }, (response) => {
          if (response?.status === 'ok') {
            setCurrentRoom('general');
          }
        });
      });

      socket.on('disconnect', (reason) => {
        console.log('[SocketContext] Disconnected:', reason);
        setConnected(false);
        setSocketId(null);
        
        if (reason === 'io server disconnect') {
          // Server disconnected, reconnect manually
          socket.connect();
        }
      });

      socket.on('connect_error', (error) => {
        console.error('[SocketContext] Connection error:', error);
        setConnected(false);
      });

      // Socket.io event listeners
      socket.on('clientCount', (count) => {
        setClientCount(count);
      });

      socket.on('chatThread', (message) => {
        setMessages((prev) => [...prev, message]);
      });

      socket.on('userTyping', (msg) => {
        setTypingStatus(msg);
      });

      socket.on('reconnect', (attemptNumber) => {
        console.log(`[SocketContext] Reconnected after ${attemptNumber} attempts`);
        toast.success('Reconnected to Socket.io server');
      });

      socket.on('reconnect_error', (error) => {
        console.error('[SocketContext] Reconnection error:', error);
      });
    }

    // Cleanup on unmount (only if component is truly unmounting)
    return () => {
      // Don't disconnect on navigation - only on app unmount
      // This is handled by React's cleanup, but we want to keep the socket alive
    };
  }, []); // Empty deps - only run once

  // Room management functions
  const joinRoom = (roomId, password = null, callback) => {
    const socket = socketRef.current;
    if (!socket || !socket.connected) {
      toast.error('Socket.io not connected');
      if (callback) callback({ status: 'error', message: 'Not connected' });
      return;
    }

    socket.emit('joinRoom', { room: roomId, password }, (response) => {
      if (response?.status === 'ok') {
        setCurrentRoom(roomId);
        setMessages([]); // Clear messages when switching rooms
        if (callback) callback(response);
      } else {
        if (callback) callback(response);
      }
    });
  };

  const sendMessage = (message, callback) => {
    const socket = socketRef.current;
    if (!socket || !socket.connected) {
      toast.error('Socket.io not connected');
      if (callback) callback({ status: 'error', message: 'Not connected' });
      return;
    }

    socket.emit('chatMessage', { room: currentRoom, message }, (response) => {
      if (callback) callback(response);
    });
  };

  const emitTyping = () => {
    const socket = socketRef.current;
    if (socket && socket.connected) {
      socket.emit('typing', currentRoom);
    }
  };

  const emitStopTyping = () => {
    const socket = socketRef.current;
    if (socket && socket.connected) {
      socket.emit('stopTyping', currentRoom);
    }
  };

  const value = {
    socket: socketRef.current,
    connected,
    socketId,
    clientCount,
    currentRoom,
    messages,
    typingStatus,
    joinRoom,
    sendMessage,
    emitTyping,
    emitStopTyping,
    setMessages, // Allow components to clear messages if needed
  };

  return (
    <SocketContext.Provider value={value}>
      {children}
    </SocketContext.Provider>
  );
}

export function useSocket() {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider');
  }
  return context;
}

