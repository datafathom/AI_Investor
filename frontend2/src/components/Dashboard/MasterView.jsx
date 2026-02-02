import React, { useState } from 'react';
import { Box, Grid, Typography, Paper, Tab, Tabs, Button, IconButton } from '@mui/material';
import SCMScore from '../Reporting/SCMScore';
import RegimeLight from '../Charts/RegimeLight';
import DeepDive from '../Research/DeepDive';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import PublicIcon from '@mui/icons-material/Public';
import SecurityIcon from '@mui/icons-material/Security';
import HubIcon from '@mui/icons-material/Hub';

const MasterView = () => {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <Box sx={{ p: 4, bgcolor: '#0a0e14', minHeight: '100vh', color: 'white' }}>
      <Box display="flex" justifyContent="space-between" alignItems="flex-end" mb={4}>
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 1, background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Ultimate Wealth Orchestrator
          </Typography>
          <Typography variant="subtitle1" sx={{ opacity: 0.6 }}>SYSTEM STATUS: ALL ENGINES OPERATIONAL | EPOCH X COMPLETE</Typography>
        </Box>
        <Button variant="outlined" color="primary" startIcon={<HubIcon />}>NEO4J SUPER GRAPH</Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <SCMScore />
        </Grid>
        <Grid item xs={12} md={6}>
          <Box sx={{ bgcolor: 'rgba(255,255,255,0.03)', borderRadius: 2, p: 2, height: '100%', border: '1px solid rgba(255,255,255,0.05)' }}>
             <Typography variant="h6" gutterBottom>Global Unified exposure</Typography>
             {/* Map or Graph placeholder */}
             <Box sx={{ height: 250, bgcolor: 'rgba(0,0,0,0.2)', borderRadius: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <PublicIcon sx={{ fontSize: 100, opacity: 0.1 }} />
                <Typography variant="caption" sx={{ position: 'absolute', opacity: 0.5 }}>NEO4J CROSS-DOMAIN KNOWLEDGE GRAPH ACTIVE</Typography>
             </Box>
             <Box mt={2}>
               <RegimeLight />
             </Box>
          </Box>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, bgcolor: 'rgba(33, 150, 243, 0.1)', border: '1px solid #2196f3', height: '100%' }}>
            <Typography variant="subtitle2" color="primary" gutterBottom>EVENT STREAM</Typography>
            <Box sx={{ fontSize: '0.8rem', fontFamily: 'monospace' }}>
              <Typography variant="inherit" display="block" color="success.main">[OK] TAX_ENGINE: Estate Plan Audited</Typography>
              <Typography variant="inherit" display="block" sx={{ opacity: 0.7 }}>[INFO] KAFKA: Taiwan_Conflict signal received</Typography>
              <Typography variant="inherit" display="block" color="warning.main">[WARN] RISK_MANAGER: Beta Reduction in Progress</Typography>
              <Typography variant="inherit" display="block" color="primary.main">[OK] SFO_SVC: Breakeven analysis verified</Typography>
              <Typography variant="inherit" display="block" sx={{ opacity: 0.4 }}>...</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
              <Tab icon={<BusinessCenterIcon />} label="Fundamental Diligence" />
              <Tab icon={<SecurityIcon />} label="Wealth Protection" />
              <Tab icon={<PublicIcon />} label="Geopolitical Reflexivity" />
            </Tabs>
          </Box>
          <Box sx={{ py: 3 }}>
            {activeTab === 0 && <DeepDive />}
            {activeTab === 1 && <Typography variant="h6">Wealth Protection Logic (APT/SWR/Insurance) integration visible here.</Typography>}
            {activeTab === 2 && <Typography variant="h6">Geopolitical Reflexivity (Michael Green Simulator) integration visible here.</Typography>}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MasterView;
