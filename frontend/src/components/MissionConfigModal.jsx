import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Slider, Typography, TextField, Box, Switch, FormControlLabel } from '@mui/material';

const MissionConfigModal = ({ open, onClose, template }) => {
    const [budget, setBudget] = useState(500);
    const [ttl, setTtl] = useState(600);
    const [approvalMode, setApprovalMode] = useState(false);

    const handleDeploy = () => {
        // In real app: POST /api/missions/deploy
        console.log("Deploying mission:", {
            template_id: template.id,
            config: { budget, ttl, approvalMode }
        });
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>Configure Mission: {template?.name}</DialogTitle>
            <DialogContent>
                <Box sx={{ mt: 2 }}>
                    <Typography gutterBottom>Budget Limit (Credits)</Typography>
                    <Slider
                        value={budget}
                        onChange={(_, val) => setBudget(val)}
                        valueLabelDisplay="auto"
                        step={50}
                        min={100}
                        max={2000}
                    />
                    <Typography variant="caption" color="text.secondary">
                        Max spend for this mission instance.
                    </Typography>
                </Box>

                <Box sx={{ mt: 3 }}>
                    <Typography gutterBottom>Time-To-Live (Seconds)</Typography>
                    <Slider
                        value={ttl}
                        onChange={(_, val) => setTtl(val)}
                        valueLabelDisplay="auto"
                        step={60}
                        min={60}
                        max={3600}
                    />
                </Box>

                <Box sx={{ mt: 3 }}>
                     <FormControlLabel
                        control={<Switch checked={approvalMode} onChange={(e) => setApprovalMode(e.target.checked)} />}
                        label="Require Human Approval for Tool Calls?"
                    />
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleDeploy} variant="contained" color="primary">
                    Launch Mission
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default MissionConfigModal;
