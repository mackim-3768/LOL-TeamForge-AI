import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import GroupWorkIcon from '@mui/icons-material/GroupWork';

interface Recommendation {
    compName: string;
    champions: string[];
    reason: string;
    synergyScore: number;
}

// Mock Data for now as API might not provide structured recs yet
const MOCK_RECS: Recommendation[] = [
    {
        compName: "Wombo Combo",
        champions: ["Malphite", "Jarvan IV", "Orianna", "Miss Fortune", "Amumu"],
        reason: "Maximize AOE damage and crowd control for easy teamfight wins.",
        synergyScore: 95
    },
    {
        compName: "Protect the Hypercarry",
        champions: ["Shen", "Sejuani", "Lulu", "Jinx", "Janna"],
        reason: "Peel for Jinx and let her reset. Strong late game assurance.",
        synergyScore: 88
    }
];

export default function TeamRecommendationCard() {
    return (
        <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 1 }}>
                    <GroupWorkIcon color="info" />
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Recommended Comps
                    </Typography>
                </Box>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {MOCK_RECS.map((rec, idx) => (
                        <Box key={idx} sx={{
                            p: 2,
                            borderRadius: 2,
                            bgcolor: 'rgba(255,255,255,0.03)',
                            border: '1px solid rgba(255,255,255,0.05)',
                            transition: 'all 0.2s',
                            '&:hover': { bgcolor: 'rgba(255,255,255,0.05)', borderColor: 'rgba(255,255,255,0.1)' }
                        }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1.5 }}>
                                <Typography variant="subtitle1" fontWeight="600" color="text.primary">{rec.compName}</Typography>
                                <Chip label={`${rec.synergyScore}% Synergy`} size="small" color="success" variant="filled" sx={{ height: 20 }} />
                            </Box>

                            <Box sx={{ display: 'flex', gap: 1, mb: 1.5 }}>
                                {rec.champions.map(champ => (
                                    <Chip key={champ} label={champ} size="small" variant="outlined" sx={{ borderColor: 'rgba(255,255,255,0.2)' }} />
                                ))}
                            </Box>

                            <Typography variant="body2" color="text.secondary">
                                {rec.reason}
                            </Typography>
                        </Box>
                    ))}
                </Box>
            </CardContent>
        </Card>
    );
}
