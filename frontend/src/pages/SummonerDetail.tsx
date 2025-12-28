import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import type { ScoreResponse, MatchPerformance } from '../api';
import { Container, Typography, Grid, Card, CardContent, CircularProgress, Divider, Box, Button } from '@mui/material';

const SummonerDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [scores, setScores] = useState<ScoreResponse[]>([]);
  const [analysis, setAnalysis] = useState('');
  const [matches, setMatches] = useState<MatchPerformance[]>([]);
  const [matchesOffset, setMatchesOffset] = useState(0);
  const [hasMoreMatches, setHasMoreMatches] = useState(true);
  const [matchesLoading, setMatchesLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const PAGE_SIZE = 20;

  useEffect(() => {
    if (name) {
      fetchData(name);
    }
  }, [name]);

  const fetchData = async (summonerName: string) => {
    try {
      const [scoresRes, analysisRes, matchesRes] = await Promise.all([
        api.getScores(summonerName),
        api.getAnalysis(summonerName),
        api.getMatches(summonerName, 0, PAGE_SIZE),
      ]);
      setScores(scoresRes.data);
      setAnalysis(analysisRes.data.analysis);
      setMatches(matchesRes.data.matches);
      setHasMoreMatches(matchesRes.data.has_more);
      setMatchesOffset(matchesRes.data.matches.length);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadMoreMatches = async () => {
    if (!name || matchesLoading || !hasMoreMatches) return;

    setMatchesLoading(true);
    try {
      const res = await api.getMatches(name, matchesOffset, PAGE_SIZE);
      setMatches((prev) => [...prev, ...res.data.matches]);
      setHasMoreMatches(res.data.has_more);
      setMatchesOffset((prev) => prev + res.data.matches.length);
    } catch (err) {
      console.error(err);
    } finally {
      setMatchesLoading(false);
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

      <Divider style={{ margin: '20px 0' }} />

      <Typography variant="h5" gutterBottom>Recent Matches</Typography>
      {matches.length === 0 ? (
        <Typography variant="body2">아직 저장된 매치가 없습니다.</Typography>
      ) : (
        <Box display="flex" flexDirection="column" gap={2}>
          {matches.map((m) => (
            <Card
              key={m.id}
              style={{ backgroundColor: m.win ? '#e3f2fd' : '#ffebee' }}
            >
              <CardContent>
                <Box display="flex" justifyContent="space-between" flexWrap="wrap" gap={1}>
                  <Box>
                    <Typography variant="subtitle2">
                      {m.win ? '승리' : '패배'} · {(m.lane || m.role) ?? ''} · {m.champion_name}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(m.game_creation).toLocaleString()}
                    </Typography>
                  </Box>
                  <Box textAlign="right">
                    <Typography variant="subtitle2">
                      {m.kills}/{m.deaths}/{m.assists} ({m.kda.toFixed(2)} KDA)
                    </Typography>
                    <Typography variant="caption">
                      CS {m.total_minions_killed} · 골드/분 {m.gold_per_min.toFixed(1)} · 시야 {m.vision_score}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}

      {hasMoreMatches && (
        <Box display="flex" justifyContent="center" mt={2}>
          <Button variant="outlined" onClick={loadMoreMatches} disabled={matchesLoading}>
            {matchesLoading ? 'Loading...' : 'View More'}
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default SummonerDetail;
