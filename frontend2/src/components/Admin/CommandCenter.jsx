import React, { useState } from 'react';
import { Box, Paper, Typography, Button, Grid, Chip, Switch, FormControlLabel, Divider } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

const CommandCenter = () => {
  const [running, setRunning] = useState(true);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Ultimate AI Orchestrator Command Center</Typography>
      <Divider sx={{ mb: 4 }} />

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">System Core Enforced Constraints</Typography>
              <Chip label={running ? "ACTIVE" : "PAUSED"} color={running ? "success" : "default"} />
            </Box>
            
            <Box sx={{ '& > *': { mb: 2 } }}>
              <FormControlLabel control={<Switch defaultChecked />} label="Survival Constraint (VAR < 25%)" />
              <FormControlLabel control={<Switch defaultChecked />} label="Social Class Maintenance Priority (ROL Maximize)" />
              <FormControlLabel control={<Switch defaultChecked />} label="Automated Bear Market Defenses (200 SMA)" />
              <FormControlLabel control={<Switch />} label="Strict Tax Optimization (Asset Segregation)" />
            </Box>
            
            <Box mt={3} display="flex" gap={2}>
              <Button variant="contained" color="error" startIcon={<StopIcon />} onClick={() => setRunning(false)}>Emergency Halt</Button>
              <Button variant="contained" color="success" startIcon={<PlayArrowIcon />} onClick={() => setRunning(true)}>Resume Auto-Trading</Button>
              <Button variant="outlined" startIcon={<RestartAltIcon />}>Rebalance Unified Graph</Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, bgcolor: '#001e3c', color: 'white' }}>
            <Typography variant="h6" color="primary" gutterBottom>Microservice Health (200 Phases)</Typography>
            <Box sx={{ mt: 2 }}>
                <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="caption">Neo4j SuperGraph</Typography>
                    <Typography variant="caption" color="success.main">ONLINE</Typography>
                </Box>
                <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="caption">Kafka Reflexivity Bus</Typography>
                    <Typography variant="caption" color="success.main">ONLINE</Typography>
                </Box>
                <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="caption">Postgres Hybrid State</Typography>
                    <Typography variant="caption" color="success.main">ONLINE</Typography>
                </Box>
                <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="caption">SCM Simulator</Typography>
                    <Typography variant="caption" color="success.main">ONLINE</Typography>
                </Box>
                <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="caption">Beta Reducer</Typography>
                    <Typography variant="caption" color="success.main">READY</Typography>
                </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CommandCenter;
