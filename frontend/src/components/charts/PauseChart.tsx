'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import type { ChartDataPoint } from '@/types';

interface PauseChartProps {
  data: ChartDataPoint[];
  seuil?: number;
}

export function PauseChart({ data, seuil = 45 }: PauseChartProps) {
  const chartData = data.map(point => ({
    ...point,
    duree_pause: point.duree_pause || 0,
    color: (point.duree_pause || 0) >= seuil ? '#10b981' : '#ef4444',
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="date"
          tickFormatter={(value) => new Date(value).toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' })}
        />
        <YAxis label={{ value: 'Minutes', angle: -90, position: 'insideLeft' }} />
        <Tooltip
          labelFormatter={(label) => new Date(label).toLocaleDateString('fr-FR')}
          formatter={(value: number) => [`${value} min`, 'Durée de pause']}
        />
        <Legend />
        <ReferenceLine
          y={seuil}
          stroke="#f59e0b"
          strokeDasharray="3 3"
          label={{ value: `Seuil: ${seuil} min`, position: 'insideTopRight' }}
        />
        <Bar
          dataKey="duree_pause"
          name="Durée de pause"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
