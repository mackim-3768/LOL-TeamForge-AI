import React from 'react';
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

export const api = {
  getSummoners: () => axios.get<Summoner[]>(`${API_URL}/summoners/`),
  registerSummoner: (name: string) => axios.post<Summoner>(`${API_URL}/summoners/`, { name }),
  getScores: (name: string) => axios.get<ScoreResponse[]>(`${API_URL}/summoners/${name}/scores`),
  getAnalysis: (name: string) => axios.get<AnalysisResponse>(`${API_URL}/analysis/summoner/${name}`),
  recommendComp: (names: string[]) => axios.post<AnalysisResponse>(`${API_URL}/analysis/recommend-comp`, { summoner_names: names }),
  updateRiotKey: (key: string) => axios.put(`${API_URL}/admin/config/riot-key`, { riot_api_key: key })
};
