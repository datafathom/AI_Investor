import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { Box, Grid, Typography, Card, CardContent, Divider, Chip } from '@mui/material';
import RegimeLight from '../components/Charts/RegimeLight';
import SCMScore from '../components/Reporting/SCMScore';
import apiClient from '../services/apiClient';

const SentinelStrategyDashboard = () => {
    const [regimeData, setRegimeData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchRegime = async () => {
            try {
                const res = await apiClient.get('/risk/regime');
                if (res.status === 'success') {
                    setRegimeData(res.data);
                }
            } catch (err) {
                console.error("Failed to load sentinel data", err);
            } finally {
                setLoading(false);
            }
        };
        fetchRegime();
    }, []);

    return (
        <Box sx={{ p: 4, bgcolor: '#0a0e17', minHeight: '100vh', color: 'white' }}>
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', letterSpacing: 2 }}>
                SENTINEL: ADAPTIVE STRATEGY
            </Typography>
            <Divider sx={{ mb: 4, borderColor: 'rgba(255,255,255,0.1)' }} />

            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 4 }}>
                    <Card sx={{ bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.1)' }}>
                        <CardContent>
                            <Typography variant="h6" color="primary" gutterBottom>Market Regime</Typography>
                            <Box display="flex" justifyContent="center" py={2}>
                                {regimeData ? (
                                    <RegimeLight regime={regimeData.regime} trend={regimeData.price > regimeData.sma_200 ? 'POSITIVE' : 'NEGATIVE'} />
                                ) : (
                                    <Typography>Loading Regime...</Typography>
                                )}
                            </Box>
                            {regimeData && (
                                <Box mt={2}>
                                    <Typography variant="body2" sx={{ opacity: 0.7 }}>
                                        SMA 200: {regimeData.sma_200?.toFixed(2)}
                                    </Typography>
                                    <Typography variant="body2" sx={{ opacity: 0.7 }}>
                                        Current: {regimeData.price?.toFixed(2)}
                                    </Typography>
                                </Box>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                <Grid size={{ xs: 12, md: 8 }}>
                    <Card sx={{ bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.1)', height: '100%' }}>
                        <CardContent>
                            <Typography variant="h6" color="primary" gutterBottom>Adaptive Policy Logic</Typography>
                            <Typography variant="body1" sx={{ mb: 2 }}>
                                Strategy is automatically toggling based on the 200-day trend and volatility clusters.
                            </Typography>
                            <Box display="flex" gap={1} flexWrap="wrap">
                                <Chip label="Trend Following: ACTIVE" color="success" variant="outlined" />
                                <Chip label="Volatility Hedging: ON" color="warning" variant="outlined" />
                                <Chip label="Tail Risk: MONITORING" color="info" variant="outlined" />
                            </Box>
                            <Box mt={4} p={2} sx={{ bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 1 }}>
                                <Typography variant="caption" sx={{ fontStyle: 'italic', opacity: 0.6 }}>
                                    Current Policy: If Regime == BEAR, use Puts to hedge 40% of Delta. If BULL, maintain standard 1.2x beta.
                                </Typography>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
                
                <Grid size={{ xs: 12 }}>
                     <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>SCM Projection</Typography>
                     <SCMScore score={1.15} clewRate={0.084} yieldRate={0.115} />
                </Grid>
            </Grid>
        </Box>
    );
};

export default SentinelStrategyDashboard;
