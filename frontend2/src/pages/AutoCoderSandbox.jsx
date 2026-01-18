import React, { useState, useEffect, useRef } from 'react';
import { autoCoderService } from '../services/autoCoderService';
import { Terminal, Code, Play, CheckCircle, Cpu, Loader, AlertTriangle, PlayCircle } from 'lucide-react';
import './AutoCoderSandbox.css';

/**
 * AutoCoderSandbox.jsx
 * Theme: Hacker / IDE / Cyberpunk
 * 
 * Demonstrates the AI's ability to "Write its own code".
 */
const AutoCoderSandbox = () => {
    const [tasks, setTasks] = useState([]);
    const [activeTask, setActiveTask] = useState(null);
    const [codeContent, setCodeContent] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [status, setStatus] = useState('IDLE'); // IDLE, CODING, TESTING, DEPLOYED
    const [logs, setLogs] = useState([]);
    const codeContainerRef = useRef(null);

    useEffect(() => {
        setTasks(autoCoderService.getTasks());
    }, []);

    // Auto-scroll code view
    useEffect(() => {
        if (codeContainerRef.current) {
            codeContainerRef.current.scrollTop = codeContainerRef.current.scrollHeight;
        }
    }, [codeContent]);

    const startTask = (taskId) => {
        if (isTyping) return;

        setActiveTask(taskId);
        setIsTyping(true);
        setStatus('CODING');
        setCodeContent('');
        setLogs([]);
        addLog('Initializing Stacker Agent v4.2...');
        addLog('Analyzing requirements...');

        autoCoderService.streamCode(taskId,
            (newCode) => setCodeContent(newCode),
            () => {
                setIsTyping(false);
                runTests();
            }
        );
    };

    const runTests = async () => {
        setStatus('TESTING');
        addLog('Code generation complete. Starting Unit Tests...');

        const steps = [
            'Verifying syntax compliance (PEP-8)...',
            'Running static analysis...',
            'Executing functional tests...',
            'Checking rate limit logic...',
            'Validating API signatures...'
        ];

        for (let i = 0; i < steps.length; i++) {
            await new Promise(r => setTimeout(r, 800));
            addLog(steps[i], 'success');
        }

        setStatus('DEPLOY_READY');
        addLog('All Tests Passed (5/5). Ready for Hot-Swap.', 'success');
    };

    const deployModule = () => {
        setStatus('DEPLOYED');
        addLog('Stopping current worker instance...');
        addLog('Hot-swapping module_alpha_v1...', 'warn');
        addLog('Restarting worker...', 'warn');
        addLog('Deployment Successful. New logic active.', 'success');
    }

    const addLog = (msg, type = 'info') => {
        setLogs(prev => [...prev, { msg, type, time: new Date().toLocaleTimeString() }]);
    };

    return (
        <div className="auto-coder-container min-h-screen p-6 text-green-500 font-mono">
            {/* Header */}
            <header className="mb-6 flex items-center justify-between p-4 border border-green-900 bg-black/60 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <Cpu className="text-green-500 animate-neon-pulse" size={32} />
                    <div>
                        <h1 className="text-2xl font-bold tracking-tighter text-green-400 text-glow-cyan">AUTO-CODER <span className="text-xs border border-green-500 px-1 rounded">V4.0</span></h1>
                        <p className="text-xs text-green-700 font-bold uppercase tracking-widest">Self-Improving Agent Sandbox</p>
                    </div>
                </div>
                <div className="flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${status === 'IDLE' ? 'bg-slate-500' : 'bg-green-500 animate-ping'}`}></div>
                        STATUS: {status}
                    </div>
                    <div className="bg-green-900/20 px-3 py-1 rounded border border-green-900 text-green-300">
                        CPU: {(30 + Math.random() * 40).toFixed(1)}%
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-12 gap-6 h-[calc(100vh-160px)]">

                {/* Left: Task Queue */}
                <div className="col-span-3 border border-green-900 bg-black/40 flex flex-col">
                    <div className="p-3 border-b border-green-900 bg-green-900/20 text-xs font-bold flex items-center gap-2">
                        <Terminal size={14} /> PENDING OPTIMIZATIONS
                    </div>
                    <div className="flex-1 p-2 space-y-2 overflow-y-auto">
                        {tasks.map(task => (
                            <div
                                key={task.id}
                                onClick={() => startTask(task.id)}
                                className={`p-3 border cursor-pointer transition-all hover:scale-[1.02] interact-hover ${activeTask === task.id ? 'border-green-500 bg-green-900/40 shadow-[0_0_15px_rgba(34,197,94,0.2)]' : 'border-green-900/30 text-green-700 hover:border-green-700'}`}
                            >
                                <div className="font-bold text-sm mb-1">{task.name}</div>
                                <div className="text-[10px] leading-tight opacity-70">{task.description}</div>
                                {activeTask === task.id && isTyping && (
                                    <div className="mt-2 text-[10px] animate-pulse">Running Generation...</div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Center: Editor */}
                <div className="col-span-6 border border-green-900 bg-black flex flex-col relative overflow-hidden">
                    <div className="p-2 border-b border-green-900 flex justify-between items-center bg-slate-900">
                        <span className="text-xs text-slate-400 flex items-center gap-2">
                            <Code size={14} /> main.py
                        </span>
                        {isTyping && <Loader size={14} className="animate-spin text-green-500" />}
                    </div>
                    <div
                        ref={codeContainerRef}
                        className="flex-1 p-4 overflow-y-auto font-mono text-sm leading-relaxed text-slate-300"
                    >
                        <pre className="whitespace-pre-wrap">
                            {codeContent}
                            <span className="animate-pulse inline-block w-2 h-4 bg-green-500 ml-1"></span>
                        </pre>
                    </div>
                </div>

                {/* Right: Output & Test Runner */}
                <div className="col-span-3 border border-green-900 bg-black/40 flex flex-col">
                    <div className="p-3 border-b border-green-900 bg-green-900/20 text-xs font-bold flex items-center gap-2">
                        <PlayCircle size={14} /> RUNTIME LOGS
                    </div>
                    <div className="flex-1 p-3 overflow-y-auto font-mono text-xs space-y-2">
                        {logs.map((log, idx) => (
                            <div key={idx} className={`flex gap-2 ${log.type === 'error' ? 'text-red-500' : log.type === 'warn' ? 'text-amber-400' : log.type === 'success' ? 'text-green-400' : 'text-slate-500'}`}>
                                <span className="opacity-50">[{log.time}]</span>
                                <span>{log.type === 'success' ? '✓ ' : '> '}{log.msg}</span>
                            </div>
                        ))}
                        {status === 'DEPLOY_READY' && (
                            <button
                                onClick={deployModule}
                                className="w-full mt-4 bg-green-600 hover:bg-green-500 text-black font-bold py-2 rounded animate-bounce shadow-[0_0_20px_rgba(34,197,94,0.5)] interact-hover"
                            >
                                DEPLOY TO PRODUCTION
                            </button>
                        )}
                        {status === 'DEPLOYED' && (
                            <div className="mt-4 p-3 border border-green-500 bg-green-900/20 text-center text-green-400 font-bold">
                                <CheckCircle className="mx-auto mb-2" size={24} />
                                MODULE ACTIVE
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AutoCoderSandbox;
