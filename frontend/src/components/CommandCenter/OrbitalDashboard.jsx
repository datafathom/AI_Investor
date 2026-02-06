import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, Chip, Switch, FormControlLabel } from '@mui/material';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import PublicIcon from '@mui/icons-material/Public';

// Mock list of 84 agents (abbreviated for component size)
const MOCK_FLEET = Array.from({ length: 84 }, (_, i) => ({
    id: `agent_${i+1}`,
    name: `Agent ${i+1}`,
    dept: Math.floor(i / 6) + 1, // 14 Depts * 6 Agents
    status: Math.random() > 0.9 ? 'ERROR' : (Math.random() > 0.5 ? 'WORKING' : 'IDLE'),
    roi: (Math.random() * 20 - 5).toFixed(1) + '%'
}));

const OrbitalDashboard = () => {
    const [focusMode, setFocusMode] = useState(false);

    // CEO Focus Mode: Only show working or error agents, or high ROI
    const filteredFleet = focusMode 
        ? MOCK_FLEET.filter(a => a.status === 'ERROR' || parseFloat(a.roi) > 10.0) 
        : MOCK_FLEET;

    return (
        <Card sx={{ height: '100%', bgcolor: '#000', color: '#fff', border: '1px solid #333' }}>
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <PublicIcon sx={{ mr: 2, color: '#00FA9A', fontSize: 30 }} />
                        <div>
                            <Typography variant="h5" sx={{ fontFamily: 'monospace', fontWeight: 'bold' }}>
                                ORBITAL COMMAND
                            </Typography>
                            <Typography variant="caption" sx={{ color: '#666' }}>
                                GLOBAL_FLEET_STATUS: {MOCK_FLEET.length} UNITS
                            </Typography>
                        </div>
                    </Box>
                    
                    <FormControlLabel 
                        control={
                            <Switch 
                                checked={focusMode} 
                                onChange={(e) => setFocusMode(e.target.checked)} 
                                color="error" 
                            />
                        }
                        label={
                            <Typography sx={{ fontFamily: 'monospace', color: focusMode ? '#ff4444' : '#666' }}>
                                CEO_FOCUS_MODE
                            </Typography>
                        }
                    />
                </Box>

                <Grid container spacing={1}>
                    {filteredFleet.map((agent) => (
                        <Grid item xs={1} key={agent.id}>
                            <Box 
                                sx={{ 
                                    height: 40, 
                                    bgcolor: agent.status === 'ERROR' ? '#330000' : (agent.status === 'WORKING' ? '#001a0f' : '#111'),
                                    border: `1px solid ${agent.status === 'ERROR' ? '#ff0000' : (agent.status === 'WORKING' ? '#00FA9A' : '#333')}`,
                                    borderRadius: 1,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    cursor: 'pointer',
                                    '&:hover': {
                                        borderColor: '#fff',
                                        bgcolor: '#222'
                                    }
                                }}
                            >
                                <Typography variant="caption" sx={{ fontSize: '0.6rem', color: '#888' }}>
                                    {agent.dept}-{agent.id.split('_')[1]}
                                </Typography>
                                <Box 
                                    sx={{ 
                                        width: 6, 
                                        height: 6, 
                                        borderRadius: '50%', 
                                        bgcolor: agent.status === 'ERROR' ? '#ff0000' : (agent.status === 'WORKING' ? '#00FA9A' : '#444'),
                                        boxShadow: agent.status === 'WORKING' ? '0 0 5px #00FA9A' : 'none'
                                    }} 
                                />
                            </Box>
                        </Grid>
                    ))}
                </Grid>
            </CardContent>
        </Card>
    );
};

export default OrbitalDashboard;
