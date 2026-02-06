import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Button, Slider, Box, Switch, FormControlLabel } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const ColdHavenConfig = () => {
    const [heartbeatInterval, setHeartbeatInterval] = useState(60);
    const [panicActive, setPanicActive] = useState(false);

    useEffect(() => {
        // Send heartbeat every 10s if page is open
        const interval = setInterval(() => {
            if (!panicActive) {
                console.log("Sending heartbeat...");
                // fetch('/api/approvals/system/heartbeat', { method: 'POST' });
            }
        }, 10000);
        return () => clearInterval(interval);
    }, [panicActive]);

    const handlePanic = () => {
        if (window.confirm("ARE YOU SURE? THIS WILL TERMINATE ALL AGENTS AND SWEEP ASSETS.")) {
            setPanicActive(true);
            // fetch('/api/approvals/panic', { method: 'POST', body: JSON.stringify({ reason: "MANUAL", confirmation: "I_AM_SURE" }) });
        }
    };

    return (
        <Card sx={{ height: '100%', bgcolor: panicActive ? '#dc322f' : '#073642', color: '#fff' }}>
            <CardContent>
                 <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ErrorOutlineIcon color="error" sx={{ mr: 1 }} />
                    <Typography variant="h6">
                        Cold-Haven Protocols
                    </Typography>
                </Box>

                {panicActive ? (
                    <Box sx={{ textAlign: 'center', mt: 4 }}>
                        <Typography variant="h4" fontWeight="bold">SYSTEM LOCKED</Typography>
                        <Typography variant="body1">Evacuation in progress...</Typography>
                        <Button 
                            variant="outlined" 
                            sx={{ mt: 2, color: '#fff', borderColor: '#fff' }}
                            onClick={() => setPanicActive(false)}
                        >
                            Enter Recovery Key
                        </Button>
                    </Box>
                ) : (
                    <>
                        <Box sx={{ mb: 4 }}>
                            <Typography gutterBottom>Dead Man's Switch (Mins)</Typography>
                            <Slider
                                value={heartbeatInterval}
                                onChange={(_, val) => setHeartbeatInterval(val)}
                                valueLabelDisplay="auto"
                                min={1}
                                max={120}
                                sx={{ color: '#cb4b16' }}
                            />
                            <Typography variant="caption" sx={{ color: '#93a1a1' }}>
                                Auto-Panic if offline for {heartbeatInterval} mins.
                            </Typography>
                        </Box>

                        <Button 
                            variant="contained" 
                            color="error" 
                            fullWidth 
                            size="large"
                            onClick={handlePanic}
                            sx={{ height: 60, fontWeight: 'bold' }}
                        >
                            INITIATE PANIC PROTOCOL
                        </Button>
                    </>
                )}
            </CardContent>
        </Card>
    );
};

export default ColdHavenConfig;
