import { useState, useEffect } from 'react';
import { api } from '../api';
import type { ScoreResponse, AnalysisResponse, MatchDetailResponse } from '../api';

interface DashboardData {
    scores: ScoreResponse[];
    analysis: AnalysisResponse | null;
    recentMatches: MatchDetailResponse[]; // Simplified for now
    summary: {
        totalGames: number;
        winRate: number;
        avgScore: number;
        topRole: string;
    } | null;
}

export const useDashboardData = (summonerName: string) => {
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        if (!summonerName) return;

        const fetchData = async () => {
            setLoading(true);
            setError(null);
            setProgress(10);

            try {
                // 1. Ensure Summoner is registered/exists
                // For existing backend logic, we might need to register first if not found, 
                // but let's assume valid search or handle 404.
                try {
                    await api.registerSummoner(summonerName);
                } catch (e) {
                    // Ignore if already registered or fetch error, proceed to get scores
                    console.log("Register step skipped or failed", e);
                }
                setProgress(30);

                // 2. Fetch Scores
                const scoresRes = await api.getScores(summonerName);
                setProgress(60);

                // 3. Fetch Analysis (Mocked or real)
                let analysisRes: { data: AnalysisResponse } | null = null;
                try {
                    analysisRes = await api.getAnalysis(summonerName);
                } catch (e) {
                    console.warn("Analysis failed, using mock", e);
                    analysisRes = { data: { analysis: "AI Analysis currently unavailable or pending." } };
                }
                setProgress(80);

                // Process Summary
                const scores = scoresRes.data;
                const totalGames = scores.reduce((acc, curr) => acc + (curr.win_rate * 0 + 10), 0); // Mock total games calculation

                const topRole = scores.reduce((prev, current) => (prev.score > current.score) ? prev : current, scores[0] || { role: 'N/A', score: 0 }).role;
                const avgScore = scores.length > 0 ? scores.reduce((acc, curr) => acc + curr.score, 0) / scores.length : 0;

                // Mock Winrate (Average of roles?)
                const avgWinRate = scores.length > 0 ? scores.reduce((acc, curr) => acc + curr.win_rate, 0) / scores.length : 0;

                setData({
                    scores: scores,
                    analysis: analysisRes?.data || null,
                    recentMatches: [], // Fetch matches later if needed
                    summary: {
                        totalGames: totalGames,
                        winRate: avgWinRate,
                        avgScore: avgScore,
                        topRole: topRole
                    }
                });
                setProgress(100);
            } catch (err: any) {
                setError(err.message || "Failed to load summoner data");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [summonerName]);

    return { data, loading, error, progress };
};
