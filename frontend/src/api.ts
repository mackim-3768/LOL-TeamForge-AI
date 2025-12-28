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
};
