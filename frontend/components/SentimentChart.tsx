'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { DailySentiment } from '@/types';
import { useTheme } from '@/contexts/ThemeContext';
import Tooltip, { InfoIcon, TOOLTIP_CONTENT } from './Tooltip';

interface SentimentChartProps {
  data: DailySentiment[];
}

// Thesis terminology for sentiment indicators
const INDICATOR_LABELS = {
  RSI: 'RSI (Relative Strength Index)',
  BSI: 'BSI (Buy-Sell Imbalance)',
  'Pure Sentiment': 'Pure Sentiment (Market-Adjusted)',
};

export default function SentimentChart({ data }: SentimentChartProps) {
  const { theme } = useTheme();
  const isDark = theme === 'dark';
  
  const chartData = data.map(d => ({
    date: new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    RSI: d.rsi,
    BSI: d.bsi ? d.bsi * 100 : null, // Scale BSI to 0-100 for better visualization
    'Pure Sentiment': d.pure_sentiment,
  }));

  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow">
      <div className="flex items-center gap-2 mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Sentiment Indicators</h3>
        <Tooltip content={TOOLTIP_CONTENT.PCA_SENTIMENT}>
          <InfoIcon />
        </Tooltip>
      </div>
      <div className="flex flex-wrap gap-4 mb-4 text-xs">
        <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
          <span className="w-3 h-3 rounded-full bg-[#8884d8]"></span>
          RSI
          <Tooltip content={TOOLTIP_CONTENT.RSI}>
            <InfoIcon className="w-3 h-3" />
          </Tooltip>
        </span>
        <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
          <span className="w-3 h-3 rounded-full bg-[#82ca9d]"></span>
          BSI
          <Tooltip content={TOOLTIP_CONTENT.BSI}>
            <InfoIcon className="w-3 h-3" />
          </Tooltip>
        </span>
        <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
          <span className="w-3 h-3 rounded-full bg-[#ffc658]"></span>
          Pure Sentiment
          <Tooltip content={TOOLTIP_CONTENT.PURE_SENTIMENT}>
            <InfoIcon className="w-3 h-3" />
          </Tooltip>
        </span>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={isDark ? '#374151' : '#e5e7eb'}
          />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12, fill: isDark ? '#9ca3af' : '#6b7280' }}
            interval="preserveStartEnd"
            stroke={isDark ? '#4b5563' : '#d1d5db'}
          />
          <YAxis 
            tick={{ fontSize: 12, fill: isDark ? '#9ca3af' : '#6b7280' }}
            stroke={isDark ? '#4b5563' : '#d1d5db'}
          />
          <RechartsTooltip 
            formatter={(value: number, name: string) => [
              value?.toFixed(2) ?? 'N/A',
              INDICATOR_LABELS[name as keyof typeof INDICATOR_LABELS] || name
            ]}
            contentStyle={{
              backgroundColor: isDark ? '#1f2937' : '#ffffff',
              border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
              borderRadius: '0.5rem',
              color: isDark ? '#f9fafb' : '#111827',
            }}
          />
          <Legend 
            formatter={(value) => INDICATOR_LABELS[value as keyof typeof INDICATOR_LABELS] || value}
            wrapperStyle={{ color: isDark ? '#d1d5db' : '#374151' }}
          />
          <Line 
            type="monotone" 
            dataKey="RSI" 
            name="RSI"
            stroke="#8884d8" 
            strokeWidth={2}
            dot={false}
          />
          <Line 
            type="monotone" 
            dataKey="BSI" 
            name="BSI"
            stroke="#82ca9d" 
            strokeWidth={2}
            dot={false}
          />
          <Line 
            type="monotone" 
            dataKey="Pure Sentiment" 
            name="Pure Sentiment"
            stroke="#ffc658" 
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
