import React from 'react';
import { Pencil, Move, Crop, Type, Minus, MousePointer2 } from 'lucide-react';

export const DrawingToolbar = ({ activeTool, onSelectTool }) => {
    const tools = [
        { id: 'cursor', icon: <MousePointer2 size={18} />, label: 'Cursor' },
        { id: 'line', icon: <Minus size={18} className="rotate-45" />, label: 'Trendline' },
        { id: 'fib', icon: <Crop size={18} />, label: 'Fibonacci' }, // Mock icon
        { id: 'brush', icon: <Pencil size={18} />, label: 'Brush' },
        { id: 'text', icon: <Type size={18} />, label: 'Text' },
    ];

    return (
        <div className="absolute left-4 top-20 flex flex-col gap-2 bg-slate-900 border border-slate-800 p-1.5 rounded-lg shadow-xl z-20">
            {tools.map(tool => (
                <button
                    key={tool.id}
                    onClick={() => onSelectTool(tool.id)}
                    className={`p-2 rounded hover:bg-slate-800 transition-colors ${
                        activeTool === tool.id ? 'bg-cyan-500/20 text-cyan-400' : 'text-slate-400'
                    }`}
                    title={tool.label}
                >
                    {tool.icon}
                </button>
            ))}
        </div>
    );
};
