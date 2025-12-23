import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<SummonerRegistration />} />
        <Route path="/summoner/:name" element={<SummonerDetail />} />
        <Route path="/team-builder" element={<TeamBuilder />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/fetch" element={<FetchData />} />
      </Routes>
    </Router>
  );
}

export default App;
