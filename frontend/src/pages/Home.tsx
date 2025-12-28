import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper, Tabs, Tab, Table, TableHead, TableRow, TableCell, TableBody, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import type { LeaderboardEntry } from '../api';

const Home: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [timeframe, setTimeframe] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');
  const navigate = useNavigate();

  useEffect(() => {
    // Prefetch summoners for autocomplete
    api.getLeaderboard(timeframe).then(res => setLeaderboard(res.data)).catch(console.error);
  }, [timeframe]);

  const topSummoners = leaderboard.slice(0, 10);

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
        <Typography variant="h3" fontWeight="bold" gutterBottom>
          Best Players
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          일간 / 주간 / 월간 / 연간 베스트 플레이어 랭킹
        </Typography>

        <Paper sx={{ mt: 4, borderRadius: 2, overflow: 'hidden' }}>
          <Tabs
            value={timeframe}
            onChange={(_e, value) => setTimeframe(value)}
            indicatorColor="secondary"
            textColor="inherit"
            centered
          >
            <Tab label="일간" value="daily" />
            <Tab label="주간" value="weekly" />
            <Tab label="월간" value="monthly" />
            <Tab label="연간" value="yearly" />
          </Tabs>

          <Table>
            <TableHead>
              <TableRow>
                <TableCell align="center">Rank</TableCell>
                <TableCell>Summoner</TableCell>
                <TableCell align="center">Best Role</TableCell>
                <TableCell align="right">Score</TableCell>
                <TableCell align="right">Games</TableCell>
                <TableCell align="center">Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topSummoners.map((entry, index) => (
                <TableRow key={entry.name} hover>
                  <TableCell align="center">{index + 1}</TableCell>
                  <TableCell>{entry.name}</TableCell>
                  <TableCell align="center">{entry.best_role ?? '-'}</TableCell>
                  <TableCell align="right">{entry.best_score.toFixed(1)}</TableCell>
                  <TableCell align="right">{entry.games}</TableCell>
                  <TableCell align="center">
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => navigate(`/summoner/${entry.name}`)}
                    >
                      View Detail
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </Container>
    </Box>
  );
};

export default Home;
