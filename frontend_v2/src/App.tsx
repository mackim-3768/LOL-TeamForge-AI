import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/Layout/MainLayout';
import Home from './pages/Home';
import { Box } from '@mui/material';

// Placeholder Dashboard
const Dashboard = () => <Box sx={{ p: 4 }}>Dashboard (Work In Progress)</Box>;

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard/:summonerName" element={<Dashboard />} />
          {/* Add more routes here */}
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
