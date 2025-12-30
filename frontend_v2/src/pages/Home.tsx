import { Container, Typography, Box, Grid, Card, CardContent, Chip, Stack } from '@mui/material';
import SearchInput from '../components/Common/SearchInput';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PsychologyIcon from '@mui/icons-material/Psychology';
import GroupsIcon from '@mui/icons-material/Groups';
import HistoryIcon from '@mui/icons-material/History';
import { motion } from 'framer-motion';

const features = [
    {
        icon: <TrendingUpIcon fontSize="large" color="primary" />,
        title: 'Role Analysis',
        desc: 'Deep dive into your performance across all roles using advanced metrics.'
    },
    {
        icon: <PsychologyIcon fontSize="large" color="secondary" />,
        title: 'AI Insights',
        desc: 'Get personalized coaching tips and strategy adjustments from our AI.'
    },
    {
        icon: <GroupsIcon fontSize="large" color="info" />,
        title: 'Team Synergy',
        desc: 'Discover the best team compositions for your playstyle and squad.'
    }
];

export default function Home() {
    const recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');

    return (
        <Container maxWidth="lg">
            {/* Hero Section */}
            <Box sx={{
                minHeight: '80vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                pt: 8, pb: 12
            }}>
                {/* Animated Badge */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
                    <Chip
                        label="Version 2.0 Now Available"
                        color="primary"
                        variant="outlined"
                        size="small"
                        sx={{ mb: 4, bgcolor: 'rgba(59, 130, 246, 0.1)', borderColor: 'rgba(59, 130, 246, 0.3)' }}
                    />
                </motion.div>

                {/* Title */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
                    <Typography variant="h1" sx={{
                        fontWeight: 800,
                        mb: 2,
                        background: 'linear-gradient(to bottom right, #ffffff, #94a3b8)',
                        backgroundClip: 'text',
                        textFillColor: 'transparent',
                        letterSpacing: '-0.03em',
                        fontSize: { xs: '2.5rem', md: '4rem' }
                    }}>
                        Dominate Flex Queue
                    </Typography>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
                    <Typography variant="h5" color="text.secondary" sx={{ mb: 6, maxWidth: 600, mx: 'auto', lineHeight: 1.6 }}>
                        Advanced analytics, role scoring, and AI-powered recommendations to help your team climb together.
                    </Typography>
                </motion.div>

                {/* Search */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    style={{ width: '100%', display: 'flex', justifyContent: 'center', position: 'relative', zIndex: 10 }}
                >
                    <SearchInput placeholder="Enter Summoner Name (e.g. Hide on bush)" />
                </motion.div>

                {/* Recent Searches */}
                {recentSearches.length > 0 && (
                    <Box sx={{ mt: 3, display: 'flex', gap: 1, alignItems: 'center' }}>
                        <HistoryIcon fontSize="small" color="disabled" />
                        <Typography variant="body2" color="text.secondary">Recent:</Typography>
                        <Stack direction="row" spacing={1}>
                            {/* Placeholder for now / simple implementation */}
                            <Chip label="Faker" size="small" onClick={() => { }} clickable variant="outlined" />
                            <Chip label="Chovy" size="small" onClick={() => { }} clickable variant="outlined" />
                        </Stack>
                    </Box>
                )}
            </Box>

            {/* Features Grid */}
            <Grid container spacing={4} sx={{ mb: 12 }}>
                {features.map((feature, i) => (
                    <Grid size={{ xs: 12, md: 4 }} key={i}>
                        <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 + (i * 0.1) }}>
                            <Card sx={{ height: '100%', background: 'rgba(30, 41, 59, 0.4)', borderColor: 'rgba(255,255,255,0.05)' }}>
                                <CardContent sx={{ p: 4, textAlign: 'left' }}>
                                    <Box sx={{ mb: 2, p: 1.5, display: 'inline-flex', borderRadius: 3, bgcolor: 'rgba(255,255,255,0.03)' }}>
                                        {feature.icon}
                                    </Box>
                                    <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                                        {feature.title}
                                    </Typography>
                                    <Typography variant="body1" color="text.secondary">
                                        {feature.desc}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </motion.div>
                    </Grid>
                ))}
            </Grid>
        </Container>
    );
}
