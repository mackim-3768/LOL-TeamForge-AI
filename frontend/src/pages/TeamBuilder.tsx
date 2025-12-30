import React, { useState, useEffect } from 'react';
import { api } from '../api';
import type { Summoner } from '../api';
import { Container, Typography, Button, FormControl, InputLabel, Select, MenuItem, Chip, Box, Card, CardContent } from '@mui/material';
import MarkdownPreview from '../components/MarkdownPreview';
import type { SelectChangeEvent } from '@mui/material';

const TeamBuilder: React.FC = () => {
  const [allSummoners, setAllSummoners] = useState<Summoner[]>([]);
  const [selectedSummoners, setSelectedSummoners] = useState<string[]>([]);
  const [recommendation, setRecommendation] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getSummoners().then(res => setAllSummoners(res.data));
  }, []);

  const handleSelect = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;

    // value can be string or string[]
    const valueArray = typeof value === 'string' ? value.split(',') : value;

    // Limit to 5
    if (valueArray.length <= 5) {
      setSelectedSummoners(valueArray);
    }
  };

  const getRecommendation = async () => {
    setLoading(true);
    try {
      const res = await api.recommendComp(selectedSummoners);
      setRecommendation(res.data.analysis);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>Team Composition Builder</Typography>
      <Typography variant="body1" gutterBottom>Select up to 5 summoners to get an AI recommendation.</Typography>
      
      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel>Summoners</InputLabel>
        <Select
          multiple
          value={selectedSummoners}
          onChange={handleSelect}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
        >
          {allSummoners.map((s) => (
            <MenuItem key={s.id} value={s.name}>
              {s.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      
      <Button 
        variant="contained" 
        color="primary" 
        onClick={getRecommendation}
        disabled={selectedSummoners.length === 0 || loading}
      >
        {loading ? 'Analyzing...' : 'Get Recommendation'}
      </Button>

      {recommendation && (
        <Card style={{ marginTop: '20px' }}>
          <CardContent>
            <Typography variant="h6">AI Strategy</Typography>
            <MarkdownPreview content={recommendation} />
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default TeamBuilder;
