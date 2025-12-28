import React, { useMemo } from 'react';
import type { ScoreResponse } from '../api';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
} from 'recharts';

interface RoleRadarChartProps {
  scores: ScoreResponse[];
}

const ROLE_ORDER: string[] = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY'];

const RoleRadarChart: React.FC<RoleRadarChartProps> = ({ scores }) => {
  const data = useMemo(
    () => {
      const scoreMap = new Map<string, number>();
      scores.forEach((s) => {
        scoreMap.set(s.role, s.score);
      });

      return ROLE_ORDER.map((role) => ({
        role,
        score: scoreMap.get(role) ?? 0,
      }));
    },
    [scores],
  );

  return (
    <ResponsiveContainer width="100%" height="100%">
      <RadarChart data={data} outerRadius="70%">
        <PolarGrid />
        <PolarAngleAxis dataKey="role" />
        <PolarRadiusAxis angle={90} domain={[0, 100]} />
        <Radar name="Score" dataKey="score" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
        <Tooltip />
      </RadarChart>
    </ResponsiveContainer>
  );
};

export default RoleRadarChart;
