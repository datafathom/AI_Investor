import React, { useState, useEffect } from 'react';
import autocoderService from '../services/autocoderService';
import './AutoCoderDashboard.css';
import { Bot, Code2, Play, Rocket, ShieldCheck, Terminal, Save, X, Eye, FileCode } from 'lucide-react';
import FileTree from '../components/AutoCoder/FileTree';
import CodeDiffViewer from '../components/AutoCoder/CodeDiffViewer';
import TaskQueue from '../components/AutoCoder/TaskQueue';
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const AutoCoderDashboard = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'filetree', x: 0, y: 0, w: 2, h: 12 },
            { i: 'editor', x: 2, y: 0, w: 7, h: 12 },
            { i: 'sidebar', x: 9, y: 0, w: 3, h: 12 }
        ]
    };
    const STORAGE_KEY = 'layout_autocoder';

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const [task, setTask] = useState('Create a data normalizer for 10-year yield data.');
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [viewMode, setViewMode] = useState('code'); // 'code' or 'diff'
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const init = async () => {
            addLog('System', 'Environment initialized. Connecting to AI Engine...', 'info');
            try {
                const status = await autocoderService.getStatus();
                addLog('System', `AI Engine status: ${status.status}. Registry count: ${status.registry_count}`, 'success');
            } catch (err) {
                addLog('System', 'AI Engine offline or unreachable.', 'error');
            }
        };
        init();
    }, []);

    const addLog = (tag, message, type = 'info') => {
        setLogs(prev => [{ tag, message, type, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 50));
    };

    const generateCode = async () => {
        if (!task.trim()) return;
        setLoading(true);
        addLog('AI', `Processing instructions: ${task}...`);
        try {
            const generatedCode = await autocoderService.generateCode(task);
            setCode(generatedCode);
            addLog('AI', 'Code generation complete. Syntactically verified.', 'success');
        } catch (error) {
            addLog('AI', `Generation failed: ${error.message}`, 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="autocoder-container">
            <header className="autocoder-header">
                <div className="flex items-center gap-3">
                    <Bot className="text-cyan-400" size={24} />
                    <div>
                        <h1 className="text-xl font-bold font-display text-white">Auto-Coder Link</h1>
                        <span className="text-[10px] font-mono text-cyan-500 uppercase tracking-widest">Phase 39: Self-Improving Logic</span>
                    </div>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono">
                    <span className="flex items-center gap-2"><span className="status-dot healthy"></span> SANDBOX ACTIVE</span>
                    <span className="text-slate-500">|</span>
                    <span>HEAD: main</span>
                </div>
            </header>

            <ResponsiveGridLayout
                className="layout"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={60}
                isDraggable={true}
                isResizable={true}
                draggableHandle=".glass-panel-header"
                margin={[10, 10]}
            >

                {/* LEFT: File Tree */}
                <div key="filetree" className="glass-panel">
                    <div className="glass-panel-header">
                        <FileCode size={14} />
                        <span>File Explorer</span>
                    </div>
                    <div className="p-2 overflow-auto h-[calc(100%-40px)]">
                        <FileTree />
                    </div>
                </div>

                {/* CENTER: Editor & Actions */}
                <div key="editor" className="glass-panel">
                    <div className="glass-panel-header">
                        <Terminal size={14} />
                        <span>Editor Workspace</span>
                    </div>
                    
                    <div className="p-4 border-b border-white/5 bg-white/5 flex gap-2">
                        <div className="flex-1 relative">
                            <input
                                type="text"
                                value={task}
                                onChange={(e) => setTask(e.target.value)}
                                className="w-full bg-black/40 border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500/50"
                                placeholder="Describe the feature or fix..."
                            />
                        </div>
                        <button
                            onClick={generateCode}
                            disabled={loading}
                            className={`px-4 py-2 rounded font-bold text-xs flex items-center gap-2 transition-all ${loading ? 'bg-white/10 text-slate-500 cursor-not-allowed' : 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/30'}`}
                        >
                            {loading ? 'Thinking...' : <><Code2 size={14} /> GENERATE</>}
                        </button>
                    </div>

                    {/* Toolbar */}
                    <div className="flex items-center justify-between px-4 py-2 border-b border-white/5 bg-white/5">
                        <div className="flex gap-2">
                            <button
                                onClick={() => setViewMode('code')}
                                className={`px-3 py-1 rounded text-xs font-medium flex items-center gap-2 transition-all ${viewMode === 'code' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'}`}
                            >
                                <Code2 size={14} /> Code
                            </button>
                            <button
                                onClick={() => setViewMode('diff')}
                                className={`px-3 py-1 rounded text-xs font-medium flex items-center gap-2 transition-all ${viewMode === 'diff' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' : 'text-slate-400 hover:text-white'}`}
                            >
                                <Eye size={14} /> Diff Review
                            </button>
                        </div>
                        <div className="flex gap-3">
                            <button className="text-slate-400 hover:text-cyan-400 transition-colors"><ShieldCheck size={14} /></button>
                            <button className="text-slate-400 hover:text-green-400 transition-colors"><Play size={14} /></button>
                            <button className="text-slate-400 hover:text-purple-400 transition-colors"><Rocket size={14} /></button>
                        </div>
                    </div>

                    {/* Editor Content */}
                    <div className="flex-1 overflow-hidden relative h-[calc(100%-140px)]">
                        {viewMode === 'diff' ? (
                            <CodeDiffViewer />
                        ) : (
                            <textarea
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                className="w-full h-full bg-black/20 text-slate-300 font-mono text-xs p-4 resize-none focus:outline-none scroll-buffer"
                                placeholder="// Generated code will appear here..."
                                spellCheck="false"
                            />
                        )}
                    </div>
                </div>

                {/* RIGHT: Tasks & Logs */}
                <div key="sidebar" className="glass-panel">
                    <div className="h-1/2 border-b border-white/5 flex flex-col overflow-hidden">
                        <div className="glass-panel-header">
                            <Rocket size={14} />
                            <span>Task Queue</span>
                        </div>
                        <div className="flex-1 overflow-auto p-2">
                            <TaskQueue />
                        </div>
                    </div>

                    <div className="h-1/2 flex flex-col overflow-hidden">
                        <div className="glass-panel-header">
                            <Terminal size={14} />
                            <span>System Logs</span>
                        </div>
                        <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-[10px] scroll-buffer">
                            {logs.map((log, idx) => (
                                <div key={idx} className={`flex gap-2 p-1 rounded ${log.type === 'error' ? 'bg-red-500/10 text-red-400' : log.type === 'success' ? 'bg-green-500/10 text-green-400' : 'bg-white/5 text-slate-400'}`}>
                                    <span className="opacity-50">[{log.time}]</span>
                                    <span className="font-bold text-slate-300">[{log.tag}]</span>
                                    <span>{log.message}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default AutoCoderDashboard;
