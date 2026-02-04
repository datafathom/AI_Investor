import React, { useState } from 'react';
import { Folder, FileCode, ChevronRight, ChevronDown, File } from 'lucide-react';

const FileTree = () => {
    const [expanded, setExpanded] = useState({ 'src': true, 'components': true });

    const toggle = (dir) => {
        setExpanded(prev => ({ ...prev, [dir]: !prev[dir] }));
    };

    const tree = {
        name: 'root',
        type: 'folder',
        children: [
            {
                name: 'src', type: 'folder', children: [
                    {
                        name: 'components', type: 'folder', children: [
                            { name: 'AlphaEngine.py', type: 'file', lang: 'python' },
                            { name: 'RiskMetrics.py', type: 'file', lang: 'python' },
                            { name: 'DataIngest.py', type: 'file', lang: 'python' },
                        ]
                    },
                    { name: 'main.py', type: 'file', lang: 'python' },
                    { name: 'config.json', type: 'file', lang: 'json' },
                ]
            },
            {
                name: 'tests', type: 'folder', children: [
                    { name: 'test_alpha.py', type: 'file', lang: 'python' }
                ]
            },
            { name: 'README.md', type: 'file', lang: 'md' }
        ]
    };

    const renderNode = (node, path = '') => {
        const isFolder = node.type === 'folder';
        const isExpanded = expanded[node.name];

        return (
            <div key={node.name} className="pl-3">
                <div
                    className={`flex items-center gap-1.5 py-1 px-2 rounded cursor-pointer hover:bg-slate-800 border border-transparent hover:border-slate-700 transition-colors text-xs font-mono group ${isFolder ? 'text-slate-300' : 'text-slate-400'}`}
                    onClick={(e) => {
                        e.stopPropagation();
                        if (isFolder) toggle(node.name);
                    }}
                >
                    {isFolder && (
                        <span className="text-slate-500">
                            {isExpanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                        </span>
                    )}
                    {!isFolder && <span className="w-3"></span>}

                    {isFolder ? <Folder size={14} className="text-blue-400" /> : <FileCode size={14} className={node.name.endsWith('py') ? 'text-yellow-400' : 'text-slate-500'} />}

                    <span className="group-hover:text-white">{node.name}</span>
                </div>
                {isFolder && isExpanded && node.children && (
                    <div className="border-l border-slate-800 ml-2.5">
                        {node.children.map(child => renderNode(child, path + '/' + node.name))}
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-2 mb-2 flex items-center justify-between">
                <span>Project Explorer</span>
                <span className="text-[10px] bg-slate-800 px-1 rounded">v2.1</span>
            </h3>
            <div className="flex-1 overflow-y-auto">
                {renderNode(tree)}
            </div>
        </div>
    );
};

export default FileTree;
