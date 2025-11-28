'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import type { ChartDataPoint } from '@/types';

interface DepartureChartProps {
  data: ChartDataPoint[];
  moyenne?: string;
}

export function DepartureChart({ data, moyenne }: DepartureChartProps) {
  // Convert time string to minutes for charting
  const convertTimeToMinutes = (time: string): number => {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  };

  // Convert minutes back to time string
  const convertMinutesToTime = (minutes: number): string => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
  };

  const chartData = data.map(point => ({
    ...point,
    heureMinutes: point.heure_depart ? convertTimeToMinutes(point.heure_depart) : 0,
  }));

  const moyenneMinutes = moyenne ? convertTimeToMinutes(moyenne) : undefined;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="date"
          tickFormatter={(value) => new Date(value).toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' })}
        />
        <YAxis
          tickFormatter={(value) => convertMinutesToTime(value)}
          domain={['dataMin - 30', 'dataMax + 30']}
        />
        <Tooltip
          labelFormatter={(label) => new Date(label).toLocaleDateString('fr-FR')}
          formatter={(value: number) => [convertMinutesToTime(value), 'Heure de départ']}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="heureMinutes"
          name="Heure de départ"
          stroke="#10b981"
          strokeWidth={2}
          dot={{ r: 4 }}
        />
        {moyenneMinutes && (
          <ReferenceLine
            y={moyenneMinutes}
            stroke="#ef4444"
            strokeDasharray="3 3"
            label={{ value: `Moyenne: ${moyenne}`, position: 'insideTopRight' }}
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
}
