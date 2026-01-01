import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip
} from 'recharts';
import { Paper, Typography, Box } from '@mui/material';

interface PerformanceMetrics {
  role: string;
  win_rate: number;
  kda: number;
  vision_score: number;
  avg_gold: number;
  avg_damage: number;
  avg_cs: number;
}

interface Props {
  data: PerformanceMetrics;
}

export const PerformanceRadarChart: React.FC<Props> = ({ data }) => {
  // Normalize data for the chart (assuming some baseline max values for visualization)
  // Win Rate: 0-100
  // KDA: 0-10 (approx) -> scale to 100
  // Vision: 0-50 -> scale to 100
  // Gold: 0-20000 -> scale to 100
  // Damage: 0-40000 -> scale to 100
  // CS: 0-300 -> scale to 100

  // We want to display the "shape" of the player.
  // Note: These max values are arbitrary "good" performance benchmarks.
  const MAX_KDA = 5;
  const MAX_VISION = 30;
  const MAX_GOLD = 15000;
  const MAX_DAMAGE = 30000;
  const MAX_CS = 250;

  const normalize = (value: number, max: number) => {
    return Math.min(100, (value / max) * 100);
  };

  const chartData = [
    {
      subject: 'Win Rate',
      A: data.win_rate, // Already 0-100
      fullMark: 100,
      original: `${data.win_rate}%`,
    },
    {
      subject: 'KDA',
      A: normalize(data.kda, MAX_KDA),
      fullMark: 100,
      original: data.kda.toFixed(2),
    },
    {
      subject: 'Vision',
      A: normalize(data.vision_score, MAX_VISION),
      fullMark: 100,
      original: data.vision_score.toFixed(1),
    },
    {
      subject: 'Gold',
      A: normalize(data.avg_gold, MAX_GOLD),
      fullMark: 100,
      original: Math.round(data.avg_gold).toLocaleString(),
    },
    {
      subject: 'DMG',
      A: normalize(data.avg_damage, MAX_DAMAGE),
      fullMark: 100,
      original: Math.round(data.avg_damage).toLocaleString(),
    },
    {
      subject: 'CS',
      A: normalize(data.avg_cs, MAX_CS),
      fullMark: 100,
      original: Math.round(data.avg_cs).toLocaleString(),
    },
  ];

  return (
    <Paper elevation={3} sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Typography variant="h6" gutterBottom>
        Performance Style ({data.role})
      </Typography>
      <Box sx={{ width: '100%', height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} />
            <Radar
              name={data.role}
              dataKey="A"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
            />
            <Tooltip
              formatter={(_value, _name, props) => [props.payload.original, props.payload.subject]}
            />
          </RadarChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};
