import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Chip, Button, TextField, MenuItem, Box } from '@mui/material';
import MissionConfigModal from './MissionConfigModal';

// Mock data (would come from API /api/missions/templates)
const MOCK_TEMPLATES = [
    { id: "mission_001", name: "M&A Scout", sector: "Wealth", risk: "Medium", roi: "12%" },
    { id: "mission_002", name: "Crash Protocol", sector: "Security", risk: "High", roi: "N/A" },
    { id: "mission_003", name: "Sentiment Analysis", sector: "Intelligence", risk: "Low", roi: "8%" },
    { id: "mission_004", name: "Competitor Sabotage", sector: "Shadow", risk: "High", roi: "25%" },
    { id: "mission_005", name: "Portfolio Rebalancing", sector: "Wealth", risk: "Low", roi: "5%" },
];

const SECTORS = ["All", "Wealth", "Security", "Intelligence", "Shadow"];

const MissionLibrary = () => {
    const [templates, setTemplates] = useState(MOCK_TEMPLATES);
    const [filter, setFilter] = useState("All");
    const [selectedTemplate, setSelectedTemplate] = useState(null);

    const filteredTemplates = templates.filter(t => filter === "All" || t.sector === filter);

    const handleDeployClick = (template) => {
        setSelectedTemplate(template);
    };

    const handleCloseModal = () => {
        setSelectedTemplate(null);
    };

    const getRiskColor = (risk) => {
        switch(risk) {
            case 'High': return 'error';
            case 'Medium': return 'warning';
            default: return 'success';
        }
    };

    return (
        <Box sx={{ p: 2, height: '100%', overflow: 'auto' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h5" color="text.primary">Mission Library</Typography>
                <TextField 
                    select 
                    label="Sector Filter" 
                    value={filter} 
                    onChange={(e) => setFilter(e.target.value)}
                    size="small"
                    sx={{ width: 150 }}
                >
                    {SECTORS.map((s) => (
                        <MenuItem key={s} value={s}>{s}</MenuItem>
                    ))}
                </TextField>
            </Box>

            <Grid container spacing={2}>
                {filteredTemplates.map((template) => (
                    <Grid item xs={12} sm={6} md={4} key={template.id}>
                        <Card sx={{ 
                            height: '100%', 
                            display: 'flex', 
                            flexDirection: 'column', 
                            justifyContent: 'space-between',
                            transition: '0.3s',
                            '&:hover': { transform: 'translateY(-4px)', boxShadow: 4 }
                        }}>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>{template.name}</Typography>
                                <Typography variant="body2" color="text.secondary" paragraph>
                                    ID: {template.id}
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                                    <Chip label={template.sector} size="small" color="primary" variant="outlined" />
                                    <Chip label={`Risk: ${template.risk}`} size="small" color={getRiskColor(template.risk)} />
                                </Box>
                                <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                                    Est. ROI: {template.roi}
                                </Typography>
                            </CardContent>
                            <Box sx={{ p: 2, pt: 0 }}>
                                <Button 
                                    variant="contained" 
                                    fullWidth 
                                    onClick={() => handleDeployClick(template)}
                                >
                                    Configure & Deploy
                                </Button>
                            </Box>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            {selectedTemplate && (
                <MissionConfigModal 
                    open={!!selectedTemplate} 
                    onClose={handleCloseModal} 
                    template={selectedTemplate} 
                />
            )}
        </Box>
    );
};

export default MissionLibrary;
