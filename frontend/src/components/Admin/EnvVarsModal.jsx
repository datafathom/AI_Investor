import React, { useState, useEffect } from 'react';
import { Settings, Eye, EyeOff, Save, Plus, Lock, X } from "lucide-react";
import './EnvVarsModal.css';

const EnvVarsModal = ({ open, onOpenChange }) => {
    const [envVars, setEnvVars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const [showSensitive, setShowSensitive] = useState({});
    const [error, setError] = useState("");

    // Edit/Add State
    const [editMode, setEditMode] = useState(false);
    const [currentKey, setCurrentKey] = useState("");
    const [currentValue, setCurrentValue] = useState("");

    const fetchEnvVars = async () => {
        setLoading(true);
        setError("");
        try {
            const response = await fetch('http://localhost:5050/api/v1/admin/env');
            if (response.ok) {
                const data = await response.json();
                setEnvVars(data);
            } else {
                setError("Failed to fetch variables");
            }
        } catch (error) {
            console.error("Failed to fetch env vars", error);
            setError("Connection error");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (open) fetchEnvVars();
    }, [open]);

    const handleSave = async () => {
        if (!currentKey.trim()) return;

        try {
            const response = await fetch('http://localhost:5050/api/v1/admin/env', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: currentKey, value: currentValue })
            });

            if (!response.ok) throw new Error("Failed to save variable");

            setEditMode(false);
            setCurrentKey("");
            setCurrentValue("");
            fetchEnvVars();
        } catch (error) {
            setError(error.message);
        }
    };

    const toggleShow = (key) => {
        setShowSensitive(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const filteredVars = envVars.filter(v => 
        v.key.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (!open) return null;

    return (
        <div className="modal-overlay" onClick={() => onOpenChange(false)}>
            <div className="env-vars-modal" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <div className="header-title">
                        <h2>System Environment Variables</h2>
                        <button className="close-btn" onClick={() => onOpenChange(false)}>
                            <X size={20} />
                        </button>
                    </div>
                    <p className="subtitle">
                        Manage server-side configuration. Sensitive values are masked by default.
                    </p>
                </div>

                <div className="modal-actions">
                    <input 
                        type="text"
                        placeholder="Search variables..." 
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                    <button 
                        className="add-btn"
                        onClick={() => { setEditMode(true); setCurrentKey(""); setCurrentValue(""); }}
                    >
                        <Plus size={16} /> Add Variable
                    </button>
                </div>

                {editMode && (
                    <div className="edit-panel">
                        <h3>Add / Edit Variable</h3>
                        <div className="form-row">
                            <div className="input-group">
                                <label>Key</label>
                                <input 
                                    value={currentKey} 
                                    onChange={(e) => setCurrentKey(e.target.value.toUpperCase())}
                                    placeholder="API_KEY"
                                    className="mono-input"
                                />
                            </div>
                            <div className="input-group">
                                <label>Value</label>
                                <input 
                                    value={currentValue}
                                    onChange={(e) => setCurrentValue(e.target.value)}
                                    type="password"
                                    placeholder="Value..."
                                />
                            </div>
                        </div>
                        <div className="form-actions">
                            <button className="cancel-btn" onClick={() => setEditMode(false)}>Cancel</button>
                            <button className="save-btn" onClick={handleSave}>
                                <Save size={16} /> Save
                            </button>
                        </div>
                    </div>
                )}

                {error && <div className="error-banner">{error}</div>}

                <div className="table-container">
                    <table className="env-table">
                        <thead>
                            <tr>
                                <th>Key</th>
                                <th>Value</th>
                                <th className="text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr>
                                    <td colSpan="3" className="loading-cell">Loading...</td>
                                </tr>
                            ) : filteredVars.length === 0 ? (
                                <tr>
                                    <td colSpan="3" className="empty-cell">No variables found.</td>
                                </tr>
                            ) : (
                                filteredVars.map((v) => (
                                    <tr key={v.key}>
                                        <td className="key-cell">
                                            {v.key}
                                            {v.is_sensitive && <Lock size={12} className="sensitive-icon" />}
                                        </td>
                                        <td className="value-cell">
                                            <div className="value-wrapper">
                                                <span className={v.is_sensitive && !showSensitive[v.key] ? "masked" : "plain"}>
                                                    {v.is_sensitive && !showSensitive[v.key] ? "••••••••••••••••" : v.value}
                                                </span>
                                                {v.is_sensitive && (
                                                    <button className="toggle-show-btn" onClick={() => toggleShow(v.key)}>
                                                        {showSensitive[v.key] ? <EyeOff size={14} /> : <Eye size={14} />}
                                                    </button>
                                                )}
                                            </div>
                                        </td>
                                        <td className="action-cell">
                                            <button 
                                                className="edit-icon-btn"
                                                onClick={() => {
                                                    setEditMode(true);
                                                    setCurrentKey(v.key);
                                                    setCurrentValue("");
                                                }}
                                            >
                                                <Settings size={14} />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default EnvVarsModal;
