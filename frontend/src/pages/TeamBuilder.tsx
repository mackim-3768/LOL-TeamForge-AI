import React, { useState, useEffect } from 'react';
import { api } from '../api';
import type { Summoner, DuoSynergyResponse } from '../api';
import { Container, Typography, Button, FormControl, InputLabel, Select, MenuItem, Chip, Box, Card, CardContent } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';

const TeamBuilder: React.FC = () => {
  const [allSummoners, setAllSummoners] = useState<Summoner[]>([]);
  const [selectedSummoners, setSelectedSummoners] = useState<string[]>([]);
  const [recommendation, setRecommendation] = useState('');
  const [loading, setLoading] = useState(false);
  const [duoA, setDuoA] = useState<string>('');
  const [duoB, setDuoB] = useState<string>('');
  const [duoLoading, setDuoLoading] = useState(false);
  const [duoError, setDuoError] = useState<string | null>(null);
  const [duoResult, setDuoResult] = useState<DuoSynergyResponse | null>(null);

  useEffect(() => {
    api.getSummoners().then(res => setAllSummoners(res.data));
  }, []);

  useEffect(() => {
    if (selectedSummoners.length < 2) {
      setDuoA('');
      setDuoB('');
      setDuoResult(null);
      setDuoError(null);
      return;
    }

    if (!duoA && !duoB) {
      setDuoA(selectedSummoners[0]);
      setDuoB(selectedSummoners[1]);
    }
  }, [selectedSummoners, duoA, duoB]);

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

  const handleAnalyzeDuo = async () => {
    if (!duoA || !duoB || duoA === duoB) return;
    if (!selectedSummoners.includes(duoA) || !selectedSummoners.includes(duoB)) return;

    setDuoLoading(true);
    setDuoError(null);
    try {
      const res = await api.getDuoSynergy(duoA, duoB);
      setDuoResult(res.data);
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setDuoError('듀오 중 한 명 이상의 소환사를 찾을 수 없습니다. Register에서 등록했는지 확인해주세요.');
      } else {
        setDuoError('듀오 시너지 분석 중 오류가 발생했습니다.');
      }
      setDuoResult(null);
    } finally {
      setDuoLoading(false);
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
            <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{recommendation}</Typography>
          </CardContent>
        </Card>
      )}

      <Card style={{ marginTop: '20px' }}>
        <CardContent>
          <Typography variant="h6">Duo Synergy</Typography>
          {selectedSummoners.length < 2 ? (
            <Typography variant="body2" color="textSecondary">
              듀오 시너지를 보려면 먼저 최소 두 명의 소환사를 선택하세요.
            </Typography>
          ) : (
            <>
              <Box display="flex" gap={2} mt={1} mb={2} flexWrap="wrap">
                <FormControl size="small" style={{ minWidth: 160 }}>
                  <InputLabel>Duo 1</InputLabel>
                  <Select
                    value={duoA || ''}
                    label="Duo 1"
                    onChange={(e) => setDuoA(e.target.value as string)}
                  >
                    {selectedSummoners.map((name) => (
                      <MenuItem key={name} value={name}>
                        {name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl size="small" style={{ minWidth: 160 }}>
                  <InputLabel>Duo 2</InputLabel>
                  <Select
                    value={duoB || ''}
                    label="Duo 2"
                    onChange={(e) => setDuoB(e.target.value as string)}
                  >
                    {selectedSummoners.map((name) => (
                      <MenuItem key={name} value={name}>
                        {name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Button
                  variant="outlined"
                  onClick={handleAnalyzeDuo}
                  disabled={
                    duoLoading ||
                    !duoA ||
                    !duoB ||
                    duoA === duoB ||
                    !selectedSummoners.includes(duoA) ||
                    !selectedSummoners.includes(duoB)
                  }
                >
                  {duoLoading ? '분석 중...' : '듀오 분석'}
                </Button>
              </Box>

              {duoError && (
                <Typography variant="body2" color="error" gutterBottom>
                  {duoError}
                </Typography>
              )}

              {duoResult && !duoLoading && (
                <>
                  <Typography variant="subtitle1" gutterBottom>
                    {duoResult.summoner1} &amp; {duoResult.summoner2}
                  </Typography>
                  <Typography variant="h5" color="primary" gutterBottom>
                    {duoResult.synergy_score}
                    <Typography component="span" variant="subtitle1" color="textSecondary" style={{ marginLeft: 8 }}>
                      / 100 Synergy
                    </Typography>
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={0.5}>
                    <Typography variant="body2">
                      스타일 궁합: {Math.round(duoResult.style_score * 100)}점
                    </Typography>
                    <Typography variant="body2">
                      듀오 퍼포먼스: {Math.round(duoResult.performance_score * 100)}점 ({duoResult.games_together}게임)
                    </Typography>
                  </Box>
                </>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

export default TeamBuilder;
