import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Button, Box, Select, MenuItem, TextField, CircularProgress, Alert } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import SaveIcon from '@mui/icons-material/Save';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

const AgentLogicEditor = () => {
    const [selectedAgent, setSelectedAgent] = useState('scraper_agent_01');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState(null);
    const [code, setCode] = useState(`
import logging
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    """
    Sovereign OS: Autonomous Logic Forge
    Generated for: ${selectedAgent}
    """
    async def process_event(self, event):
        logger.info("Processing logic via Hot-Swap...")
        return {"status": "success", "data": "Handled by Hot-Reload Engine"}
`);

    const handleDeploy = async () => {
        setLoading(true);
        setStatus(null);
        try {
            const response = await fetch('/api/v1/dev/hotswap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent_id: selectedAgent,
                    code: code,
                    file_path: `agents/${selectedAgent}.py`
                })
            });
            const data = await response.json();
            if (data.status === 'success') {
                setStatus({ type: 'success', message: `Deployed ${selectedAgent} [${data.deployment_id}] Successfully!` });
            } else {
                throw new Error(data.error);
            }
        } catch (err) {
            setStatus({ type: 'error', message: `Deployment Failed: ${err.message}` });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card sx={{ height: '100%', bgcolor: '#002b36', color: '#839496', border: '1px solid #586e75' }}>
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                         <CodeIcon sx={{ mr: 1, color: '#268bd2' }} />
                         <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#eee' }}>Logic Forge (IDE)</Typography>
                    </Box>
                    <Select
                        value={selectedAgent}
                        onChange={(e) => setSelectedAgent(e.target.value)}
                        sx={{ bgcolor: '#073642', color: '#fff', height: 40, border: '1px solid #586e75' }}
                    >
                        <MenuItem value="scraper_agent_01">Scraper Agent</MenuItem>
                        <MenuItem value="analyst_agent_02">Analyst Agent</MenuItem>
                        <MenuItem value="trader_agent_05">Trader Agent</MenuItem>
                    </Select>
                </Box>
                
                {status && (
                    <Alert severity={status.type} sx={{ mb: 2, bgcolor: status.type === 'success' ? '#1b3a2e' : '#3d1c1c', color: '#eee' }}>
                        {status.message}
                    </Alert>
                )}
                
                <TextField
                    multiline
                    rows={18}
                    fullWidth
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    sx={{ 
                        fontFamily: "'Fira Code', monospace",
                        bgcolor: '#073642',
                        '& .MuiInputBase-input': { 
                            color: '#859900',
                            fontSize: '0.9rem',
                            lineHeight: 1.5
                        },
                        border: '1px solid #586e75'
                    }}
                />
                
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                    <Button 
                        variant="contained" 
                        sx={{ bgcolor: '#268bd2', '&:hover': { bgcolor: '#2aa198' } }}
                        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
                        onClick={handleDeploy}
                        disabled={loading}
                    >
                        Hot Deploy (Blue-Green)
                    </Button>
                    <Button 
                        variant="outlined" 
                        sx={{ color: '#b58900', borderColor: '#b58900' }}
                        startIcon={<PlayArrowIcon />}
                    >
                        Dry Run (Static Analysis)
                    </Button>
                </Box>
            </CardContent>
        </Card>
    );
};

export default AgentLogicEditor;
