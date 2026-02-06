import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Chip, Box, IconButton, CircularProgress } from '@mui/material';
import ReplayIcon from '@mui/icons-material/Replay';
import HistoryIcon from '@mui/icons-material/History';

const HistoryReplay = () => {
    const [traces, setTraces] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTraces = async () => {
            try {
                const response = await fetch('/api/v1/dev/traces');
                const data = await response.json();
                if (data.success) {
                    setTraces(data.data);
                }
            } catch (err) {
                console.error("Failed to fetch traces:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchTraces();
    }, []);

    return (
         <Card sx={{ height: '100%', bgcolor: '#073642', color: '#93a1a1', border: '1px solid #586e75' }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <HistoryIcon sx={{ mr: 1, color: '#d33682' }} />
                    <Typography variant="h6" sx={{ color: '#eee', fontWeight: 'bold' }}>Intelligence Replay</Typography>
                </Box>
                
                {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                        <CircularProgress color="secondary" />
                    </Box>
                ) : (
                    <List>
                        {traces.map((trace) => (
                            <ListItem 
                                key={trace.id}
                                secondaryAction={
                                    <IconButton edge="end" sx={{ color: '#268bd2' }} title="Replay Trace">
                                        <ReplayIcon />
                                    </IconButton>
                                }
                                sx={{ borderBottom: '1px solid #586e75', '&:hover': { bgcolor: '#002b36' } }}
                            >
                                <ListItemText 
                                    primary={trace.input}
                                    secondary={`ID: ${trace.id} | ${trace.agent} | ${trace.error || 'SUCCESS'}`}
                                    primaryTypographyProps={{ color: '#eee', fontWeight: 'medium' }}
                                    secondaryTypographyProps={{ color: '#839496', fontSize: '0.8rem' }}
                                />
                                <Chip 
                                    label={trace.status} 
                                    sx={{ 
                                        bgcolor: trace.status === 'SUCCESS' ? '#85990022' : '#dc322f22',
                                        color: trace.status === 'SUCCESS' ? '#859900' : '#dc322f',
                                        borderColor: trace.status === 'SUCCESS' ? '#859900' : '#dc322f',
                                        fontWeight: 'bold'
                                    }}
                                    variant="outlined"
                                    size="small" 
                                />
                            </ListItem>
                        ))}
                    </List>
                )}
            </CardContent>
        </Card>
    );
};

export default HistoryReplay;
