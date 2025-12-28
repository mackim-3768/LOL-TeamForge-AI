import axios from 'axios';

// Ensure this matches the FastAPI port
const API_URL = 'http://localhost:8000';

export interface Summoner {
  id: number;
  name: string;
  level: number;
}

export interface ScoreResponse {
  role: string;
  score: number;
  win_rate: number;
  kda: number;
  avg_gold: number;
  vision_score: number;
}

export interface PlaystyleTag {
  id: string;
  label_ko: string;
}

export interface PlaystyleTagSnapshot {
  tags: PlaystyleTag[];
  primary_role: string | null;
  games_used: number;
  calculated_at: string | null;
  version: string;
}

export interface AnalysisResponse {
  analysis: string;
}

export interface MatchPerformance {
  id: number;
  match_id: string;
  game_creation: string;
  lane: string;
  role: string;
  champion_name: string;
  win: boolean;
  kills: number;
  deaths: number;
  assists: number;
  kda: number;
  gold_per_min: number;
  vision_score: number;
  total_minions_killed: number;
  total_damage_dealt_to_champions: number;
}

export interface MatchListResponse {
  matches: MatchPerformance[];
  has_more: boolean;
}

export interface MatchDetailParticipant {
  summoner_name: string;
  champion_name: string;
  team_id: number;
  lane: string;
  role: string;
  kills: number;
  deaths: number;
  assists: number;
  kda: number;
  total_damage_dealt_to_champions: number;
  total_minions_killed: number;
  gold_earned: number;
  win: boolean;
  items: number[];
  primary_rune_id?: number | null;
  op_score: number;
}

export interface MatchDetailResponse {
  match_id: string;
  game_creation: string;
  game_duration: number;
  queue_id: number;
  blue_team: MatchDetailParticipant[];
  red_team: MatchDetailParticipant[];
  blue_total_kills: number;
  red_total_kills: number;
  blue_total_gold: number;
  red_total_gold: number;
}

export interface LeaderboardEntry {
  name: string;
  level: number;
  best_role: string | null;
  best_score: number;
  games: number;
}

export const api = {
  getSummoners: () => axios.get<Summoner[]>(`${API_URL}/summoners/`),
  registerSummoner: (name: string) => axios.post<Summoner>(`${API_URL}/summoners/`, { name }),
  getScores: (name: string) => axios.get<ScoreResponse[]>(`${API_URL}/summoners/${name}/scores`),
  getAnalysis: (name: string) => axios.get<AnalysisResponse>(`${API_URL}/analysis/summoner/${name}`),
  recommendComp: (names: string[]) => axios.post<AnalysisResponse>(`${API_URL}/analysis/recommend-comp`, { summoner_names: names }),
  updateRiotKey: (key: string) => axios.put(`${API_URL}/admin/config/riot-key`, { riot_api_key: key }),
  updateOpenAIKey: (key: string) => axios.put(`${API_URL}/admin/config/openai-key`, { openai_api_key: key }),
  getMatches: (name: string, offset: number, limit: number) =>
    axios.get<MatchListResponse>(`${API_URL}/summoners/${name}/matches`, {
      params: { offset, limit },
    }),
  getMatchDetail: (matchId: string) =>
    axios.get<MatchDetailResponse>(`${API_URL}/matches/${matchId}`),
  getLeaderboard: (timeframe: 'daily' | 'weekly' | 'monthly' | 'yearly') =>
    axios.get<LeaderboardEntry[]>(`${API_URL}/leaderboard`, { params: { timeframe } }),
  getPlaystyleTags: (name: string) =>
    axios.get<PlaystyleTagSnapshot>(`${API_URL}/summoners/${name}/playstyle-tags`),
  recalcPlaystyleTags: (name: string, options?: { noRefresh?: boolean }) =>
    axios.post<PlaystyleTagSnapshot>(
      `${API_URL}/summoners/${name}/playstyle-tags/recalculate`,
      null,
      options?.noRefresh !== undefined
        ? { params: { no_refresh: options.noRefresh } }
        : undefined,
    ),
};
