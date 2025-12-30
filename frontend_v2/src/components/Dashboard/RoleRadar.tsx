import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar, Tooltip, PolarRadiusAxis } from 'recharts';
import { Box, Typography, Paper } from '@mui/material';

interface RoleData {
    role: string;
    score: number;
}

interface RoleRadarProps {
    data: RoleData[];
}

// Custom Tooltip
const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <Paper sx={{ p: 1.5, background: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.1)' }}>
                <Typography variant="subtitle2" sx={{ color: '#fff', fontWeight: 600 }}>{label}</Typography>
                <Typography variant="body2" sx={{ color: '#3b82f6' }}>Score: {payload[0].value}</Typography>
            </Paper>
        );
    }
    return null;
};

export default function RoleRadar({ data }: RoleRadarProps) {
    return (
        <Box sx={{ width: '100%', height: 320 }}>
            {data.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
                        <PolarGrid stroke="rgba(255,255,255,0.1)" />
                        <PolarAngleAxis
                            dataKey="role"
                            tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 500 }}
                        />
                        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                        <Radar
                            name="Role Score"
                            dataKey="score"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            fill="#3b82f6"
                            fillOpacity={0.3}
                        />
                        <Tooltip content={<CustomTooltip />} cursor={false} />
                    </RadarChart>
                </ResponsiveContainer>
            ) : (
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'text.disabled' }}>
                    No data available
                </Box>
            )}
        </Box>
    );
}
