import React, { useState } from 'react';
import { Card, CardContent, Typography, Box, Slider, Stack, Button, Divider } from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import FlightIcon from '@mui/icons-material/Flight';
import PersonIcon from '@mui/icons-material/Person';
import HomeIcon from '@mui/icons-material/Home';

const InflationBasket = ({ onSave }) => {
  const [basket, setBasket] = useState({
    tuition: 7,
    travel: 12,
    staff: 5,
    realEstate: 8
  });

  const handleChange = (name) => (event, newValue) => {
    setBasket({ ...basket, [name]: newValue });
  };

  return (
    <Card sx={{ bgcolor: 'background.paper', borderRadius: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Personal Inflation Basket (CLEW)</Typography>
        <Typography variant="body2" sx={{ mb: 3, opacity: 0.7 }}>
          Adjust the annual price increases for your specific lifestyle components to calculate your SCM baseline.
        </Typography>
        
        <Stack spacing={3}>
          <Box>
            <Box display="flex" alignItems="center" mb={1}>
              <SchoolIcon fontSize="small" sx={{ mr: 1 }} />
              <Typography variant="body2">Ivy League / Private Tuition</Typography>
              <Typography variant="body2" sx={{ ml: 'auto', fontWeight: 'bold' }}>{basket.tuition}%</Typography>
            </Box>
            <Slider value={basket.tuition} onChange={handleChange('tuition')} min={0} max={20} />
          </Box>

          <Box>
            <Box display="flex" alignItems="center" mb={1}>
              <FlightIcon fontSize="small" sx={{ mr: 1 }} />
              <Typography variant="body2">Luxury Travel & Concierge</Typography>
              <Typography variant="body2" sx={{ ml: 'auto', fontWeight: 'bold' }}>{basket.travel}%</Typography>
            </Box>
            <Slider value={basket.travel} onChange={handleChange('travel')} min={0} max={30} />
          </Box>

          <Box>
            <Box display="flex" alignItems="center" mb={1}>
              <PersonIcon fontSize="small" sx={{ mr: 1 }} />
              <Typography variant="body2">Private Staff & Security</Typography>
              <Typography variant="body2" sx={{ ml: 'auto', fontWeight: 'bold' }}>{basket.staff}%</Typography>
            </Box>
            <Slider value={basket.staff} onChange={handleChange('staff')} min={0} max={15} />
          </Box>

          <Box>
            <Box display="flex" alignItems="center" mb={1}>
              <HomeIcon fontSize="small" sx={{ mr: 1 }} />
              <Typography variant="body2">Prime Real Estate Ops</Typography>
              <Typography variant="body2" sx={{ ml: 'auto', fontWeight: 'bold' }}>{basket.realEstate}%</Typography>
            </Box>
            <Slider value={basket.realEstate} onChange={handleChange('realEstate')} min={0} max={20} />
          </Box>
        </Stack>

        <Divider sx={{ my: 3 }} />
        
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="caption" sx={{ opacity: 0.6 }}>WEIGHTED CLEW RATE</Typography>
            <Typography variant="h5" color="secondary" sx={{ fontWeight: 'bold' }}>
              {(Object.values(basket).reduce((a, b) => a + b, 0) / 4).toFixed(1)}%
            </Typography>
          </Box>
          <Button variant="contained" onClick={() => onSave(basket)}>Update Baseline</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default InflationBasket;
