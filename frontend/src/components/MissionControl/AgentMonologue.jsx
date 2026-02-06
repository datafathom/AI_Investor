import React, { useState, useEffect, useRef } from 'react';
import { useSocket } from '../../contexts/SocketContext';
import { Terminal, Brain, Cpu, AlertTriangle, Activity } from 'lucide-react';
import './AgentMonologue.css';

const AgentMonologue = ({ agentId = 'SovereignMaster' }) => {
  const { socket, connected } = useSocket();
  const [traces, setTraces] = useState([]);
  const [agentState, setAgentState] = useState('INIT');
  const viewportRef = useRef(null);
  const [autoScroll, setAutoScroll] = useState(true);

  useEffect(() => {
    if (!socket) return;

    const eventName = `TRACE_${agentId}`;
    
    // Subscribe to agent-specific trace channel
    socket.emit('subscribe', { channel: agentId });

    const handleTrace = (payload) => {
      setTraces((prev) => [...prev.slice(-100), payload]); // Keep last 100 traces
      if (payload.state) setAgentState(payload.state);
    };

    socket.on(eventName, handleTrace);

    return () => {
      socket.off(eventName, handleTrace);
      socket.emit('unsubscribe', { channel: agentId });
    };
  }, [socket, agentId]);

  useEffect(() => {
    if (autoScroll && viewportRef.current) {
      viewportRef.current.scrollTop = viewportRef.current.scrollHeight;
    }
  }, [traces, autoScroll]);

  const getIcon = (type) => {
    switch (type) {
      case 'thought': return <Brain size={14} />;
      case 'tool_call': return <Cpu size={14} />;
      case 'error': return <AlertTriangle size={14} />;
      case 'state_transition': return <Activity size={14} />;
      default: return <Terminal size={14} />;
    }
  };

  return (
    <div className="agent-monologue">
      <div className="monologue-header">
        <div className="monologue-title">
          Inner Monologue: {agentId}
        </div>
        <div className="monologue-status">
          <span className="status-label">{agentState}</span>
          <div className={`status-dot ${connected ? 'online' : 'offline'}`} />
        </div>
      </div>

      <div 
        className="monologue-viewport" 
        ref={viewportRef}
        onScroll={(e) => {
          const { scrollTop, scrollHeight, clientHeight } = e.target;
          const isAtBottom = scrollHeight - scrollTop <= clientHeight + 50;
          setAutoScroll(isAtBottom);
        }}
      >
        {traces.length === 0 && (
          <div className="empty-state">Awaiting agent neural activity...</div>
        )}
        
        {traces.map((trace, index) => (
          <div key={index} className={`trace-entry trace-type-${trace.type || 'info'}`}>
            <div className="trace-meta">
              <span className="trace-time">{trace.timestamp}</span>
              <span className="trace-icon">{getIcon(trace.type)}</span>
              <span className="trace-label">{trace.label}</span>
              {trace.step_id && <span className="trace-step">STEP:{trace.step_id}</span>}
            </div>
            <div className="trace-content">
              {typeof trace.content === 'string' 
                ? trace.content 
                : JSON.stringify(trace.content, null, 2)}
            </div>
          </div>
        ))}
      </div>

      <div className="monologue-footer">
        <span>Latency: 24ms</span>
        <span>Auto-scroll: {autoScroll ? 'ON' : 'OFF'}</span>
      </div>
    </div>
  );
};

export default AgentMonologue;
