import React, { useState, useEffect } from 'react';
import { Play, Save, Trash2, Plus, RefreshCw, FileText, Code, Check } from 'lucide-react';

export const NotebookSidebar = ({ notebooks, activeId, onSelect, onCreate }) => {
    return (
        <div className="w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col h-full">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider">Notebooks</h3>
                <button onClick={onCreate} className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-white">
                    <Plus size={16} />
                </button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-1">
                {notebooks.map(nb => (
                    <div 
                        key={nb.id}
                        onClick={() => onSelect(nb.id)}
                        className={`p-2 rounded text-sm cursor-pointer flex items-center gap-2 ${
                            activeId === nb.id ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30' : 'text-slate-400 hover:bg-slate-800'
                        }`}
                    >
                        <FileText size={14} />
                        <span className="truncate">{nb.name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export const CodeCell = ({ cell, onChange, onExecute, onDelete }) => {
    const [running, setRunning] = useState(false);

    const handleRun = async () => {
        setRunning(true);
        await onExecute(cell.id);
        setRunning(false);
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden mb-4 group ring-1 ring-transparent focus-within:ring-indigo-500/50 transition-all">
            <div className="flex bg-slate-900 border-b border-slate-800">
                <div className="w-12 bg-slate-800/50 text-slate-500 text-xs font-mono flex items-center justify-center border-r border-slate-800 select-none">
                    In [{cell.execution_count || ' '}]
                </div>
                <div className="flex-1 bg-slate-950">
                    <textarea 
                        value={cell.content}
                        onChange={(e) => onChange(cell.id, e.target.value)}
                        className="w-full bg-transparent text-slate-200 font-mono text-sm p-3 outline-none min-h-[80px]"
                        spellCheck={false}
                    />
                </div>
            </div>
            
            {/* Toolbar */}
             <div className="bg-slate-900 px-2 py-1 flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button onClick={handleRun} className="flex items-center gap-1 text-emerald-500 hover:text-emerald-400 text-xs px-2 py-1 rounded hover:bg-slate-800">
                    <Play size={12} fill="currentColor" /> Run
                </button>
                <button onClick={() => onDelete(cell.id)} className="text-slate-500 hover:text-red-400 text-xs px-2 py-1 rounded hover:bg-slate-800">
                    <Trash2 size={12} />
                </button>
            </div>

            {/* Output */}
            {cell.output && (
                <div className="border-t border-slate-800 bg-slate-950 p-3">
                    {cell.output.stderr && (
                        <div className="text-red-400 font-mono text-xs whitespace-pre-wrap mb-2">{cell.output.stderr}</div>
                    )}
                    {cell.output.stdout && (
                        <div className="text-slate-300 font-mono text-xs whitespace-pre-wrap">{cell.output.stdout}</div>
                    )}
                </div>
            )}
        </div>
    );
};

export const MarkdownCell = ({ cell, onChange, onDelete, onEdit }) => {
    const [editing, setEditing] = useState(false);

    return (
        <div className="mb-4 group relative">
             {editing ? (
                <textarea 
                    value={cell.content}
                    onChange={(e) => onChange(cell.id, e.target.value)}
                    onBlur={() => setEditing(false)}
                    autoFocus
                    className="w-full bg-slate-900 text-slate-200 p-3 rounded border border-indigo-500 outline-none min-h-[60px]"
                />
             ) : (
                 <div 
                    onClick={() => setEditing(true)}
                    className="prose prose-invert max-w-none p-3 hover:bg-slate-900/50 rounded cursor-text"
                >
                    {/* Simplified render for now */}
                    {cell.content.split('\n').map((line, i) => (
                        <div key={i} className={line.startsWith('#') ? 'font-bold text-white text-lg' : 'text-slate-300'}>
                            {line.replace(/^#+\s/, '')}
                        </div>
                    ))}
                 </div>
             )}
             
             <div className="absolute top-0 right-0 opacity-0 group-hover:opacity-100 p-2">
                <button onClick={() => onDelete(cell.id)} className="text-slate-500 hover:text-red-400">
                    <Trash2 size={14} />
                </button>
             </div>
        </div>
    );
};
