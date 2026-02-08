import React, { useState, useEffect } from 'react';
import './StorageManager.css';

const StorageManager = () => {
    const [pools, setPools] = useState([]);
    const [syncStatus, setSyncStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [poolRes, syncRes] = await Promise.all([
                fetch('/api/v1/admin/storage/pools'),
                fetch('/api/v1/admin/storage/sync-status')
            ]);
            const poolData = await poolRes.json();
            const syncData = await syncRes.json();
            setPools(poolData);
            setSyncStatus(syncData);
        } catch (error) {
            console.error("Error fetching storage data:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleTriggerSync = async () => {
        setSyncing(true);
        try {
            await fetch('/api/v1/admin/storage/sync/trigger', { method: 'POST' });
            fetchData();
        } catch (error) {
            console.error("Error triggering sync:", error);
        } finally {
            setSyncing(false);
        }
    };

    if (loading) return <div className="storage-loading">QUERYING_ZFS_SUBSYSTEM...</div>;

    return (
        <div className="storage-manager-container">
            <header className="page-header">
                <h1>PRIVATE_CLOUD_STORAGE</h1>
                <div className="header-actions">
                    <button className={`sync-btn ${syncing ? 'syncing' : ''}`} onClick={handleTriggerSync} disabled={syncing}>
                        {syncing ? 'SYNCING...' : 'TRIGGER_OFFSITE_SYNC'}
                    </button>
                </div>
            </header>

            <div className="storage-grid">
                <section className="pools-section">
                    <h3>ZFS_POOLS</h3>
                    <div className="pools-list">
                        {pools.map(pool => (
                            <div key={pool.name} className="pool-card">
                                <div className="pool-header">
                                    <span className="pool-name">{pool.name}</span>
                                    <span className={`pool-health ${pool.health === 'HEALTHY' ? 'good' : 'bad'}`}>
                                        {pool.health}
                                    </span>
                                </div>
                                <div className="pool-metrics">
                                    <div className="metric">
                                        <label>STATUS</label>
                                        <span>{pool.status}</span>
                                    </div>
                                    <div className="metric">
                                        <label>CAPACITY</label>
                                        <span>{pool.capacity}</span>
                                    </div>
                                </div>
                                <div className="pool-scan">
                                    <label>LAST_SCAN</label>
                                    <p>{pool.scan}</p>
                                </div>
                                <div className="vdevs-list">
                                    <label>VDEVS</label>
                                    {pool.vdevs.map((v, i) => (
                                        <div key={i} className="vdev-item">
                                            <span>{v.name}</span>
                                            <span className="vdev-status">{v.status}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="sync-section">
                    <h3>SYNC_STATUS</h3>
                    {syncStatus && (
                        <div className="sync-card">
                            <div className="sync-item">
                                <label>LAST_SYNC_EPOCH</label>
                                <span>{new Date(syncStatus.last_sync).toLocaleString()}</span>
                            </div>
                            <div className="sync-item">
                                <label>CURRENT_STATUS</label>
                                <span className="status-glow">{syncStatus.status}</span>
                            </div>
                            <div className="sync-item">
                                <label>NEXT_SCHEDULED</label>
                                <span>{new Date(syncStatus.next_scheduled).toLocaleDateString()}</span>
                            </div>
                            <div className="sync-progress">
                                <label>SYNC_PROGRESS</label>
                                <div className="bar-bg">
                                    <div className="bar-fill" style={{ width: `${syncStatus.progress}%` }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
};

export default StorageManager;
