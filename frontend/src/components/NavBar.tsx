import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link } from 'react-router-dom';

const NavBar: React.FC = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: '#5383E8' }}>
      <Toolbar>
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'white', fontWeight: 'bold' }}>
          LoL Flex Analyst
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" component={Link} to="/admin">Admin</Button>
          <Button color="inherit" component={Link} to="/register">Summoner Registration</Button>
          <Button color="inherit" component={Link} to="/team-builder">Combination</Button>
          <Button color="inherit" component={Link} to="/fetch">Fetch Data</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
