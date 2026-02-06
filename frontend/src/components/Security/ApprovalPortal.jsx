import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Button, List, ListItem, ListItemText, Box, Chip } from '@mui/material';
import FingerprintIcon from '@mui/icons-material/Fingerprint';

// Mock API Call
const approveRequest = async (id) => {
    // In real app: POST /api/approvals/verify
    console.log(`Approving ${id} with WebAuthn signature...`);
    return new Promise(resolve => setTimeout(resolve, 1000));
};

const ApprovalPortal = () => {
    const [pending, setPending] = useState([]);
    
    // Simulating polling
    useEffect(() => {
        const interval = setInterval(() => {
            // Mock data for demo
            if (Math.random() > 0.7 && pending.length < 2) {
                const newReq = {
                    id: `req_${Date.now()}`,
                    mission: "Mission #004 (Competitor Sabotage)",
                    action: "Deploy Exploit",
                    risk: "HIGH",
                    created_at: new Date().toLocaleTimeString()
                };
                setPending(prev => [...prev, newReq]);
            }
        }, 5000);
        return () => clearInterval(interval);
    }, [pending]);

    const handleApprove = async (id) => {
        // Trigger browser biometric prompt (mock)
        const credential = await window.confirm("Please verify identity with Biometrics (Mock)");
        if (credential) {
             await approveRequest(id);
             setPending(prev => prev.filter(r => r.id !== id));
        }
    };

    return (
        <Card sx={{ height: '100%', bgcolor: '#fdf6e3' }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <FingerprintIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6" color="primary">
                        Biometric Approval Gate
                    </Typography>
                </Box>
                
                {pending.length === 0 ? (
                    <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                        No pending approvals. Systems autonomous.
                    </Typography>
                ) : (
                    <List>
                        {pending.map((req) => (
                            <ListItem key={req.id} sx={{ bgcolor: 'rgba(220, 50, 47, 0.1)', mb: 1, borderRadius: 1 }}>
                                <ListItemText 
                                    primary={req.mission}
                                    secondary={`Action: ${req.action} | Time: ${req.created_at}`}
                                />
                                <Chip label={req.risk} color="error" size="small" sx={{ mr: 1 }} />
                                <Button 
                                    variant="contained" 
                                    color="secondary" 
                                    size="small"
                                    startIcon={<FingerprintIcon />}
                                    onClick={() => handleApprove(req.id)}
                                >
                                    Sign
                                </Button>
                            </ListItem>
                        ))}
                    </List>
                )}
            </CardContent>
        </Card>
    );
};

export default ApprovalPortal;
