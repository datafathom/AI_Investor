/**
 * useSocketBuffer Hook
 * 
 * Buffers high-frequency socket.io updates and flushes them to state at a throttled rate.
 * This prevents React from re-rendering on every socket message, which can freeze the UI.
 * 
 * @param {number} flushInterval - Milliseconds between state updates (default: 100ms = 10fps)
 * @returns {[Array, Function]} - [bufferedData, addToBuffer]
 */
import { useState, useRef, useEffect, useCallback } from 'react';

export function useSocketBuffer(flushInterval = 100) {
  const [state, setState] = useState([]);
  const bufferRef = useRef([]);
  const flushTimerRef = useRef(null);

  // Flush buffer to state
  const flushBuffer = useCallback(() => {
    if (bufferRef.current.length > 0) {
      setState((prev) => {
        // Merge buffered items with existing state
        // For chat messages, we append; for other data types, you might want to replace
        return [...prev, ...bufferRef.current];
      });
      bufferRef.current = [];
    }
  }, []);

  // Add data to buffer (doesn't trigger render)
  const addToBuffer = useCallback((item) => {
    bufferRef.current.push(item);
    
    // For chat messages, flush immediately to ensure real-time feel
    // For other high-frequency data, use throttled flushing
    const isChatMessage = item && (item.author !== undefined || item.text !== undefined);
    
    if (isChatMessage) {
      // Immediate flush for chat messages
      flushBuffer();
    } else {
      // Schedule flush if not already scheduled (for non-chat data)
      if (!flushTimerRef.current) {
        flushTimerRef.current = setTimeout(() => {
          flushBuffer();
          flushTimerRef.current = null;
        }, flushInterval);
      }
    }
  }, [flushInterval, flushBuffer]);

  // Immediate flush function (for critical updates)
  const flushImmediate = useCallback(() => {
    if (flushTimerRef.current) {
      clearTimeout(flushTimerRef.current);
      flushTimerRef.current = null;
    }
    flushBuffer();
  }, [flushBuffer]);

  // Clear buffer and state
  const clearBuffer = useCallback(() => {
    // Clear both the buffer and any pending flush timer
    bufferRef.current = [];
    setState([]);
    if (flushTimerRef.current) {
      clearTimeout(flushTimerRef.current);
      flushTimerRef.current = null;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (flushTimerRef.current) {
        clearTimeout(flushTimerRef.current);
      }
    };
  }, []);

  return [state, addToBuffer, flushImmediate, clearBuffer];
}

