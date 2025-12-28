import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Box, Card, CardContent, CircularProgress, Grid, LinearProgress } from '@mui/material';
import { api } from '../api';
import type { DuoSynergyResponse } from '../api';

const DuoSynergyTool: React.FC = () => {
  const [summoner1, setSummoner1] = useState('');
  const [summoner2, setSummoner2] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DuoSynergyResponse | null>(null);

  const canSubmit = !loading && summoner1.trim() !== '' && summoner2.trim() !== '';

  const handleAnalyze = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.getDuoSynergy(summoner1.trim(), summoner2.trim());
      setResult(res.data);
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setError('둘 중 한 명 이상의 소환사를 찾을 수 없습니다. 먼저 Register에서 등록했는지 확인해주세요.');
      } else {
        setError('듀오 시너지 분석 중 오류가 발생했습니다.');
      }
    } finally {
      setLoading(false);
    }
  };

  const renderBreakdownBar = (label: string, value: number) => (
    <Box mb={1.5} key={label}>
      <Box display="flex" justifyContent="space-between" mb={0.5}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="caption">{Math.round(value * 100)}점</Typography>
      </Box>
      <LinearProgress variant="determinate" value={Math.max(0, Math.min(100, value * 100))} />
    </Box>
  );

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Duo Synergy Calculator
      </Typography>
      <Typography variant="body1" gutterBottom>
        두 소환사의 최근 플레이 스타일과 실제 듀오 성과를 기반으로 시너지 점수를 계산합니다.
      </Typography>

      <Box display="flex" gap={2} mt={3} mb={2} flexWrap="wrap">
        <TextField
          label="Summoner 1"
          value={summoner1}
          onChange={(e) => setSummoner1(e.target.value)}
          size="small"
        />
        <TextField
          label="Summoner 2"
          value={summoner2}
          onChange={(e) => setSummoner2(e.target.value)}
          size="small"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleAnalyze}
          disabled={!canSubmit}
        >
          {loading ? '분석 중...' : '분석하기'}
        </Button>
      </Box>

      {error && (
        <Typography variant="body2" color="error" gutterBottom>
          {error}
        </Typography>
      )}

      {loading && (
        <Box display="flex" justifyContent="center" my={3}>
          <CircularProgress />
        </Box>
      )}

      {result && !loading && (
        <Card style={{ marginTop: '1rem' }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              {result.summoner1} &amp; {result.summoner2}
            </Typography>
            <Typography variant="h3" color="primary" gutterBottom>
              {result.synergy_score}
              <Typography component="span" variant="h6" color="textSecondary" style={{ marginLeft: 8 }}>
                / 100 Synergy
              </Typography>
            </Typography>

            <Grid container spacing={2} mb={2}>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Typography variant="subtitle2" color="textSecondary">스타일 궁합</Typography>
                <Typography variant="h6">{Math.round(result.style_score * 100)}점</Typography>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Typography variant="subtitle2" color="textSecondary">듀오 퍼포먼스</Typography>
                <Typography variant="h6">{Math.round(result.performance_score * 100)}점</Typography>
                <Typography variant="caption" color="textSecondary">
                  함께 뛴 경기 수: {result.games_together}게임
                </Typography>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Typography variant="subtitle2" color="textSecondary">개인 샘플 수</Typography>
                <Typography variant="body2">
                  {result.summoner1}: {result.summoner1_games}게임
                </Typography>
                <Typography variant="body2">
                  {result.summoner2}: {result.summoner2_games}게임
                </Typography>
              </Grid>
            </Grid>

            <Box mt={2}>
              <Typography variant="subtitle1" gutterBottom>
                스타일 브레이크다운
              </Typography>
              {renderBreakdownBar('초반/라인전', result.style_breakdown.early_game)}
              {renderBreakdownBar('후반/캐리', result.style_breakdown.late_game)}
              {renderBreakdownBar('시야/오브젝트', result.style_breakdown.vision_objective)}
              {renderBreakdownBar('맵 압박', result.style_breakdown.map_pressure)}
              {renderBreakdownBar('리스크 컨트롤', result.style_breakdown.risk_control)}
            </Box>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default DuoSynergyTool;
