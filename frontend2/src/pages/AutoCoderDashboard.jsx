/**
 * AutoCoderDashboard.jsx
 * 
 * A developer tool for generating, testing, and deploying AI adapters.
 */

import React, { useState, useEffect } from 'react';
import autocoderService from '../services/autocoderService';
import './AutoCoderDashboard.css';
import { Bot, Code2, Play, Rocket, ShieldCheck, Terminal, Save, X } from 'lucide-react';

const AutoCoderDashboard = () => {
    const [task, setTask] = useState('Create a data normalizer for 10-year yield data.');
    const [code, setCode] = useState('');
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        try {
            const data = await autocoderService.getStatus();
            setStatus(data);
        } catch (error) {
            addLog('System', 'Failed to fetch status.', 'error');
        }
    };

    const addLog = (tag, message, type = 'info') => {
        setLogs(prev => [{ tag, message, type, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 50));
    };

    const generateCode = async () => {
        setLoading(true);
        addLog('AI', `Generating code for: ${task}...`);
        try {
            const data = await autocoderService.generateCode(task);
            setCode(data.code);
            addLog('AI', 'Code generation complete.', 'success');
        } catch (error) {
            addLog('AI', 'Generation failed.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const validateCode = async () => {
        addLog('Sandbox', 'Running safety validation...');
        try {
            const data = await autocoderService.validateCode(code);
            if (data.is_valid) {
                addLog('Sandbox', 'Validation Passed: No forbidden keywords detected.', 'success');
            } else {
                addLog('Sandbox', 'Validation Failed: Security violation.', 'error');
            }
        } catch (error) {
            addLog('Sandbox', 'Process crashed.', 'error');
        }
    };

    const deployModule = async () => {
        const name = prompt('Enter module name:', 'new_adapter');
        if (!name) return;

        addLog('Deploy', `Hot-swapping '${name}' into runtime...`);
        try {
            const data = await autocoderService.deployModule(name, code);
            addLog('Deploy', data.message, 'success');
            fetchStatus();
        } catch (error) {
            addLog('Deploy', 'Deployment failed.', 'error');
        }
    };

    return (
        <div className="autocoder-container glass">
            <header className="autocoder-header">
                <div className="header-title">
                    <Bot className="icon-main" />
                    <h1>Auto-Coder</h1>
                    <span className="badge">Phase 39: Self-Improving Logic</span>
                </div>
                <div className="system-status">
                    <span className="status-dot healthy"></span>
                    <span>Sandbox: Virtualized</span>
                    <span className="separator">|</span>
                    <span>Active Modules: {status?.registry_count || 0}</span>
                </div>
            </header>

            <main className="autocoder-content">
                <div className="editor-section">
                    <div className="prompt-bar">
                        <textarea
                            value={task}
                            onChange={(e) => setTask(e.target.value)}
                            placeholder="Describe the adapter you want to build..."
                            className="prompt-input"
                        />
                        <button
                            onClick={generateCode}
                            disabled={loading}
                            className="btn-primary"
                        >
                            {loading ? 'Thinking...' : <><Code2 size={16} /> Generate Adapter</>}
                        </button>
                    </div>

                    <div className="code-editor glass">
                        <div className="editor-header">
                            <span>Python Sandbox</span>
                            <div className="editor-actions">
                                <button onClick={validateCode} className="btn-ghost" title="Run Security Scan">
                                    <ShieldCheck size={16} /> Validate
                                </button>
                                <button onClick={deployModule} className="btn-ghost highlight" title="Hot Swap Module">
                                    <Rocket size={16} /> Deploy
                                </button>
                            </div>
                        </div>
                        <textarea
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                            className="code-textarea"
                            spellCheck="false"
                        />
                    </div>
                </div>

                <div className="side-panel">
                    <div className="log-window card glass">
                        <div className="panel-header">
                            <Terminal size={14} />
                            <h3>Terminal Logs</h3>
                        </div>
                        <div className="logs-list">
                            {logs.length === 0 ? (
                                <p className="empty-logs">Awaiting instructions...</p>
                            ) : (
                                logs.map((log, idx) => (
                                    <div key={idx} className={`log-entry ${log.type}`}>
                                        <span className="log-time">[{log.time}]</span>
                                        <span className="log-tag">[{log.tag}]</span>
                                        <span className="log-message">{log.message}</span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    <div className="registry-window card glass">
                        <div className="panel-header">
                            <Save size={14} />
                            <h3>Module Registry</h3>
                        </div>
                        <div className="registry-list">
                            {status?.modules?.map((m, idx) => (
                                <div key={idx} className="registry-item">
                                    <span>{m}.py</span>
                                    <span className="badge-small">HOT</span>
                                </div>
                            ))}
                            {(!status?.modules || status.modules.length === 0) && (
                                <p className="empty-registry">No custom modules loaded.</p>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AutoCoderDashboard;
