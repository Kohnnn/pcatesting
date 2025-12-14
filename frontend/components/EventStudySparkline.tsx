'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { EventStudyData } from '@/types';
import { useTheme } from '@/contexts/ThemeContext';

interface EventStudySparklineProps {
  data: EventStudyData;
  title: string;
  dataKey: 'car' | 'cas';
  color: string;
}

// Thesis terminology for event study metrics
const METRIC_DESCRIPTIONS: Record<string, string> = {
  car: 'CAR (Cumulative Abnormal Return)',
  cas: 'CAS (Cumulative Abnormal Sentiment)',
};

export default function EventStudySparkline({ data, title, dataKey, color }: EventStudySparklineProps) {
  const { theme } = useTheme();
  const isDark = theme === 'dark';
  
  const chartData = data.days.map((day, index) => ({
    day,
    value: data[dataKey][index],
  }));

  const metricLabel = METRIC_DESCRIPTIONS[dataKey] || title;

  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow">
      {title && <h4 className="mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">{title}</h4>}
      <p className="mb-2 text-xs text-gray-500 dark:text-gray-400">{metricLabel}</p>
      <ResponsiveContainer width="100%" height={150}>
        <LineChart data={chartData}>
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={isDark ? '#374151' : '#f0f0f0'} 
          />
          <XAxis 
            dataKey="day" 
            tick={{ fontSize: 10, fill: isDark ? '#9ca3af' : '#6b7280' }}
            label={{ 
              value: 'Days from Event (T)', 
              position: 'insideBottom', 
              offset: -5, 
              fontSize: 10,
              fill: isDark ? '#9ca3af' : '#6b7280'
            }}
            stroke={isDark ? '#4b5563' : '#d1d5db'}
          />
          <YAxis 
            tick={{ fontSize: 10, fill: isDark ? '#9ca3af' : '#6b7280' }}
            stroke={isDark ? '#4b5563' : '#d1d5db'}
          />
          <Tooltip 
            formatter={(value: number) => [value.toFixed(4), metricLabel]}
            labelFormatter={(label) => label === 0 ? 'Event Day (T=0)' : `T${label > 0 ? '+' : ''}${label}`}
            contentStyle={{
              backgroundColor: isDark ? '#1f2937' : '#ffffff',
              border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
              borderRadius: '0.5rem',
              color: isDark ? '#f9fafb' : '#111827',
            }}
          />
          <ReferenceLine 
            x={0} 
            stroke={isDark ? '#9ca3af' : '#666'} 
            strokeDasharray="3 3" 
            label={{ value: 'T=0', fontSize: 10, fill: isDark ? '#9ca3af' : '#666' }} 
          />
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke={color} 
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
