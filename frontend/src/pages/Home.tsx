import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper, Tabs, Tab, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import { api } from '../api';
import type { Summoner } from '../api';

const Home: React.FC = () => {
  const [summoners, setSummoners] = useState<Summoner[]>([]);
  const [timeframe, setTimeframe] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');

  useEffect(() => {
    // Prefetch summoners for autocomplete
    api.getSummoners().then(res => setSummoners(res.data)).catch(console.error);
  }, []);

  const topSummoners = [...summoners].sort((a, b) => b.level - a.level).slice(0, 10);

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
                <TableCell align="right">Level</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topSummoners.map((s, index) => (
                <TableRow key={s.id} hover>
                  <TableCell align="center">{index + 1}</TableCell>
                  <TableCell>{s.name}</TableCell>
                  <TableCell align="right">{s.level}</TableCell>
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
