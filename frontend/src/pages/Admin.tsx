import React, { useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import AdminKeyModal from '../components/AdminKeyModal';

const Admin: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Admin Dashboard</Typography>

      <Box sx={{ mt: 2 }}>
        <Typography variant="h6">Configuration</Typography>
        <Typography variant="body1" paragraph>
          Manage application settings and API keys.
        </Typography>
        <Button variant="contained" onClick={() => setIsModalOpen(true)}>
          Update Riot API Key
        </Button>
      </Box>

      <AdminKeyModal open={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </Container>
  );
};

export default Admin;
