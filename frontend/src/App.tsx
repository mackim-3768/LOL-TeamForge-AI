import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, CssBaseline } from '@mui/material';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import SummonerRegistration from './pages/SummonerRegistration';
import SummonerDetail from './pages/SummonerDetail';
import TeamBuilder from './pages/TeamBuilder';
import Admin from './pages/Admin';
import FetchData from './pages/FetchData';

function App() {
  return (
    <Router>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', width: '100%' }}>
        <NavBar />
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', width: '100%' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<SummonerRegistration />} />
            <Route path="/summoner/:name" element={<SummonerDetail />} />
            <Route path="/team-builder" element={<TeamBuilder />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/fetch" element={<FetchData />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
