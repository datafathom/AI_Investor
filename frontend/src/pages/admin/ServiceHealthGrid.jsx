import React, { useState, useEffect } from 'react';
import './ServiceHealthGrid.css';
import ServiceCard from '../../components/cards/ServiceCard';
import apiClient from '../../services/apiClient';

const ServiceHealthGrid = () => {
    const [healthData, setHealthData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState(null);

    useEffect(() => {
        fetchHealth();
        const interval = setInterval(fetchHealth, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchHealth = async () => {
        try {
            const data = await apiClient.get('/admin/health/services');
            setHealthData(data);
            setLastUpdated(new Date());
        } catch (error) {
            console.error("Error fetching health data:", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading && !healthData) return <div className="health-loading">SCANNING_SYSTEM_VITALS...</div>;

    return (
        <div className="health-grid-container">
            <header className="page-header">
                <div className="title-group">
                    <h1>SYSTEM_HEALTH_GRID</h1>
                    <span className={`overall-status ${healthData?.overall.toLowerCase()}`}>
                        {healthData?.overall}
                    </span>
                </div>
                <div className="header-meta">
                    <label>LAST_SCAN</label>
                    <span>{lastUpdated?.toLocaleTimeString()}</span>
                </div>
            </header>

            <div className="service-grid">
                {healthData?.services.map(service => (
                    <ServiceCard key={service.id} service={service} />
                ))}
            </div>

            <section className="vendor-apis-section">
                <h3>EXTERNAL_VENDOR_CONNECTIVITY</h3>
                <div className="vendor-grid">
                    {Object.entries(healthData?.vendor_apis || {}).map(([name, data]) => (
                        <div key={name} className={`vendor-card ${data.status.toLowerCase()}`}>
                            <span className="vendor-name">{name.replace('_', ' ').toUpperCase()}</span>
                            <span className="vendor-latency">{data.latency_ms}ms</span>
                            <span className="vendor-status">{data.status}</span>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default ServiceHealthGrid;
