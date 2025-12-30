import { Box, Typography, LinearProgress, Container, CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';

interface LoadingStateProps {
    progress?: number;
    message?: string;
}

const steps = [
    { threshold: 10, label: "Connecting to Riot API..." },
    { threshold: 30, label: "Fetching Match History..." },
    { threshold: 60, label: "Calculating Role Performance..." },
    { threshold: 80, label: "Generating AI Insights..." },
    { threshold: 100, label: "Finalizing Analysis..." }
];

export default function LoadingState({ progress = 0 }: LoadingStateProps) {
    const currentStep = steps.find(s => progress <= s.threshold)?.label || "Processing...";

    return (
        <Container maxWidth="sm" sx={{ minHeight: '80vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
                <Box sx={{ position: 'relative', mb: 6, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Box sx={{ position: 'relative' }}>
                        <CircularProgress
                            size={80}
                            thickness={2}
                            sx={{ color: 'rgba(59, 130, 246, 0.2)' }}
                            variant="determinate" value={100}
                        />
                        <CircularProgress
                            size={80}
                            thickness={2}
                            sx={{ color: 'primary.main', position: 'absolute', left: 0 }}
                            variant="determinate" value={progress}
                        />
                        <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Typography variant="caption" sx={{ fontSize: '1.2rem', fontWeight: 600 }}>
                                {progress}%
                            </Typography>
                        </Box>
                    </Box>
                </Box>

                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, textAlign: 'center' }}>
                    Analyzing Summoner
                </Typography>

                <Typography variant="body1" color="text.secondary" sx={{ mb: 4, minHeight: 24, textAlign: 'center' }}>
                    {currentStep}
                </Typography>

                <Box sx={{ width: '100%', minWidth: 300 }}>
                    <LinearProgress
                        variant="determinate"
                        value={progress}
                        sx={{
                            height: 8,
                            borderRadius: 4,
                            bgcolor: 'rgba(255,255,255,0.05)',
                            '& .MuiLinearProgress-bar': {
                                borderRadius: 4,
                                background: 'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)'
                            }
                        }}
                    />
                </Box>

                <Box sx={{ mt: 8, p: 3, bgcolor: 'rgba(255,255,255,0.02)', borderRadius: 2, border: '1px solid rgba(255,255,255,0.05)' }}>
                    <Typography variant="subtitle2" color="secondary" gutterBottom>
                        Did you know?
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Focusing on 2-3 champions per role can increase your win rate by up to 15%.
                    </Typography>
                </Box>
            </motion.div>
        </Container>
    );
}
