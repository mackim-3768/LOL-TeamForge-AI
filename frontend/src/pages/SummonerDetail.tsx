import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import type { ScoreResponse, MatchPerformance, MatchDetailResponse, PlaystyleTagSnapshot } from '../api';
import { Container, Typography, Grid, Card, CardContent, CircularProgress, Divider, Box, Button, Dialog, DialogTitle, DialogContent, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import { DDRAGON_BASE, COLOR_BLUE_TEAM, COLOR_RED_TEAM, CHAMPION_ICON_SIZE, ITEM_ICON_SIZE, RUNE_ICON_SIZE } from '../config';
import RoleRadarChart from '../components/RoleRadarChart';
import MarkdownPreview from '../components/MarkdownPreview';

const getChampionIconUrl = (championName: string) =>
  `${DDRAGON_BASE}/img/champion/${championName}.png`;

const getItemIconUrl = (itemId: number) =>
  `${DDRAGON_BASE}/img/item/${itemId}.png`;

const getRuneIconUrl = (runeId: number) =>
  `${DDRAGON_BASE}/img/perk/${runeId}.png`;

const SummonerDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [scores, setScores] = useState<ScoreResponse[]>([]);
  const [analysis, setAnalysis] = useState('');
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
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
  const [playstyleSnapshot, setPlaystyleSnapshot] = useState<PlaystyleTagSnapshot | null>(null);
  const [playstyleLoading, setPlaystyleLoading] = useState(false);
  const [playstyleRecalcLoading, setPlaystyleRecalcLoading] = useState(false);
  const [playstyleRefreshLoading, setPlaystyleRefreshLoading] = useState(false);
  const [playstyleError, setPlaystyleError] = useState<string | null>(null);
  const PAGE_SIZE = 20;

  useEffect(() => {
    if (name) {
      fetchData(name);
      loadAnalysis();
    }
  }, [name]);

  const loadPlaystyleTags = async (summonerName: string) => {
    setPlaystyleLoading(true);
    setPlaystyleError(null);
    try {
      const res = await api.getPlaystyleTags(summonerName);
      setPlaystyleSnapshot(res.data);
    } catch (err) {
      console.error(err);
      setPlaystyleError('플레이 스타일 태그를 불러오지 못했습니다.');
    } finally {
      setPlaystyleLoading(false);
    }
  };

  const fetchData = async (summonerName: string) => {
    try {
      const [scoresRes, matchesRes] = await Promise.all([
        api.getScores(summonerName),
        api.getMatches(summonerName, 0, PAGE_SIZE),
      ]);
      setScores(scoresRes.data);
      setMatches(matchesRes.data.matches);
      setHasMoreMatches(matchesRes.data.has_more);
      setMatchesOffset(matchesRes.data.matches.length);
      await loadPlaystyleTags(summonerName);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadAnalysis = async (options?: { forceRefresh?: boolean }) => {
    if (!name || analysisLoading) return;

    setAnalysisLoading(true);
    setAnalysisError(null);
    try {
      const res = await api.getAnalysis(name, options);
      setAnalysis(res.data.analysis);
    } catch (err) {
      console.error(err);
      setAnalysisError('AI 분석을 불러오지 못했습니다.');
    } finally {
      setAnalysisLoading(false);
    }
  };

  const recalcPlaystyleTagsOnly = async () => {
    if (!name || playstyleRecalcLoading || playstyleRefreshLoading) return;

    setPlaystyleRecalcLoading(true);
    setPlaystyleError(null);
    try {
      const res = await api.recalcPlaystyleTags(name, { noRefresh: true });
      setPlaystyleSnapshot(res.data);
    } catch (err) {
      console.error(err);
      setPlaystyleError('플레이 스타일 태그 재계산에 실패했습니다.');
    } finally {
      setPlaystyleRecalcLoading(false);
    }
  };

  const refreshMatchesAndTags = async () => {
    if (!name || playstyleRefreshLoading || playstyleRecalcLoading) return;

    setPlaystyleRefreshLoading(true);
    setPlaystyleError(null);
    try {
      await api.recalcPlaystyleTags(name);
      await fetchData(name);
    } catch (err) {
      console.error(err);
      setPlaystyleError('매치데이터 업데이트에 실패했습니다.');
    } finally {
      setPlaystyleRefreshLoading(false);
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
      <Box sx={{ width: '100%', height: 300, mb: 2 }}>
        <RoleRadarChart scores={scores} />
      </Box>
      <Box sx={{ mb: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6">플레이 스타일 태그</Typography>
          <Box display="flex" gap={1}>
            <Button
              variant="outlined"
              size="small"
              onClick={recalcPlaystyleTagsOnly}
              disabled={playstyleRecalcLoading || playstyleRefreshLoading}
            >
              {playstyleRecalcLoading ? '태그 계산 중...' : '태그만 업데이트'}
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={refreshMatchesAndTags}
              disabled={playstyleRefreshLoading || playstyleRecalcLoading}
            >
              {playstyleRefreshLoading ? '매치 갱신 중...' : '매치데이터 업데이트'}
            </Button>
          </Box>
        </Box>
        {playstyleLoading ? (
          <CircularProgress size={20} />
        ) : playstyleError ? (
          <Typography variant="body2" color="error">
            {playstyleError}
          </Typography>
        ) : playstyleSnapshot && playstyleSnapshot.tags.length > 0 ? (
          <Box display="flex" flexWrap="wrap" gap={1}>
            {playstyleSnapshot.tags.map((t) => (
              <Box
                key={t.id}
                sx={{
                  px: 1,
                  py: 0.5,
                  borderRadius: 2,
                  bgcolor: t.color || '#e3f2fd',
                  fontSize: 12,
                }}
              >
                {t.label_ko}
              </Box>
            ))}
          </Box>
        ) : (
          <Typography variant="body2" color="textSecondary">
            아직 플레이 스타일 분석이 없습니다.
          </Typography>
        )}
        {playstyleSnapshot && playstyleSnapshot.games_used > 0 && (
          <Typography variant="caption" color="textSecondary">
            최근 {playstyleSnapshot.games_used}게임 기준
            {playstyleSnapshot.calculated_at
              ? ` · ${new Date(playstyleSnapshot.calculated_at).toLocaleString()} 기준`
              : ''}
          </Typography>
        )}
      </Box>
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
      
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
        <Typography variant="h5" gutterBottom>AI Analysis</Typography>
        <Button
          variant="outlined"
          size="small"
          onClick={() => loadAnalysis({ forceRefresh: true })}
          disabled={analysisLoading || !name}
        >
          {analysisLoading ? 'AI 분석 중...' : 'AI 분석 업데이트'}
        </Button>
      </Box>
      <Card>
        <CardContent>
          {analysisLoading ? (
            <CircularProgress size={20} />
          ) : analysisError ? (
            <Typography variant="body2" color="error">
              {analysisError}
            </Typography>
          ) : analysis ? (
            <MarkdownPreview content={analysis} />
          ) : (
            <Typography variant="body2" color="textSecondary">
              아직 AI 분석이 없습니다. 상단의 "AI 분석 업데이트" 버튼을 눌러 생성해 주세요.
            </Typography>
          )}
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
                <Typography variant="subtitle2" gutterBottom>Total Kill</Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography variant="caption" color="primary">{matchDetail.blue_total_kills}</Typography>
                  <Box flex={1}>
                    <Box display="flex" height={10} borderRadius={4} overflow="hidden">
                      {(() => {
                        const total = matchDetail.blue_total_kills + matchDetail.red_total_kills || 1;
                        const blueRatio = (matchDetail.blue_total_kills / total) * 100;
                        const redRatio = 100 - blueRatio;
                        return (
                          <>
                            <Box width={`${blueRatio}%`} bgcolor={COLOR_BLUE_TEAM} />
                            <Box width={`${redRatio}%`} bgcolor={COLOR_RED_TEAM} />
                          </>
                        );
                      })()}
                    </Box>
                  </Box>
                  <Typography variant="caption" color="error">{matchDetail.red_total_kills}</Typography>
                </Box>
              </Box>

              <Box>
                <Typography variant="subtitle2" gutterBottom>Total Gold</Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography variant="caption" color="primary">{Math.round(matchDetail.blue_total_gold / 100) / 10}k</Typography>
                  <Box flex={1}>
                    <Box display="flex" height={8} borderRadius={4} overflow="hidden">
                      {(() => {
                        const total = matchDetail.blue_total_gold + matchDetail.red_total_gold || 1;
                        const blueRatio = (matchDetail.blue_total_gold / total) * 100;
                        const redRatio = 100 - blueRatio;
                        return (
                          <>
                            <Box width={`${blueRatio}%`} bgcolor="#42a5f5" />
                            <Box width={`${redRatio}%`} bgcolor="#ef5350" />
                          </>
                        );
                      })()}
                    </Box>
                  </Box>
                  <Typography variant="caption" color="error">{Math.round(matchDetail.red_total_gold / 100) / 10}k</Typography>
                </Box>
              </Box>

              <Box>
                <Typography variant="h6" gutterBottom>Blue Team</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Summoner</TableCell>
                      <TableCell>Champion</TableCell>
                      <TableCell>Rune / Items</TableCell>
                      <TableCell>Lane</TableCell>
                      <TableCell align="right">K / D / A</TableCell>
                      <TableCell align="right">CS</TableCell>
                      <TableCell align="right">Damage</TableCell>
                      <TableCell align="right">Gold</TableCell>
                      <TableCell align="right">OP Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matchDetail.blue_team.map((p) => (
                      <TableRow key={p.summoner_name + p.champion_name}>
                        <TableCell>{p.summoner_name}</TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            <img
                              src={getChampionIconUrl(p.champion_name)}
                              alt={p.champion_name}
                              style={{ width: CHAMPION_ICON_SIZE, height: CHAMPION_ICON_SIZE, borderRadius: 4 }}
                            />
                            <Typography variant="body2">{p.champion_name}</Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            {p.primary_rune_id && (
                              <img
                                src={getRuneIconUrl(p.primary_rune_id)}
                                alt="rune"
                                style={{ width: RUNE_ICON_SIZE, height: RUNE_ICON_SIZE, borderRadius: '50%' }}
                              />
                            )}
                            <Box display="flex" gap={0.5}>
                              {p.items.filter((id) => id > 0).map((id) => (
                                <img
                                  key={id}
                                  src={getItemIconUrl(id)}
                                  alt={`item-${id}`}
                                  style={{ width: ITEM_ICON_SIZE, height: ITEM_ICON_SIZE, borderRadius: 3 }}
                                />
                              ))}
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>{p.lane || p.role}</TableCell>
                        <TableCell align="right">
                          {p.kills} / {p.deaths} / {p.assists}
                        </TableCell>
                        <TableCell align="right">{p.total_minions_killed}</TableCell>
                        <TableCell align="right">{p.total_damage_dealt_to_champions}</TableCell>
                        <TableCell align="right">{p.gold_earned}</TableCell>
                        <TableCell align="right">{p.op_score.toFixed(1)}</TableCell>
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
                      <TableCell>Rune / Items</TableCell>
                      <TableCell>Lane</TableCell>
                      <TableCell align="right">K / D / A</TableCell>
                      <TableCell align="right">CS</TableCell>
                      <TableCell align="right">Damage</TableCell>
                      <TableCell align="right">Gold</TableCell>
                      <TableCell align="right">OP Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matchDetail.red_team.map((p) => (
                      <TableRow key={p.summoner_name + p.champion_name}>
                        <TableCell>{p.summoner_name}</TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            <img
                              src={getChampionIconUrl(p.champion_name)}
                              alt={p.champion_name}
                              style={{ width: 28, height: 28, borderRadius: 4 }}
                            />
                            <Typography variant="body2">{p.champion_name}</Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            {p.primary_rune_id && (
                              <img
                                src={getRuneIconUrl(p.primary_rune_id)}
                                alt="rune"
                                style={{ width: 24, height: 24, borderRadius: '50%' }}
                              />
                            )}
                            <Box display="flex" gap={0.5}>
                              {p.items.filter((id) => id > 0).map((id) => (
                                <img
                                  key={id}
                                  src={getItemIconUrl(id)}
                                  alt={`item-${id}`}
                                  style={{ width: 20, height: 20, borderRadius: 3 }}
                                />
                              ))}
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>{p.lane || p.role}</TableCell>
                        <TableCell align="right">
                          {p.kills} / {p.deaths} / {p.assists}
                        </TableCell>
                        <TableCell align="right">{p.total_minions_killed}</TableCell>
                        <TableCell align="right">{p.total_damage_dealt_to_champions}</TableCell>
                        <TableCell align="right">{p.gold_earned}</TableCell>
                        <TableCell align="right">{p.op_score.toFixed(1)}</TableCell>
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
