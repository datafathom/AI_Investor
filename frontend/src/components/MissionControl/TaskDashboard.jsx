import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Trash2, RefreshCw, Layers } from 'lucide-react';
import './TaskDashboard.css';

const TaskDashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const resp = await axios.get('/api/tasks/status');
      setJobs(resp.data.jobs || []);
    } catch (err) {
      console.error('Failed to fetch jobs', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleKill = async (jobId) => {
    if (!window.confirm(`Are you sure you want to kill job ${jobId}?`)) return;
    try {
      await axios.post(`/api/tasks/kill/${jobId}`);
      fetchJobs();
    } catch (err) {
      alert('Failed to kill job');
    }
  };

  return (
    <div className="task-dashboard">
      <div className="dashboard-section">
        <div className="section-header">
          <div className="section-title">
            <Layers size={16} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            Active Worker Queue (ARQ)
          </div>
          <button className="refresh-btn" onClick={fetchJobs} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'spinning' : ''} />
          </button>
        </div>

        <table className="queue-table">
          <thead>
            <tr>
              <th>Job ID</th>
              <th>Mission</th>
              <th>Status</th>
              <th>StartTime</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length === 0 ? (
              <tr>
                <td colSpan="5" align="center">No active or queued jobs</td>
              </tr>
            ) : (
              jobs.map((job) => (
                <tr key={job.id}>
                  <td>{job.id}</td>
                  <td>{job.mission_id || 'N/A'}</td>
                  <td>
                    <span className={`status-badge status-${job.status}`}>
                      {job.status}
                    </span>
                  </td>
                  <td>{job.start_time || '-'}</td>
                  <td>
                    {job.status === 'running' && (
                      <button className="kill-btn" onClick={() => handleKill(job.id)}>
                        <Trash2 size={12} /> Kill
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TaskDashboard;
