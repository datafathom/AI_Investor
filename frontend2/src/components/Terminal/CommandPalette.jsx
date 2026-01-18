import React, { useState, useEffect, useRef } from 'react';
import { Search, Command, Zap, ArrowRight, X } from 'lucide-react';
import './CommandPalette.css'; // We'll assume css is co-located or handled globally for now

const CommandPalette = ({ isOpen, onClose, onCommand }) => {
    const [query, setQuery] = useState('');
    const [selectedIndex, setSelectedIndex] = useState(0);
    const inputRef = useRef(null);

    // Mock Commands
    const commands = [
        { id: 'trade-spy', label: 'Buy SPY (Market)', category: 'Trade', shortcut: 'Shift+B' },
        { id: 'view-risk', label: 'View Risk Matrix', category: 'Analytics', shortcut: 'G R' },
        { id: 'clear-cache', label: 'Clear System Cache', category: 'System', shortcut: 'Ctrl+Shift+Del' },
        { id: 'toggle-theme', label: 'Toggle Dark Mode', category: 'Interface', shortcut: 'Cmd+D' },
        { id: 'scan-tech', label: 'Scan Tech Sector', category: 'Scanner', shortcut: '' },
    ];

    const filteredCommands = commands.filter(cmd =>
        cmd.label.toLowerCase().includes(query.toLowerCase()) ||
        cmd.category.toLowerCase().includes(query.toLowerCase())
    );

    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (!isOpen) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (filteredCommands[selectedIndex]) {
                    onCommand(filteredCommands[selectedIndex]);
                    onClose();
                }
            } else if (e.key === 'Escape') {
                onClose();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, filteredCommands, selectedIndex, onCommand, onClose]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[9999] bg-black/60 backdrop-blur-sm flex items-start justify-center pt-[20vh]">
            <div className="w-full max-w-2xl bg-[#0a0a0a] border border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-200">
                <div className="flex items-center px-4 py-3 border-b border-slate-800">
                    <Search className="text-slate-400 mr-3" size={20} />
                    <input
                        ref={inputRef}
                        type="text"
                        className="flex-1 bg-transparent border-none text-white text-lg placeholder-slate-500 focus:outline-none font-mono"
                        placeholder="Type a command or search..."
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                            setSelectedIndex(0);
                        }}
                    />
                    <button onClick={onClose} className="text-slate-500 hover:text-white">
                        <X size={20} />
                    </button>
                </div>

                <div className="max-h-[60vh] overflow-y-auto">
                    {filteredCommands.length > 0 ? (
                        <div className="py-2">
                            {filteredCommands.map((cmd, index) => (
                                <button
                                    key={cmd.id}
                                    onClick={() => {
                                        onCommand(cmd);
                                        onClose();
                                    }}
                                    className={`w-full text-left px-4 py-3 flex items-center justify-between transition-colors ${index === selectedIndex ? 'bg-indigo-600/20 border-l-2 border-indigo-500' : 'hover:bg-white/5 border-l-2 border-transparent'
                                        }`}
                                >
                                    <div className="flex items-center gap-3">
                                        <div className={`p-2 rounded ${index === selectedIndex ? 'bg-indigo-500/20 text-indigo-300' : 'bg-slate-800 text-slate-400'}`}>
                                            {index === selectedIndex ? <ArrowRight size={14} /> : <Zap size={14} />}
                                        </div>
                                        <div>
                                            <div className={`font-medium ${index === selectedIndex ? 'text-white' : 'text-slate-300'}`}>{cmd.label}</div>
                                            <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">{cmd.category}</div>
                                        </div>
                                    </div>
                                    {cmd.shortcut && (
                                        <span className="text-xs font-mono bg-slate-800 px-2 py-1 rounded text-slate-400 border border-slate-700">
                                            {cmd.shortcut}
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>
                    ) : (
                        <div className="p-8 text-center text-slate-500">
                            <Command size={48} className="mx-auto mb-4 opacity-20" />
                            <p>No commands found matching "{query}"</p>
                        </div>
                    )}
                </div>

                <div className="bg-slate-900/50 px-4 py-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-500 font-mono">
                    <div className="flex gap-4">
                        <span><kbd className="bg-slate-800 px-1 rounded">↑↓</kbd> to navigate</span>
                        <span><kbd className="bg-slate-800 px-1 rounded">↵</kbd> to select</span>
                    </div>
                    <span>DataFathom OS v2.1</span>
                </div>
            </div>
        </div>
    );
};

export default CommandPalette;
