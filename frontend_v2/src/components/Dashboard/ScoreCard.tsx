import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

interface ScoreCardProps {
    title: string;
    value: string | number;
    subValue?: string;
    trend?: 'up' | 'down' | 'neutral';
    trendValue?: string;
    icon?: React.ReactNode;
    color?: string;
}

export default function ScoreCard({ title, value, subValue, trend, trendValue, icon, color = 'primary.main' }: ScoreCardProps) {
    return (
        <Card sx={{ height: '100%', position: 'relative', overflow: 'hidden' }}>
            <Box sx={{
                position: 'absolute', top: -10, right: -10, p: 2,
                borderRadius: '50%', background: color, opacity: 0.1,
                width: 100, height: 100, zIndex: 0
            }} />
            <CardContent sx={{ position: 'relative', zIndex: 1, p: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                        {title}
                    </Typography>
                    {icon && <Box sx={{ color: color, opacity: 0.8 }}>{icon}</Box>}
                </Box>

                <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                    {value}
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {trend && (
                        <Chip
                            icon={trend === 'up' ? <ArrowUpwardIcon /> : trend === 'down' ? <ArrowDownwardIcon /> : undefined}
                            label={trendValue}
                            size="small"
                            color={trend === 'up' ? 'success' : trend === 'down' ? 'error' : 'default'}
                            variant="outlined"
                            sx={{ height: 24, borderRadius: '6px', '& .MuiChip-label': { px: 1, fontSize: '0.75rem', fontWeight: 600 } }}
                        />
                    )}
                    {subValue && (
                        <Typography variant="body2" color="text.secondary">
                            {subValue}
                        </Typography>
                    )}
                </Box>
            </CardContent>
        </Card>
    );
}
