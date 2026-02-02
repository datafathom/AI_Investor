import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, LinearProgress, Tooltip } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import InfoIcon from '@mui/icons-material/Info';

const SCMScore = ({ score = 1.2, clewRate = 0.08, yieldRate = 0.12 }) => {
  const isHealthy = score >= 1.0;
  
  return (
    <Card sx={{ minWidth: 275, background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" color="primary">SCM Score (Return on Lifestyle)</Typography>
          <Tooltip title="Social Class Maintenance Score. >1.0 means your portfolio growth exceeds your custom lifestyle inflation (CLEW).">
            <InfoIcon fontSize="small" sx={{ opacity: 0.6 }} />
          </Tooltip>
        </Box>
        
        <Box textAlign="center" py={3}>
          <Typography variant="h2" color={isHealthy ? "success.main" : "error.main"} sx={{ fontWeight: 'bold' }}>
            {score.toFixed(2)}
          </Typography>
          <Typography variant="subtitle1" sx={{ opacity: 0.8 }}>
            {isHealthy ? "SOCIAL CLASS EXPANDING" : "SOCIAL CLASS DILUTING"}
          </Typography>
        </Box>
        
        <Box mt={2}>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <Typography variant="body2">CLEW Inflation (Lifestyle)</Typography>
            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{(clewRate * 100).toFixed(1)}%</Typography>
          </Box>
          <LinearProgress variant="determinate" value={clewRate * 100 * 5} color="error" sx={{ height: 8, borderRadius: 4 }} />
          
          <Box display="flex" justifyContent="space-between" mt={2} mb={1}>
            <Typography variant="body2">Portfolio Yield (Realized)</Typography>
            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{(yieldRate * 100).toFixed(1)}%</Typography>
          </Box>
          <LinearProgress variant="determinate" value={yieldRate * 100 * 5} color="success" sx={{ height: 8, borderRadius: 4 }} />
        </Box>
        
        <Box display="flex" alignItems="center" mt={3} p={1} sx={{ bgcolor: isHealthy ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)', borderRadius: 1 }}>
          {isHealthy ? <TrendingUpIcon color="success" sx={{ mr: 1 }} /> : <TrendingDownIcon color="error" sx={{ mr: 1 }} />}
          <Typography variant="caption">
            {isHealthy 
              ? `You are currently outperforming personal inflation by ${(yieldRate - clewRate).toFixed(2) * 100}% points.`
              : `Lifestyle burn is eroding purchasing power. Recommendation: Reduce Beta or Increase Yield.`}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SCMScore;
