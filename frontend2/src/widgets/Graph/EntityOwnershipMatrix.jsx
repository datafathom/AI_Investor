import React, { useMemo } from 'react';
import { ChevronRight, ChevronDown, Layers } from 'lucide-react';

const EntityOwnershipMatrix = ({ data }) => {
    // Simplified tree-grid representation
    const ownershipData = [
        { id: 'Ultimate Holding Co', stake: 100, children: [
            { id: 'Venture Entity A', stake: 60, children: [
                { id: 'Portco X', stake: 15 },
                { id: 'Portco Y', stake: 25 }
            ]},
            { id: 'Family Trust B', stake: 40, children: [
                { id: 'Real Estate LLC', stake: 100 }
            ]}
        ]}
    ];

    const Row = ({ node, level = 0 }) => {
        const [isOpen, setIsOpen] = React.useState(true);
        const hasChildren = node.children && node.children.length > 0;

        return (
            <div className="flex flex-col">
                <div 
                    className="flex items-center py-2 px-3 hover:bg-white/5 cursor-pointer border-b border-white/5 group"
                    style={{ paddingLeft: `${level * 16 + 12}px` }}
                    onClick={() => setIsOpen(!isOpen)}
                >
                    <div className="flex items-center gap-2 flex-1">
                        {hasChildren ? (
                            isOpen ? <ChevronDown size={14} className="text-zinc-500" /> : <ChevronRight size={14} className="text-zinc-500" />
                        ) : (
                            <div className="w-3.5" />
                        )}
                        <Layers size={14} className="text-blue-400 opacity-50 group-hover:opacity-100" />
                        <span className="text-zinc-300 text-xs font-medium">{node.id}</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="text-zinc-500 text-[10px] font-mono">STAKE:</div>
                        <div className="w-16 bg-zinc-800 h-1 rounded-full overflow-hidden">
                            <div className="bg-blue-500 h-full" style={{ width: `${node.stake}%` }} />
                        </div>
                        <span className="text-white text-[10px] font-mono w-8 text-right">{node.stake}%</span>
                    </div>
                </div>
                {isOpen && hasChildren && (
                    node.children.map(child => <Row key={child.id} node={child} level={level + 1} />)
                )}
            </div>
        );
    };

    return (
        <div className="w-full h-full flex flex-col p-4 overflow-y-auto">
            <div className="bg-slate-900/30 rounded-lg border border-white/5 overflow-hidden">
                <div className="flex justify-between items-center py-2 px-4 bg-white/5 border-b border-white/5">
                    <span className="text-zinc-500 text-[9px] font-black uppercase tracking-widest">Entity Structure</span>
                    <span className="text-zinc-500 text-[9px] font-black uppercase tracking-widest">Equity Weight</span>
                </div>
                {ownershipData.map(root => <Row key={root.id} node={root} />)}
            </div>
        </div>
    );
};

export default EntityOwnershipMatrix;
