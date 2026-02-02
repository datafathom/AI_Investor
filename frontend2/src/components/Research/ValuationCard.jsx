import React from 'react';
import { Card, CardContent, Typography, Box, Divider, Stack } from '@mui/material';

const ValuationCard = ({ fairValue = 185.20, price = 154.00, upside = 20.2 }) => {
  return (
    <Card sx={{ bgcolor: 'background.paper', borderLeft: '6px solid #4caf50' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Intrinsic Value (DCF)</Typography>
        <Box display="flex" justifyContent="space-between" alignItems="center" my={2}>
          <Box>
            <Typography variant="caption" sx={{ opacity: 0.7 }}>ESTIMATED FAIR VALUE</Typography>
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>${fairValue.toFixed(2)}</Typography>
          </Box>
          <Box textAlign="right">
            <Typography variant="caption" sx={{ opacity: 0.7 }}>CURRENT PRICE</Typography>
            <Typography variant="h4" color="text.secondary">${price.toFixed(2)}</Typography>
          </Box>
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        <Stack spacing={1}>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2">Potential Upside</Typography>
            <Typography variant="body2" color="success.main" sx={{ fontWeight: 'bold' }}>+{upside}%</Typography>
          </Box>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2">WACC (Discount Rate)</Typography>
            <Typography variant="body2">9.0%</Typography>
          </Box>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2">Terminal Growth</Typography>
            <Typography variant="body2">2.5%</Typography>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ValuationCard;
