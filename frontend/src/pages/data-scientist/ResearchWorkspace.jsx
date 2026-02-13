import React, { useState, useEffect } from 'react';
import { researchService } from '../../services/researchService';
import { NotebookSidebar, CodeCell, MarkdownCell } from '../../components/editors/NotebookEditor';
import { toast } from 'sonner';
import { Plus, Save, Play, RefreshCw, Terminal } from 'lucide-react';

const ResearchWorkspace = () => {
    const [notebooks, setNotebooks] = useState([]);
    const [activeNotebook, setActiveNotebook] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadNotebooks();
    }, []);

    const loadNotebooks = async () => {
        try {
            const data = await researchService.getNotebooks();
            setNotebooks(data);
             if (data.length > 0 && !activeNotebook) {
                setActiveNotebook(data[0]);
            }
        } catch (e) {
            toast.error("Failed to load notebooks");
        } finally {
            setLoading(false);
        }
    };

    const handleCreateNotebook = async () => {
        const name = prompt("Notebook Name:");
        if (name) {
            try {
                const nb = await researchService.createNotebook(name);
                setNotebooks([...notebooks, nb]);
                setActiveNotebook(nb);
                toast.success("Notebook created");
            } catch (e) {
                toast.error("Failed to create notebook");
            }
        }
    };

    const handleSelectNotebook = async (id) => {
        try {
            setLoading(true);
            const nb = await researchService.getNotebook(id);
            setActiveNotebook(nb);
        } catch (e) {
             toast.error("Failed to load notebook");
        } finally {
             setLoading(false);
        }
    };

    const handleCellChange = (cellId, content) => {
        if (!activeNotebook) return;
        const updatedCells = activeNotebook.cells.map(c => 
            c.id === cellId ? { ...c, content } : c
        );
        setActiveNotebook({ ...activeNotebook, cells: updatedCells });
    };

    const handleExecuteCell = async (cellId) => {
        if (!activeNotebook) return;
        const cell = activeNotebook.cells.find(c => c.id === cellId);
        if (!cell) return;

        try {
            const result = await researchService.executeCell(activeNotebook.id, cell.content);
            const updatedCells = activeNotebook.cells.map(c => 
                c.id === cellId ? { ...c, output: result, execution_count: (c.execution_count || 0) + 1 } : c
            );
            setActiveNotebook({ ...activeNotebook, cells: updatedCells });
            // Auto-save
            await researchService.saveNotebook(activeNotebook.id, { ...activeNotebook, cells: updatedCells });
        } catch (e) {
            toast.error("Execution failed");
        }
    };

    const handleAddCell = (type) => {
        if (!activeNotebook) return;
        const newCell = {
            id: `cell_${Date.now()}`,
            type,
            content: '',
            execution_count: null,
            output: null
        };
        const updatedCells = [...activeNotebook.cells, newCell];
        setActiveNotebook({ ...activeNotebook, cells: updatedCells });
    };

    const handleDeleteCell = (cellId) => {
         if (!activeNotebook) return;
         const updatedCells = activeNotebook.cells.filter(c => c.id !== cellId);
         setActiveNotebook({ ...activeNotebook, cells: updatedCells });
    };

    const handleSave = async () => {
        if (!activeNotebook) return;
        try {
            await researchService.saveNotebook(activeNotebook.id, activeNotebook);
            toast.success("Saved");
        } catch (e) {
            toast.error("Failed to save");
        }
    };

    return (
        <div className="flex h-full bg-slate-950 text-slate-200">
            <NotebookSidebar 
                notebooks={notebooks} 
                activeId={activeNotebook?.id} 
                onSelect={handleSelectNotebook} 
                onCreate={handleCreateNotebook} 
            />
            
            <div className="flex-1 flex flex-col h-full overflow-hidden">
                {activeNotebook ? (
                    <>
                        {/* Toolbar */}
                        <div className="bg-slate-900 border-b border-slate-800 p-3 flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <Terminal size={18} className="text-emerald-500" />
                                <span className="font-bold text-white">{activeNotebook.name}</span>
                                <span className="text-xs text-slate-500 ml-2">Python 3 (Kernel Ready)</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <button onClick={() => handleAddCell('code')} className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded text-xs font-bold text-slate-300">
                                    <Plus size={14} /> Code
                                </button>
                                <button onClick={() => handleAddCell('markdown')} className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded text-xs font-bold text-slate-300">
                                    <Plus size={14} /> Markdown
                                </button>
                                <div className="w-px h-4 bg-slate-700 mx-1"></div>
                                <button onClick={handleSave} className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded text-xs font-bold text-indigo-400">
                                    <Save size={14} /> Save
                                </button>
                            </div>
                        </div>

                        {/* Editor Area */}
                        <div className="flex-1 overflow-y-auto p-8">
                            <div className="max-w-4xl mx-auto">
                                {activeNotebook.cells.map(cell => (
                                    cell.type === 'code' ? (
                                        <CodeCell 
                                            key={cell.id} 
                                            cell={cell} 
                                            onChange={handleCellChange} 
                                            onExecute={handleExecuteCell}
                                            onDelete={handleDeleteCell} 
                                        />
                                    ) : (
                                        <MarkdownCell 
                                            key={cell.id} 
                                            cell={cell} 
                                            onChange={handleCellChange} 
                                            onDelete={handleDeleteCell}
                                        />
                                    )
                                ))}
                                
                                <div className="h-32 flex items-center justify-center text-slate-700 text-sm border-2 border-dashed border-slate-800 rounded-lg mt-4 cursor-pointer hover:border-slate-700 hover:text-slate-500 transition-colors"
                                     onClick={() => handleAddCell('code')}
                                >
                                    <Plus size={16} className="mr-2" /> Add Code Cell
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 flex items-center justify-center text-slate-500">
                        Select a notebook to start research.
                    </div>
                )}
            </div>
        </div>
    );
};

export default ResearchWorkspace;
