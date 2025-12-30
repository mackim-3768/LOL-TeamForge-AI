import { useParams } from 'react-router-dom';
import { Box, Container, Grid, Typography, Button, Alert } from '@mui/material';
import ScoreCard from '../components/Dashboard/ScoreCard';
import RoleRadar from '../components/Dashboard/RoleRadar';
import AIInsightCard from '../components/Dashboard/AIInsightCard';
import TeamRecommendationCard from '../components/Dashboard/TeamRecommendationCard';
import LoadingState from '../components/Common/LoadingState';
import { useDashboardData } from '../hooks/useDashboardData';
import RefreshIcon from '@mui/icons-material/Refresh';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import CasinoIcon from '@mui/icons-material/Casino';

export default function Dashboard() {
    const { summonerName } = useParams<{ summonerName: string }>();
    const { data, loading, error, progress } = useDashboardData(summonerName || '');

    if (loading) return <LoadingState progress={progress} />;

    if (error) {
        return (
            <Container maxWidth="md" sx={{ mt: 10 }}>
                <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
                <Button variant="outlined" startIcon={<RefreshIcon />} onClick={() => window.location.reload()}>
                    Retry
                </Button>
            </Container>
        );
    }

    if (!data) return null;

    const { summary, scores, analysis } = data;

    return (
        <Container maxWidth="xl" sx={{ py: 4 }}>
            {/* Header */}
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
                        {summonerName}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Last updated: Just now
                    </Typography>
                </Box>
                <Button variant="outlined" startIcon={<RefreshIcon />}>
                    Refresh Data
                </Button>
            </Box>

            {/* KPI Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <ScoreCard
                        title="Win Rate"
                        value={`${(summary?.winRate || 0).toFixed(1)}%`}
                        trend="up" trendValue="+2.1%"
                        icon={<TrendingUpIcon fontSize="large" />}
                        color="#10b981"
                    />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <ScoreCard
                        title="Avg Score"
                        value={(summary?.avgScore || 0).toFixed(1)}
                        subValue="Rank A"
                        icon={<EmojiEventsIcon fontSize="large" />}
                        color="#f59e0b"
                    />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <ScoreCard
                        title="Total Games"
                        value={summary?.totalGames || 0}
                        icon={<VideogameAssetIcon fontSize="large" />}
                        color="#3b82f6"
                    />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <ScoreCard
                        title="Best Role"
                        value={summary?.topRole || "N/A"}
                        icon={<CasinoIcon fontSize="large" />}
                        color="#8b5cf6"
                    />
                </Grid>
            </Grid>

            {/* Main Analysis Grid */}
            <Grid container spacing={3}>
                {/* Left Column: Charts */}
                <Grid size={{ xs: 12, md: 7 }}>
                    <Grid container spacing={3}>
                        <Grid size={{ xs: 12 }}>
                            <Box sx={{ p: 3, borderRadius: 4, bgcolor: 'background.paper', border: '1px solid rgba(255,255,255,0.05)' }}>
                                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>Role Performance Radar</Typography>
                                <RoleRadar data={scores.map(s => ({ role: s.role, score: s.score }))} />
                            </Box>
                        </Grid>
                        {/* Add more charts here (Bar charts etc) */}
                    </Grid>
                </Grid>

                {/* Right Column: AI & Recommendations */}
                <Grid size={{ xs: 12, md: 5 }}>
                    <Grid container spacing={3} direction="column">
                        <Grid size={{ xs: 12 }} sx={{ flexGrow: 1 }}>
                            <AIInsightCard content={analysis?.analysis || null} />
                        </Grid>
                        <Grid size={{ xs: 12 }}>
                            <TeamRecommendationCard />
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Container>
    );
}
