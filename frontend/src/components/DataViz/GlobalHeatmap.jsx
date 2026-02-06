import React from 'react';
import { Card, CardContent, Typography, Box, Tooltip } from '@mui/material';

// Dummy data
const generateGrid = () => {
    return Array(100).fill(0).map((_, i) => ({
        id: i,
        status: Math.random() > 0.8 ? 'running' : (Math.random() > 0.5 ? 'success' : 'idle'),
        load: Math.random()
    }));
};

const GlobalHeatmap = ({ data }) => {
    const gridData = data || generateGrid();

    const getColor = (status) => {
        switch(status) {
            case 'running': return '#268bd2'; // Blue
            case 'success': return '#859900'; // Green
            case 'failed': return '#dc322f'; // Red
            default: return '#eee8d5'; // Grey/Idle
        }
    };

    return (
        <Card sx={{ height: '100%', bgcolor: '#fdf6e3' }}>
            <CardContent>
                <Typography variant="h6" gutterBottom color="primary">
                    Global Mission Heatmap
                </Typography>
                <Box sx={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(10, 1fr)', 
                    gap: 0.5,
                    aspectRatio: '1/1'
                }}>
                    {gridData.map((cell) => (
                        <Tooltip key={cell.id} title={`Mission #${cell.id} - ${cell.status.toUpperCase()}`}>
                            <Box sx={{
                                width: '100%',
                                paddingTop: '100%', // Square aspect ratio
                                backgroundColor: getColor(cell.status),
                                borderRadius: '2px',
                                position: 'relative',
                                cursor: 'pointer',
                                transition: 'transform 0.1s',
                                '&:hover': {
                                    transform: 'scale(1.1)',
                                    zIndex: 1,
                                    border: '1px solid #586e75'
                                }
                            }} />
                        </Tooltip>
                    ))}
                </Box>
            </CardContent>
        </Card>
    );
};

export default GlobalHeatmap;
