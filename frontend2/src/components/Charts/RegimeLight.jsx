import React from 'react';
import { Box, Typography, Tooltip, Paper } from '@mui/material';
import ShieldIcon from '@mui/icons-material/Shield';
import BoltIcon from '@mui/icons-material/Bolt';
import WarningIcon from '@mui/icons-material/Warning';
import apiClient from '../../services/apiClient';

const RegimeLight = ({ regime: propRegime, trend: propTrend }) => {
  const [regime, setRegime] = React.useState(propRegime || 'BULL');
  const [trend, setTrend] = React.useState(propTrend || 'POSITIVE');
  const [loading, setLoading] = React.useState(!propRegime);

  React.useEffect(() => {
    if (propRegime) {
        setRegime(propRegime);
        setTrend(propTrend || 'POSITIVE');
        return;
    }

    const fetchRegime = async () => {
        try {
            const response = await apiClient.get('/risk/regime');
            if (response.status === 'success' && response.data) {
                setRegime(response.data.regime);
                // Trend could be derived or returned by service
                setTrend(response.data.price > response.data.sma_200 ? 'POSITIVE' : 'NEGATIVE');
            }
        } catch (err) {
            console.error("Regime fetch failed:", err);
        } finally {
            setLoading(false);
        }
    };
    fetchRegime();
  }, [propRegime, propTrend]);
  const getRegimeColor = (r) => {
    switch(r) {
      case 'BULL': return '#4caf50';
      case 'BEAR': return '#f44336';
      case 'TRANSITION': return '#ff9800';
      default: return '#9e9e9e';
    }
  };

  const currentStatus = {
    BULL: { label: 'RISK ON - GROWTH MODE', icon: <BoltIcon sx={{ color: 'white' }} />, desc: 'Price above 200 SMA. Conditions favorable for Beta.' },
    BEAR: { label: 'RISK OFF - DEFENSE ACTIVE', icon: <ShieldIcon sx={{ color: 'white' }} />, desc: 'Price below 200 SMA. Defensive protocol triggered.' },
    TRANSITION: { label: 'TRANSITIONING - CAUTION', icon: <WarningIcon sx={{ color: 'white' }} />, desc: 'Market showing high volatility during trend shift.' }
  };

  const status = currentStatus[regime] || currentStatus['BULL'];

  return (
    <Paper sx={{ 
      p: 2, 
      display: 'flex', 
      alignItems: 'center', 
      background: 'rgba(0,0,0,0.2)', 
      border: `2px solid ${getRegimeColor(regime)}`,
      borderRadius: '12px'
    }}>
      <Box sx={{ 
        width: 40, 
        height: 40, 
        borderRadius: '50%', 
        bgcolor: getRegimeColor(regime), 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center',
        boxShadow: `0 0 15px ${getRegimeColor(regime)}`,
        mr: 2
      }}>
        {status.icon}
      </Box>
      
      <Box>
        <Typography variant="caption" sx={{ opacity: 0.7, letterSpacing: 1 }}>SYSTEM REGIME</Typography>
        <Tooltip title={status.desc}>
          <Typography variant="body1" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
            {status.label}
          </Typography>
        </Tooltip>
      </Box>
      
      <Box sx={{ ml: 'auto', textAlign: 'right' }}>
        <Typography variant="caption" display="block">TREND</Typography>
        <Typography variant="body2" color={trend === 'POSITIVE' ? 'success.main' : 'error.main'}>
          {trend}
        </Typography>
      </Box>
    </Paper>
  );
};

export default RegimeLight;
