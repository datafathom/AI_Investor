/**
 * Dashboard Page
 * 
 * Main overview page with all original widgets:
 * - Hero section with server/Socket.io status
 * - API Integration
 * - Color System
 * - Launch Checklist
 * - Server Telemetry with animated charts
 * - Experience Controls
 * - Socket.io Realtime Chat
 */

import React, { useEffect, useMemo, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { useColorPalette } from '../hooks/useColorPalette';
import { useSocket } from '../contexts/SocketContext';
import { SkeletonCard } from '../components/Skeleton';
import '../App.css';

const CHECKLIST_STEPS = [
  {
    title: 'Craft the UI System',
    description: 'Replace App.jsx with product UI + routes.',
    command: 'code ./src/App.jsx',
  },
  {
    title: 'Wire Backend APIs',
    description: 'Add new endpoints to server.js + proxy rules.',
    command: 'npm run dev',
  },
  {
    title: 'Enable Realtime',
    description: 'Uncomment the Socket.io block and emit events.',
    command: 'npm install socket.io socket.io-client',
  },
  {
    title: 'Deploy',
    description: 'Build once, ship anywhere. Deploy Node + static bundle.',
    command: 'npm run build',
  },
];

const TERMINAL_SNIPPETS = [
  { label: 'Install dependencies', command: 'npm install' },
  { label: 'Start both servers', command: 'npm run dev' },
  { label: 'Run lint & tests', command: 'npm run lint && npm test' },
];

const INITIAL_MEMORY_POINTS = [62, 65, 64, 70, 66, 72, 68, 73, 69];

const COLOR_TOKENS = [
  { label: 'Burgundy / Primary', path: ['burgundy', 'primary'] },
  { label: 'Burgundy / Accent', path: ['burgundy', 'accent'] },
  { label: 'Burgundy / Dark', path: ['burgundy', 'dark'] },
  { label: 'Cream / Primary', path: ['cream', 'primary'] },
  { label: 'Cream / Medium', path: ['cream', 'medium'] },
  { label: 'Text / On Burgundy', path: ['text', 'on_burgundy'] },
];

const SURFACE_SCALE = [
  { label: 'Surface 50', token: '--surface-50' },
  { label: 'Surface 100', token: '--surface-100' },
  { label: 'Surface 200', token: '--surface-200' },
];

// Room configuration
const ROOM_LIST = [
  { id: 'general', name: '#general', secure: false },
  { id: 'tech', name: '#tech', secure: false },
  { id: 'secure', name: '#secure 🔒', secure: true },
  { id: 'top-secret', name: '#top-secret 🔐', secure: true }
];

const formatJson = (data) => {
  const json = JSON.stringify(data, null, 2)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  return json.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+\.\d+|-?\d+)/g,
    (match) => {
      let cls = 'json-number';
      if (/^"/.test(match)) {
        cls = /:$/.test(match) ? 'json-key' : 'json-string';
      } else if (/true|false/.test(match)) {
        cls = 'json-boolean';
      } else if (/null/.test(match)) {
        cls = 'json-null';
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
};

const MemoryChart = ({ data }) => {
  if (data.length < 2) return null;
  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * 100;
      const normalized = Math.max(0, Math.min(1, (value - 48) / 42));
      const y = 90 - normalized * 70;
      return `${x},${y}`;
    })
    .join(' ');

  const fillPoints = `0,100 ${points} 100,100`;

  return (
    <svg className="telemetry-chart" viewBox="0 0 100 100" preserveAspectRatio="none" role="img" aria-label="Server memory usage line chart">
      <defs>
        <linearGradient id="chartStroke" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="rgba(255,255,255,0.8)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.4)" />
        </linearGradient>
        <linearGradient id="chartFill" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="rgba(255,255,255,0.25)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.02)" />
        </linearGradient>
      </defs>
      <polygon points={fillPoints} fill="url(#chartFill)" />
      <polyline points={points} fill="none" stroke="url(#chartStroke)" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
};

function Dashboard() {
  const { palette } = useColorPalette();
  const [serverStatus, setServerStatus] = useState({ label: 'Checking…', tone: 'loading' });
  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [copiedCommand, setCopiedCommand] = useState(null);
  const [memorySeries, setMemorySeries] = useState(INITIAL_MEMORY_POINTS);
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
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    document.body.classList.toggle('theme-dark', isDarkMode);
    document.body.classList.toggle('theme-light', !isDarkMode);
  }, [isDarkMode]);

  useEffect(() => {
    const interval = setInterval(() => {
      setMemorySeries((prev) => {
        const nextPoint = Math.max(48, Math.min(92, prev[prev.length - 1] + (Math.random() * 8 - 4)));
        return [...prev.slice(1), Number(nextPoint.toFixed(1))];
      });
    }, 3500);

    return () => clearInterval(interval);
  }, []);

  const fetchApiData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/example');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setApiData(data);
      toast.success('API data refreshed');
    } catch (err) {
      setError(err.message);
      toast.error(`API error: ${err.message}`);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkServerHealth = async () => {
    try {
      const response = await fetch('/api/health');
      if (!response.ok) throw new Error('Status not OK');
      const data = await response.json();
      if (data.status === 'ok') {
        setServerStatus({ label: 'Connected', tone: 'ok' });
      } else {
        setServerStatus({ label: 'Degraded', tone: 'warning' });
      }
    } catch (err) {
      setServerStatus({ label: 'Offline', tone: 'error' });
    }
  };

  useEffect(() => {
    const init = async () => {
      await checkServerHealth();
      setInitialLoading(false);
    };
    init();
    const interval = setInterval(checkServerHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [socketMessages]);

  const handleCopy = async (command, id) => {
    if (!navigator?.clipboard) {
      toast.error('Clipboard API unavailable');
      return;
    }
    try {
      await navigator.clipboard.writeText(command);
      setCopiedCommand(id);
      setTimeout(() => setCopiedCommand(null), 1800);
    } catch (err) {
      toast.error('Clipboard unavailable');
    }
  };

  const syntaxMarkup = apiData ? formatJson(apiData) : '';

  const memoryStats = useMemo(() => {
    const current = memorySeries[memorySeries.length - 1];
    const average = memorySeries.reduce((sum, value) => sum + value, 0) / memorySeries.length;
    return { current, average: Number(average.toFixed(1)) };
  }, [memorySeries]);

  const toggleTheme = () => setIsDarkMode((prev) => !prev);
  const triggerModal = () => setShowModal(true);
  const closeModal = () => setShowModal(false);

  // Socket.io handlers (using Context)
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

  if (initialLoading) {
    return (
      <div className="dashboard-grid" style={{ display: 'grid', gap: '1.5rem' }}>
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  return (
    <div 
      className={`app-shell ${isDarkMode ? 'dark' : 'light'}`} 
      style={{ 
        width: '100%', 
        height: '100%',
        minHeight: 0, // Critical for flex child
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <header className="hero">
        <div className="hero-glow" />
        <div className="hero-body" data-animate="fade">
          <p className="eyebrow">Internal Style Guide</p>
          <h1>React + Node Boilerplate</h1>
          <p className="lede">
            Ship MVPs faster with a polished, animated design system. Powered by your Burgundy &amp; Cream palette,
            modern glass surfaces, and motion-ready components.
          </p>
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={fetchApiData}>
              Ping API
            </button>
            <button className="btn btn-ghost" onClick={triggerModal}>
              View Detailed Logs
            </button>
            <div className="theme-toggle" role="group" aria-label="Theme toggle">
              <span>Light</span>
              <label className="switch">
                <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} aria-label="Toggle dark mode" />
                <span className="slider" />
              </label>
              <span>Dark</span>
            </div>
          </div>
        </div>

        <div className="status-card glass" data-animate="slide-up">
          <div className={`status-beacon ${serverStatus.tone}`}>
            <span className="dot" />
            <span className="pulse" />
          </div>
          <div>
            <p className="status-label">Server Status</p>
            <strong>{serverStatus.label}</strong>
          </div>
          <button className="btn-icon" onClick={checkServerHealth} title="Refresh status">
            ⟳
          </button>
        </div>

        <div className="status-card glass" data-animate="slide-up" style={{ marginTop: '1rem' }}>
          <div className={`status-beacon ${socketConnected ? 'ok' : 'error'}`}>
            <span className="dot" />
            <span className="pulse" />
          </div>
          <div>
            <p className="status-label">Socket.io</p>
            <strong>{socketConnected ? 'Connected' : 'Disconnected'}</strong>
            {socketConnected && clientCount > 0 && (
              <span style={{ fontSize: '0.75rem', opacity: 0.7, display: 'block', marginTop: '0.25rem' }}>
                {clientCount} client{clientCount !== 1 ? 's' : ''} online
              </span>
            )}
          </div>
        </div>
      </header>

      <main className="grid">
        <section className="glass card api-card" data-animate="delay-1">
          <header>
            <h2>API Integration</h2>
            <p>Demonstrates proxying API calls through Vite to Express.</p>
          </header>
          <div className="api-actions">
            <button className="btn btn-primary" onClick={fetchApiData} disabled={loading}>
              {loading ? 'Fetching…' : 'Fetch API Data'}
            </button>
            <button className="btn btn-secondary" onClick={() => toast.info('Simulated request sent')}>
              Simulate Request
            </button>
          </div>

          <div className="api-panel">
            {loading && (
              <div className="skeleton-block">
                <div className="skeleton shimmer" />
                <div className="skeleton shimmer" />
                <div className="skeleton shimmer" />
              </div>
            )}

            {!loading && error && (
              <div className="toast-inline error">
                <strong>Request failed:</strong> {error}
              </div>
            )}

            {apiData && (
              <>
                <div className="data-grid">
                  {Object.entries(apiData).map(([key, value]) => (
                    <div key={key} className="data-row">
                      <span>{key}</span>
                      <span>{typeof value === 'object' ? JSON.stringify(value) : value?.toString()}</span>
                    </div>
                  ))}
                </div>
                <pre className="code-block" dangerouslySetInnerHTML={{ __html: syntaxMarkup }} />
              </>
            )}

            {!loading && !apiData && !error && (
              <p className="muted">Run the request to preview live data formatting.</p>
            )}
          </div>
        </section>

        <section className="glass card palette-card" data-animate="delay-2">
          <header>
            <h2>Color System</h2>
            <p>Driven entirely by <code>config/color_palette.json</code>.</p>
          </header>
          <div className="palette-swatches">
            {COLOR_TOKENS.map((token) => {
              const value = token.path.reduce((acc, key) => acc?.[key], palette) || '--';
              return (
                <div key={token.label} className="palette-swatch">
                  <span className="swatch-dot" style={{ backgroundColor: value }} />
                  <div>
                    <p>{token.label}</p>
                    <small>{value}</small>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="surface-stack">
            {SURFACE_SCALE.map((surface) => (
              <div key={surface.label} className="surface-chip" style={{ background: `var(${surface.token})` }}>
                {surface.label}
              </div>
            ))}
          </div>
        </section>

        <section className="glass card checklist-card" data-animate="delay-3">
          <header>
            <h2>Launch Checklist</h2>
            <p>Gamified tasks engineers can check off.</p>
          </header>

          <ol className="stepper">
            {CHECKLIST_STEPS.map((step, idx) => (
              <li key={step.title}>
                <div className="step-icon">{idx + 1}</div>
                <div>
                  <strong>{step.title}</strong>
                  <p>{step.description}</p>
                  <div className="command-chip">
                    <code>{step.command}</code>
                    <button onClick={() => handleCopy(step.command, `step-${idx}`)} aria-label={`Copy ${step.title} command`}>
                      {copiedCommand === `step-${idx}` ? 'Copied!' : '📋'}
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section className="glass card telemetry-card" data-animate="delay-4">
          <header>
            <h2>Server Telemetry</h2>
            <p>Mocked memory usage sparkline.</p>
          </header>
          <div className="telemetry-body">
            <div className="telemetry-stats">
              <div>
                <span>Current</span>
                <strong>{memoryStats.current}%</strong>
              </div>
              <div>
                <span>24h Avg</span>
                <strong>{memoryStats.average}%</strong>
              </div>
            </div>
            <MemoryChart data={memorySeries} />
          </div>
        </section>

        <section className="glass card ux-card" data-animate="delay-5">
          <header>
            <h2>Experience Controls</h2>
            <p>Modal, toast, and copy interactions.</p>
          </header>

          <div className="command-list">
            {TERMINAL_SNIPPETS.map((snippet, idx) => (
              <div key={snippet.label} className="command-row">
                <div>
                  <p>{snippet.label}</p>
                  <code>{snippet.command}</code>
                </div>
                <button onClick={() => handleCopy(snippet.command, `cmd-${idx}`)} className="btn-icon" aria-label={`Copy ${snippet.label}`}>
                  {copiedCommand === `cmd-${idx}` ? '✓' : '📋'}
                </button>
              </div>
            ))}
          </div>
          <div className="ux-actions">
            <button className="btn btn-secondary" onClick={() => toast.info('Toast notification triggered')}>
              Show Toast
            </button>
            <button className="btn btn-primary" onClick={triggerModal}>
              View Logs Modal
            </button>
          </div>
        </section>

        <section className="glass card socketio-card" data-animate="delay-6">
          <header>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
              <div>
                <h2>Socket.io Realtime</h2>
                <p>Secure rooms, chat, and real-time communication.</p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
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
                  <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>
                    {socketConnected ? 'Connected' : 'Disconnected'}
                  </span>
                </div>
                {socketId && (
                  <span style={{ fontSize: '0.75rem', opacity: 0.7 }}>
                    ID: {socketId.substring(0, 8)}...
                  </span>
                )}
              </div>
            </div>
          </header>

          <div className="socketio-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {ROOM_LIST.map((room) => (
                  <motion.button
                    key={room.id}
                    onClick={() => handleJoinRoom(room)}
                    className={`btn ${currentRoom === room.id ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                    disabled={!socketConnected}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {room.name}
                  </motion.button>
                ))}
              </div>
              <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>
                <strong>{clientCount}</strong> client{clientCount !== 1 ? 's' : ''} online
              </div>
            </div>

            <div 
              style={{
                border: '1px solid rgba(0,0,0,0.1)',
                borderRadius: 'var(--radius-chip)',
                padding: '1rem',
                maxHeight: '300px',
                overflowY: 'auto',
                backgroundColor: 'rgba(0,0,0,0.02)',
                marginBottom: '1rem',
                minHeight: '200px'
              }}
            >
              {socketMessages.length === 0 ? (
                <p style={{ textAlign: 'center', opacity: 0.6, marginTop: '2rem' }}>
                  No messages yet. Start chatting!
                </p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
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
                  <div ref={messagesEndRef} />
                </div>
              )}
              
              {typingStatus && (
                <div style={{ 
                  marginTop: '0.5rem', 
                  fontSize: '0.75rem', 
                  fontStyle: 'italic', 
                  opacity: 0.7,
                  animation: 'pulse 1.5s infinite'
                }}>
                  {typingStatus}
                </div>
              )}
            </div>

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
                  border: '1px solid rgba(0,0,0,0.1)',
                  borderRadius: 'var(--radius-chip)',
                  fontSize: '0.875rem',
                  backgroundColor: 'rgba(255,255,255,0.8)'
                }}
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={!socketConnected || !inputMessage.trim()}
                style={{ padding: '0.75rem 1.5rem' }}
              >
                Send
              </button>
            </form>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>Modernized React + Node template · Glass / Motion ready · Dark mode aware</p>
      </footer>

      {showModal && (
        <div className="modal-overlay" role="dialog" aria-modal="true" aria-label="Detailed logs">
          <div className="modal glass">
            <header>
              <h3>Deployment Logs</h3>
              <button onClick={closeModal} className="btn-icon" aria-label="Close modal">
                ×
              </button>
            </header>
            <div className="modal-body">
              <code>
                <span>[04:00:12]</span> ✅ Build complete (3.4s)
                <br />
                <span>[04:00:13]</span> 🚀 Deploying to nodes…
                <br />
                <span>[04:00:18]</span> 💡 Tip: Hook into the CLI to register new micro-apps.
              </code>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={closeModal}>
                Dismiss
              </button>
              <button className="btn btn-primary" onClick={() => toast.success('Logs exported')}>
                Export Logs
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
