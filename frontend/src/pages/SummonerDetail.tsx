import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import type { ScoreResponse, MatchPerformance, MatchDetailResponse } from '../api';
import { Container, Typography, Grid, Card, CardContent, CircularProgress, Divider, Box, Button, Dialog, DialogTitle, DialogContent, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';

const SummonerDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [scores, setScores] = useState<ScoreResponse[]>([]);
  const [analysis, setAnalysis] = useState('');
  const [matches, setMatches] = useState<MatchPerformance[]>([]);
  const [matchesOffset, setMatchesOffset] = useState(0);
  const [hasMoreMatches, setHasMoreMatches] = useState(true);
  const [matchesLoading, setMatchesLoading] = useState(false);
  const [matchDetailOpen, setMatchDetailOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState<MatchPerformance | null>(null);
  const [matchDetail, setMatchDetail] = useState<MatchDetailResponse | null>(null);
  const [matchDetailLoading, setMatchDetailLoading] = useState(false);
  const [matchDetailError, setMatchDetailError] = useState<string | null>(null);
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

  const openMatchDetail = async (match: MatchPerformance) => {
    if (matchDetailLoading) return;

    setSelectedMatch(match);
    setMatchDetailOpen(true);
    setMatchDetail(null);
    setMatchDetailError(null);
    setMatchDetailLoading(true);

    try {
      const res = await api.getMatchDetail(match.match_id);
      setMatchDetail(res.data);
    } catch (err) {
      console.error(err);
      setMatchDetailError('매치 상세를 불러오지 못했습니다.');
    } finally {
      setMatchDetailLoading(false);
    }
  };

  const closeMatchDetail = () => {
    setMatchDetailOpen(false);
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
              style={{ backgroundColor: m.win ? '#e3f2fd' : '#ffebee', cursor: 'pointer' }}
              onClick={() => openMatchDetail(m)}
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

      <Dialog open={matchDetailOpen} onClose={closeMatchDetail} fullWidth maxWidth="lg">
        <DialogTitle>
          {selectedMatch
            ? `${new Date(selectedMatch.game_creation).toLocaleString()} - ${selectedMatch.champion_name}`
            : 'Match Detail'}
        </DialogTitle>
        <DialogContent dividers>
          {matchDetailLoading && (
            <Box display="flex" justifyContent="center" my={2}>
              <CircularProgress />
            </Box>
          )}

          {matchDetailError && (
            <Typography color="error" variant="body2" gutterBottom>
              {matchDetailError}
            </Typography>
          )}

          {matchDetail && (
            <Box display="flex" flexDirection="column" gap={3}>
              <Typography variant="subtitle2" color="textSecondary">
                {new Date(matchDetail.game_creation).toLocaleString()} · 약 {Math.round(matchDetail.game_duration / 60)}분 · Queue {matchDetail.queue_id}
              </Typography>

              <Box>
                <Typography variant="h6" gutterBottom>Blue Team</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Summoner</TableCell>
                      <TableCell>Champion</TableCell>
                      <TableCell>Lane</TableCell>
                      <TableCell align="right">K / D / A</TableCell>
                      <TableCell align="right">CS</TableCell>
                      <TableCell align="right">Damage</TableCell>
                      <TableCell align="right">Gold</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matchDetail.blue_team.map((p) => (
                      <TableRow key={p.summoner_name + p.champion_name}>
                        <TableCell>{p.summoner_name}</TableCell>
                        <TableCell>{p.champion_name}</TableCell>
                        <TableCell>{p.lane || p.role}</TableCell>
                        <TableCell align="right">
                          {p.kills} / {p.deaths} / {p.assists}
                        </TableCell>
                        <TableCell align="right">{p.total_minions_killed}</TableCell>
                        <TableCell align="right">{p.total_damage_dealt_to_champions}</TableCell>
                        <TableCell align="right">{p.gold_earned}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>

              <Box>
                <Typography variant="h6" gutterBottom>Red Team</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Summoner</TableCell>
                      <TableCell>Champion</TableCell>
                      <TableCell>Lane</TableCell>
                      <TableCell align="right">K / D / A</TableCell>
                      <TableCell align="right">CS</TableCell>
                      <TableCell align="right">Damage</TableCell>
                      <TableCell align="right">Gold</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matchDetail.red_team.map((p) => (
                      <TableRow key={p.summoner_name + p.champion_name}>
                        <TableCell>{p.summoner_name}</TableCell>
                        <TableCell>{p.champion_name}</TableCell>
                        <TableCell>{p.lane || p.role}</TableCell>
                        <TableCell align="right">
                          {p.kills} / {p.deaths} / {p.assists}
                        </TableCell>
                        <TableCell align="right">{p.total_minions_killed}</TableCell>
                        <TableCell align="right">{p.total_damage_dealt_to_champions}</TableCell>
                        <TableCell align="right">{p.gold_earned}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Container>
  );
};

export default SummonerDetail;
