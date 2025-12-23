import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import SummonerList from './pages/SummonerList';
import SummonerDetail from './pages/SummonerDetail';
import TeamBuilder from './pages/TeamBuilder';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            LoL Flex Analyst
          </Typography>
          <Button color="inherit" component={Link} to="/">Summoners</Button>
          <Button color="inherit" component={Link} to="/team-builder">Team Builder</Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/" element={<SummonerList />} />
        <Route path="/summoner/:name" element={<SummonerDetail />} />
        <Route path="/team-builder" element={<TeamBuilder />} />
      </Routes>
    </Router>
  );
}

export default App;
