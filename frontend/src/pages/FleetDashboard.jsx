import React, { useState, useMemo } from 'react';
import { Box, Grid, Card, Typography, Chip, Tooltip, IconButton, TextField, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import PauseCircleIcon from '@mui/icons-material/PauseCircle';
import ReplayIcon from '@mui/icons-material/Replay';
import './FleetDashboard.css';

const MOCK_AGENTS = Array.from({ length: 84 }, (_, i) => ({
    id: `agent_${(i + 1).toString().padStart(3, '0')}`,
    name: `Agent ${i + 1}`,
    status: Math.random() > 0.8 ? 'ERROR' : (Math.random() > 0.4 ? 'ACTIVE' : 'IDLE'),
    roi: (Math.random() * 20 - 5).toFixed(2),
    load: Math.floor(Math.random() * 100),
    tasks: Math.floor(Math.random() * 50),
    latency: Math.floor(Math.random() * 500) + 'ms'
}));

const FleetDashboard = () => {
    const [search, setSearch] = useState('');
    const [filter, setFilter] = useState('ALL');

    const filteredAgents = useMemo(() => {
        return MOCK_AGENTS.filter(a => {
            const matchesSearch = a.id.includes(search) || a.name.toLowerCase().includes(search.toLowerCase());
            const matchesFilter = filter === 'ALL' || a.status === filter;
            return matchesSearch && matchesFilter;
        });
    }, [search, filter]);

    const getStatusColor = (status) => {
        switch(status) {
            case 'ACTIVE': return '#859900';
            case 'ERROR': return '#dc322f';
            case 'IDLE': return '#268bd2';
            default: return '#586e75';
        }
    };

    return (
        <Box className="fleet-dashboard-root">
            <Box className="fleet-header">
                <Typography variant="h4" className="fleet-title">Sovereign Fleet Command</Typography>
                <Box className="fleet-controls">
                    <TextField 
                        placeholder="Search Fleet..."
                        size="small"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        InputProps={{
                            startAdornment: <InputAdornment position="start"><SearchIcon /></InputAdornment>,
                            sx: { color: '#eee', bgcolor: '#073642' }
                        }}
                    />
                    <Box className="fleet-summary">
                        <Chip label={`Total: ${MOCK_AGENTS.length}`} variant="outlined" sx={{ color: '#eee' }} />
                        <Chip label={`Active: ${MOCK_AGENTS.filter(a => a.status === 'ACTIVE').length}`} color="success" />
                        <Chip label={`Critical: ${MOCK_AGENTS.filter(a => a.status === 'ERROR').length}`} color="error" />
                    </Box>
                </Box>
            </Box>

            <Grid container spacing={1} className="fleet-grid">
                {filteredAgents.map((agent) => (
                    <Grid key={agent.id} size={{ xs: 12, sm: 6, md: 3, lg: 2, xl: 1.5 }}>
                        <Card className={`agent-tiny-card ${agent.status.toLowerCase()}`}>
                            <Box className="card-top">
                                <Typography className="agent-id-text">{agent.id}</Typography>
                                <Box className="status-dot" sx={{ bgcolor: getStatusColor(agent.status) }} />
                            </Box>
                            <Box className="card-stats">
                                <Box className="stat-row">
                                    <Typography className="stat-label">ROI</Typography>
                                    <Typography className={`stat-value ${parseFloat(agent.roi) >= 0 ? 'plus' : 'minus'}`}>
                                        {agent.roi}%
                                    </Typography>
                                </Box>
                                <Box className="stat-row">
                                    <Typography className="stat-label">LOAD</Typography>
                                    <Box className="load-bar-bg"><Box className="load-bar-fill" sx={{ width: `${agent.load}%` }} /></Box>
                                </Box>
                            </Box>
                            <Box className="card-actions">
                                <IconButton size="small"><ReplayIcon fontSize="inherit" /></IconButton>
                                <IconButton size="small"><PauseCircleIcon fontSize="inherit" /></IconButton>
                            </Box>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default FleetDashboard;
