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
        addLog('System', 'Environment initialized. Ready for instructions.', 'info');
    }, []);

    const addLog = (tag, message, type = 'info') => {
        setLogs(prev => [{ tag, message, type, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 50));
    };

    const generateCode = async () => {
        setLoading(true);
        addLog('AI', `Generating code for: ${task}...`);
        try {
            // Mock generation for demo
            setTimeout(() => {
                setCode(`# Generated Adapter\nimport pandas as pd\n\ndef normalize_data(df):\n    return (df - df.mean()) / df.std()`);
                addLog('AI', 'Code generation complete.', 'success');
                setLoading(false);
            }, 1500);
        } catch (error) {
            addLog('AI', 'Generation failed.', 'error');
            setLoading(false);
        }
    };

    return (
        <div className="full-bleed-page autocoder-container h-screen flex flex-col bg-slate-950 text-slate-300">
            <header className="autocoder-header border-b border-slate-800 bg-slate-900/50 p-4 flex justify-between items-center backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <Bot className="text-cyan-400" size={24} />
                    <div>
                        <h1 className="text-xl font-bold font-display text-white">Auto-Coder Link</h1>
                        <span className="text-[10px] font-mono text-cyan-500 uppercase tracking-widest">Phase 39: Self-Improving Logic</span>
                    </div>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500"></span> SANDBOX ACTIVE</span>
                    <span className="text-slate-500">|</span>
                    <span>HEAD: main</span>
                </div>
            </header>

            <ResponsiveGridLayout
                className="layout h-full overflow-hidden"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={60} // Smaller row height for fine-grained IDE control
                isDraggable={true}
                isResizable={true}
                draggableHandle=".draggable-handle"
                margin={[2, 2]} // Minimal margin for IDE feel
            >

                {/* LEFT: File Tree */}
                <div key="filetree" className="border-r border-slate-800 bg-slate-900/30 flex flex-col h-full">
                    <div className="draggable-handle p-2 bg-slate-900/50 cursor-move border-b border-slate-800 text-[10px] uppercase font-bold text-slate-500">
                        File Explorer
                    </div>
                    <div className="flex-1 overflow-auto">
                        <FileTree />
                    </div>
                </div>

                {/* CENTER: Editor & Actions */}
                <div key="editor" className="flex flex-col border-r border-slate-800 bg-[#0a0a0a] h-full">
                    {/* Prompt Bar */}
                    <div className="draggable-handle p-2 bg-slate-900/50 cursor-move border-b border-slate-800 flex justify-between items-center">
                        <span className="text-[10px] uppercase font-bold text-slate-500">Editor Workspace</span>
                    </div>
                    
                    <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex gap-2">
                        <div className="flex-1 relative">
                            <input
                                type="text"
                                value={task}
                                onChange={(e) => setTask(e.target.value)}
                                className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
                                placeholder="Describe the feature or fix..."
                            />
                        </div>
                        <button
                            onClick={generateCode}
                            disabled={loading}
                            className={`px-4 py-2 rounded font-bold text-xs flex items-center gap-2 transition-all ${loading ? 'bg-slate-700 cursor-not-allowed' : 'bg-cyan-600 hover:bg-cyan-500 text-white'}`}
                        >
                            {loading ? 'Thinking...' : <><Code2 size={14} /> GENERATE</>}
                        </button>
                    </div>

                    {/* Toolbar */}
                    <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/20">
                        <div className="flex gap-2">
                            <button
                                onClick={() => setViewMode('code')}
                                className={`px-3 py-1 rounded text-xs font-medium flex items-center gap-2 ${viewMode === 'code' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'text-slate-400 hover:text-white'}`}
                            >
                                <FileCode size={14} /> Code
                            </button>
                            <button
                                onClick={() => setViewMode('diff')}
                                className={`px-3 py-1 rounded text-xs font-medium flex items-center gap-2 ${viewMode === 'diff' ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20' : 'text-slate-400 hover:text-white'}`}
                            >
                                <Eye size={14} /> Diff Review
                            </button>
                        </div>
                        <div className="flex gap-2">
                            <button className="text-slate-400 hover:text-white"><ShieldCheck size={14} /></button>
                            <button className="text-slate-400 hover:text-green-400"><Play size={14} /></button>
                            <button className="text-slate-400 hover:text-purple-400"><Rocket size={14} /></button>
                        </div>
                    </div>

                    {/* Editor Content */}
                    <div className="flex-1 overflow-hidden relative">
                        {viewMode === 'diff' ? (
                            <CodeDiffViewer />
                        ) : (
                            <textarea
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                className="w-full h-full bg-[#0a0a0a] text-slate-300 font-mono text-xs p-4 resize-none focus:outline-none"
                                placeholder="// Generated code will appear here..."
                                spellCheck="false"
                            />
                        )}
                    </div>
                </div>

                {/* RIGHT: Tasks & Logs */}
                <div key="sidebar" className="flex flex-col bg-slate-900/30 h-full">
                    <div className="h-1/2 border-b border-slate-800 flex flex-col overflow-hidden">
                        <div className="draggable-handle p-2 bg-slate-900/50 cursor-move border-b border-slate-800 text-[10px] uppercase font-bold text-slate-500">
                            Task Queue
                        </div>
                        <TaskQueue />
                    </div>

                    <div className="h-1/2 flex flex-col overflow-hidden">
                        <div className="p-2 border-b border-slate-800 flex items-center gap-2 text-xs font-bold text-slate-500 uppercase bg-slate-900/50">
                            <Terminal size={12} /> System Logs
                        </div>
                        <div className="flex-1 overflow-y-auto p-2 space-y-1 font-mono text-[10px]">
                            {logs.map((log, idx) => (
                                <div key={idx} className={`flex gap-2 ${log.type === 'error' ? 'text-red-400' : log.type === 'success' ? 'text-green-400' : 'text-slate-400'}`}>
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
