import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useState } from 'react';
import Home from './pages/Home';
import SummonerDetail from './pages/SummonerDetail';
import TeamBuilder from './pages/TeamBuilder';
import SummonerRegistration from './pages/SummonerRegistration';
import AdminKeyModal from './components/AdminKeyModal';

function App() {
  const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);

  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            LoL Flex Analyst
          </Typography>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/register">Register</Button>
          <Button color="inherit" component={Link} to="/team-builder">Team Builder</Button>
          <Button color="inherit" onClick={() => setIsAdminModalOpen(true)}>Admin</Button>
        </Toolbar>
      </AppBar>
      <AdminKeyModal open={isAdminModalOpen} onClose={() => setIsAdminModalOpen(false)} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<SummonerRegistration />} />
        <Route path="/summoner/:name" element={<SummonerDetail />} />
        <Route path="/team-builder" element={<TeamBuilder />} />
      </Routes>
    </Router>
  );
}

export default App;
