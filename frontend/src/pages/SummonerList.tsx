import React, { useState, useEffect } from 'react';
import { api } from '../api';
import type { Summoner } from '../api';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Paper } from '@mui/material';

const SummonerList: React.FC = () => {
  const [summoners, setSummoners] = useState<Summoner[]>([]);
  const [newName, setNewName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadSummoners();
  }, []);

  const loadSummoners = async () => {
    try {
      const response = await api.getSummoners();
      setSummoners(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRegister = async () => {
    if (!newName) return;
    setLoading(true);
    setError('');
    try {
      await api.registerSummoner(newName);
      setNewName('');
      loadSummoners();
    } catch (err: any) {
      setError('Failed to register (Likely not found or invalid key)');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>Summoner Registry</Typography>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <TextField 
          label="Summoner Name" 
          value={newName} 
          onChange={(e) => setNewName(e.target.value)} 
          fullWidth
        />
        <Button variant="contained" onClick={handleRegister} disabled={loading}>
          {loading ? 'Adding...' : 'Add'}
        </Button>
      </div>
      {error && <Typography color="error">{error}</Typography>}
      <Paper>
        <List>
          {summoners.map((s) => (
            <ListItem key={s.id} component="a" href={`/summoner/${s.name}`}>
              <ListItemText primary={s.name} secondary={`Level: ${s.level}`} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
};

export default SummonerList;
