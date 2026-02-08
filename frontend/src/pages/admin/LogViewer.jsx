import React, { useState, useEffect } from 'react';
import './LogViewer.css';

const LogViewer = () => {
    const [logs, setLogs] = useState([]);
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState('backend_debug.log');
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchFiles();
        fetchLogs();
        const interval = setInterval(fetchLogs, 10000);
        return () => clearInterval(interval);
    }, [selectedFile, searchQuery]);

    const fetchFiles = async () => {
        try {
            const response = await fetch('/api/v1/admin/logs/files');
            const data = await response.json();
            setFiles(data);
        } catch (error) {
            console.error("Error fetching log files:", error);
        }
    };

    const fetchLogs = async () => {
        try {
            const url = searchQuery 
                ? `/api/v1/admin/logs/search?query=${searchQuery}`
                : `/api/v1/admin/logs/tail/${selectedFile}?lines=100`;
            const response = await fetch(url);
            const data = await response.json();
            setLogs(searchQuery ? data.results : data.map(l => ({ content: l })));
        } catch (error) {
            console.error("Error fetching logs:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="log-viewer-container">
            <header className="page-header">
                <h1>SYSTEM_LOG_VIEWER</h1>
                <div className="header-controls">
                    <input 
                        type="text" 
                        placeholder="SEARCH_LOGS..." 
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    <select value={selectedFile} onChange={(e) => setSelectedFile(e.target.value)}>
                        {files.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                </div>
            </header>

            <div className="log-display">
                <div className="log-canvas">
                    {loading ? (
                        <div className="log-loading">STREAMING_LOG_BUFFER...</div>
                    ) : (
                        logs.map((log, i) => (
                            <div key={i} className="log-line">
                                <span className="line-num">[{i}]</span>
                                <span className="line-content">{log.content || log}</span>
                                {log.file && <span className="line-file">@{log.file}</span>}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default LogViewer;
