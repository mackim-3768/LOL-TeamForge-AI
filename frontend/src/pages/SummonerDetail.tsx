import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import type { ScoreResponse } from '../api';
import { Container, Typography, Grid, Card, CardContent, CircularProgress, Divider } from '@mui/material';

const SummonerDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [scores, setScores] = useState<ScoreResponse[]>([]);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (name) {
      fetchData(name);
    }
  }, [name]);

  const fetchData = async (summonerName: string) => {
    try {
      const [scoresRes, analysisRes] = await Promise.all([
        api.getScores(summonerName),
        api.getAnalysis(summonerName)
      ]);
      setScores(scoresRes.data);
      setAnalysis(analysisRes.data.analysis);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <CircularProgress style={{ margin: '50px' }} />;

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Typography variant="h3" gutterBottom>{name}</Typography>
      
      <Typography variant="h5" gutterBottom>Role Performance (Score 0-100)</Typography>
      <Grid container spacing={2}>
        {scores.map((s) => (
          <Grid key={s.role} size={{ xs: 12, sm: 6, md: 4 }}>
            <Card style={{ backgroundColor: '#f5f5f5' }}>
              <CardContent>
                <Typography variant="h6">{s.role}</Typography>
                <Typography variant="h4" color="primary">{s.score}</Typography>
                <Typography variant="body2">WR: {s.win_rate}%</Typography>
                <Typography variant="body2">KDA: {s.kda}</Typography>
                <Typography variant="body2">Vision: {s.vision_score}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Divider style={{ margin: '20px 0' }} />
      
      <Typography variant="h5" gutterBottom>AI Analysis</Typography>
      <Card>
        <CardContent>
          <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{analysis}</Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default SummonerDetail;
