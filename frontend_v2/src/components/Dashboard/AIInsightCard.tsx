import { Card, CardContent, Typography, Box, Skeleton } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ReactMarkdown from 'react-markdown';

interface AIInsightCardProps {
    content: string | null;
    loading?: boolean;
}

export default function AIInsightCard({ content, loading }: AIInsightCardProps) {
    return (
        <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
                    <AutoAwesomeIcon color="secondary" />
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        AI Coach Insights
                    </Typography>
                </Box>

                {loading ? (
                    <Box>
                        <Skeleton width="90%" height={20} sx={{ mb: 1 }} />
                        <Skeleton width="80%" height={20} sx={{ mb: 1 }} />
                        <Skeleton width="95%" height={20} sx={{ mb: 1 }} />
                        <Skeleton width="60%" height={20} />
                    </Box>
                ) : (
                    <Box sx={{
                        color: 'text.secondary',
                        '& p': { mb: 2, lineHeight: 1.6 },
                        '& ul': { pl: 2.5, mb: 2 },
                        '& li': { mb: 0.5 },
                        '& strong': { color: 'secondary.main', fontWeight: 600 }
                    }}>
                        <ReactMarkdown>{content || "No analysis available."}</ReactMarkdown>
                    </Box>
                )}
            </CardContent>
        </Card>
    );
}
