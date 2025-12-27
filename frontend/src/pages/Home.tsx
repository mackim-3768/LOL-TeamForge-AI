import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Box, Autocomplete, Button, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import type { Summoner } from '../api';

const Home: React.FC = () => {
  const [summoners, setSummoners] = useState<Summoner[]>([]);
  const [searchValue, setSearchValue] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Prefetch summoners for autocomplete
    api.getSummoners().then(res => setSummoners(res.data)).catch(console.error);
  }, []);

  const handleSearch = () => {
    if (searchValue) {
      navigate(`/summoner/${searchValue}`);
    }
  };

  return (
    <Box
      sx={{
        backgroundColor: '#5383E8',
        minHeight: 'calc(100vh - 64px)',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white'
      }}
    >
      <Container maxWidth="md" sx={{ textAlign: 'center' }}>
        <Typography variant="h2" fontWeight="bold" gutterBottom>
          LoL Flex Analyst
        </Typography>
        <Paper
          component="form"
          sx={{
            p: '2px 4px',
            display: 'flex',
            alignItems: 'center',
            width: '100%',
            borderRadius: '50px',
            mt: 4
          }}
          onSubmit={(e) => { e.preventDefault(); handleSearch(); }}
        >
          <Autocomplete
            freeSolo
            options={summoners.map((option) => option.name)}
            fullWidth
            value={searchValue}
            onChange={(_event, newValue) => setSearchValue(newValue)}
            onInputChange={(_event, newInputValue) => setSearchValue(newInputValue)}
            renderInput={(params) => (
              <TextField
                {...params}
                placeholder="Search Summoner Name..."
                variant="standard"
                InputProps={{ ...params.InputProps, disableUnderline: true }}
                sx={{ ml: 3, flex: 1 }}
              />
            )}
          />
          <Button
            type="submit"
            variant="contained"
            sx={{ borderRadius: '50px', m: 1, backgroundColor: '#5383E8' }}
          >
            Search
          </Button>
        </Paper>
      </Container>
    </Box>
  );
};

export default Home;
