import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Grid, Divider, Chip, CircularProgress } from '@mui/material';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SearchIcon from '@mui/icons-material/Search';

const DeepDive = () => {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  const handleSearch = async () => {
    if (!ticker) return;
    setLoading(true);
    setReport(null);
    try {
      // : Real AI Research Call
      const response = await apiClient.post('/research/company-research', {
        user_id: 'default_user', // In real app, get from auth context
        symbol: ticker.toUpperCase(),
        title: `${ticker.toUpperCase()} Deep Dive`
      });

      if (response.success && response.data) {
        const rData = response.data.data; // Nested data from ResearchReport
        setReport({
          ticker: ticker.toUpperCase(),
          moat: rData.moat_score >= 8 ? 'WIDE' : rData.moat_score >= 5 ? 'NARROW' : 'NONE',
          moatScore: rData.moat_score,
          intrinsicValue: rData.fair_value || 0,
          price: rData.current_price || 0,
          sentiment: rData.moat_score > 6 ? 'Optimistic' : 'Cautionary',
          risks: rData.risk_summary ? [rData.risk_summary.substring(0, 50) + "..."] : ['Manual Review Required'],
          insiderBuying: rData.insider_signal || 'N/A'
        });
      }
    } catch (err) {
      console.error("Research failed:", err);
      // Fallback or error state
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3, display: 'flex', gap: 2 }}>
        <TextField 
          label="Enter Stock Ticker" 
          value={ticker} 
          onChange={(e) => setTicker(e.target.value)}
          size="small"
          sx={{ flexGrow: 1 }}
        />
        <Button 
          variant="contained" 
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
          onClick={handleSearch}
          disabled={!ticker || loading}
        >
          Generate Deep Dive
        </Button>
      </Paper>

      {report && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2, textAlign: 'center', height: '100%', borderTop: '4px solid #4caf50' }}>
              <Typography variant="caption">INTRINSIC VALUE</Typography>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>${report.intrinsicValue}</Typography>
              <Chip 
                label={`${(((report.intrinsicValue - report.price) / report.intrinsicValue) * 100).toFixed(1)}% Margin of Safety`} 
                color="success" 
                size="small" 
                sx={{ mt: 1 }}
              />
            </Paper>
          </Grid>
          
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2, textAlign: 'center', height: '100%', borderTop: '4px solid #2196f3' }}>
              <Typography variant="caption">ECONOMIC MOAT</Typography>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{report.moat}</Typography>
              <Typography variant="body2" sx={{ mt: 1, color: 'primary.main' }}>Stable Gross Margins</Typography>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2, textAlign: 'center', height: '100%', borderTop: '4px solid #9c27b0' }}>
              <Typography variant="caption">INSIDER SIGNAL</Typography>
              <Typography variant="h4" sx={{ fontWeight: 'bold' }}>BULLISH</Typography>
              <Typography variant="body2" sx={{ mt: 1, color: 'secondary.main' }}>{report.insiderBuying}</Typography>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>10-K Risk Factor Summary (AI Generated)</Typography>
              <Divider sx={{ mb: 2 }} />
              <Box display="flex" flexWrap="wrap" gap={1}>
                {report.risks.map((risk, i) => (
                  <Chip key={i} label={risk} variant="outlined" color="warning" />
                ))}
              </Box>
              <Typography variant="body2" sx={{ mt: 2, opacity: 0.8, fontStyle: 'italic' }}>
                "Management tone indicated high confidence in capital expenditure for AI infrastructure while remaining cautious on consumer credit cycles..."
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default DeepDive;
