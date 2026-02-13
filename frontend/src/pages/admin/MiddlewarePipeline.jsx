import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './MiddlewarePipeline.css';
import MiddlewareStep from '../../components/Admin/MiddlewareStep';

const MiddlewarePipeline = () => {
    const [pipeline, setPipeline] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        fetchPipeline();
    }, []);

    const fetchPipeline = async () => {
        try {
            const data = await apiClient.get('/admin/middleware/pipeline');
            setPipeline(data.steps);
        } catch (error) {
            console.error("Error fetching pipeline:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (id, enabled) => {
        try {
            await apiClient.patch(`/admin/middleware/${id}`, { enabled });
            setPipeline(pipeline.map(step => step.id === id ? { ...step, enabled } : step));
        } catch (error) {
            console.error("Error toggling middleware:", error);
        }
    };

    const moveStep = (dragIndex, hoverIndex) => {
        const draggedItem = pipeline[dragIndex];
        const newPipeline = [...pipeline];
        newPipeline.splice(dragIndex, 1);
        newPipeline.splice(hoverIndex, 0, draggedItem);
        setPipeline(newPipeline);
    };

    const saveOrder = async () => {
        setSaving(true);
        try {
            await apiClient.put('/admin/middleware/pipeline', pipeline.map(s => s.id));
            alert("PIPELINE_ORDER_SAVED. RESTART_REQUIRED.");
        } catch (error) {
            console.error("Error saving order:", error);
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="pipeline-loading">MAPPING_INTERCEPTOR_CHAIN...</div>;

    return (
        <div className="middleware-pipeline-container">
            <header className="page-header">
                <div className="title-group">
                    <h1>MIDDLEWARE_PIPELINE</h1>
                    <p className="subtitle">REQUEST_RESPONSE_INTERCEPTOR_ORCHESTRATION</p>
                </div>
                <button className={`save-btn ${saving ? 'saving' : ''}`} onClick={saveOrder} disabled={saving}>
                    {saving ? 'SYNCING...' : 'COMMIT_CHANGES'}
                </button>
            </header>

            <div className="pipeline-canvas">
                <div className="flow-start">CLIENT_REQUEST</div>
                <div className="steps-container">
                    {pipeline.map((step, index) => (
                        <MiddlewareStep 
                            key={step.id} 
                            index={index}
                            step={step} 
                            onToggle={handleToggle}
                            onMove={moveStep}
                        />
                    ))}
                </div>
                <div className="flow-end">API_HANDLER</div>
            </div>

            <div className="restart-notice">
                <span className="warning-icon">⚠️</span>
                NOTE: Order changes and toggles require a service restart to propagate to active threads.
            </div>
        </div>
    );
};

export default MiddlewarePipeline;
