'use client';

import { useState, useMemo, useCallback, useRef } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { TradingSignal } from '@/types';

interface SignalDistributionChartProps {
  signals: TradingSignal[];
  chartType?: 'pie' | 'bar';
  title?: string;
}

const SIGNAL_COLORS: Record<string, string> = {
  'Contrarian Dip Buy': '#10b981',
  'Momentum Breakout': '#3b82f6',
  'Retail Trap': '#ef4444',
  'Neutral / No Edge': '#9ca3af',
};

// Signal type descriptions aligned with thesis findings
const SIGNAL_DESCRIPTIONS: Record<string, string> = {
  'Contrarian Dip Buy': 'Downgrade with high sentiment and positive NFB - exploits the "Downgrade Puzzle"',
  'Momentum Breakout': 'Upgrade with rising sentiment and RSI below overbought levels',
  'Retail Trap': 'Downgrade with high BSI but negative NFB - retail investors trapped',
  'Neutral / No Edge': 'No clear statistical edge based on thesis methodology',
};

export default function SignalDistributionChart({
  signals,
  chartType: initialChartType = 'pie',
  title = 'Signal Distribution',
}: SignalDistributionChartProps) {
  const [chartType, setChartType] = useState<'pie' | 'bar'>(initialChartType);
  const chartRef = useRef<HTMLDivElement>(null);

  const distributionData = useMemo(() => {
    if (!signals || signals.length === 0) return [];
    
    const counts: Record<string, number> = {};
    signals.forEach((signal) => {
      const type = signal.signal_type || 'Unknown';
      counts[type] = (counts[type] || 0) + 1;
    });
    
    const total = signals.length;
    return Object.entries(counts).map(([name, count]) => ({
      name,
      count,
      percentage: ((count / total) * 100).toFixed(1),
      color: SIGNAL_COLORS[name] || '#6b7280',
      description: SIGNAL_DESCRIPTIONS[name] || '',
    }));
  }, [signals]);


  const exportToCSV = useCallback(() => {
    if (!distributionData.length) return;
    
    const headers = ['Signal Type', 'Count', 'Percentage'];
    const csvContent = [
      headers.join(','),
      ...distributionData.map((d) => [d.name, d.count, d.percentage].join(',')),
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `signal_distribution_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [distributionData]);

  const exportToImage = useCallback(() => {
    if (!chartRef.current) return;
    
    const svg = chartRef.current.querySelector('svg');
    if (!svg) return;
    
    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx?.drawImage(img, 0, 0);
      const link = document.createElement('a');
      link.download = `signal_distribution_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }, []);

  if (!signals || signals.length === 0) {
    return (
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex h-64 items-center justify-center text-gray-500">
          No signal data available
        </div>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: typeof distributionData[0] }> }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="rounded-lg border border-gray-200 bg-white p-3 shadow-lg">
          <p className="font-semibold" style={{ color: data.color }}>
            {data.name}
          </p>
          <p className="text-sm text-gray-600">{data.description}</p>
          <p className="mt-1 text-sm">
            <span className="font-medium">{data.count}</span> signals ({data.percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex items-center gap-4">
          <div className="flex gap-1">
            <button
              onClick={() => setChartType('pie')}
              className={`rounded px-3 py-1 text-sm font-medium transition-colors ${
                chartType === 'pie'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Pie
            </button>
            <button
              onClick={() => setChartType('bar')}
              className={`rounded px-3 py-1 text-sm font-medium transition-colors ${
                chartType === 'bar'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Bar
            </button>
          </div>
          <div className="flex gap-2">
            <button
              onClick={exportToCSV}
              className="rounded bg-gray-100 px-3 py-1 text-sm text-gray-600 hover:bg-gray-200"
              title="Export to CSV"
            >
              CSV
            </button>
            <button
              onClick={exportToImage}
              className="rounded bg-gray-100 px-3 py-1 text-sm text-gray-600 hover:bg-gray-200"
              title="Export to Image"
            >
              PNG
            </button>
          </div>
        </div>
      </div>

      <div ref={chartRef}>
        <ResponsiveContainer width="100%" height={350}>
          {chartType === 'pie' ? (
            <PieChart>
              <Pie
                data={distributionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="count"
              >
                {distributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend
                formatter={(value) => (
                  <span className="text-sm text-gray-700">{value}</span>
                )}
              />
            </PieChart>
          ) : (
            <BarChart data={distributionData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 11, fill: '#6b7280' }}
                tickLine={{ stroke: '#e5e7eb' }}
                angle={-20}
                textAnchor="end"
                height={80}
              />
              <YAxis
                tick={{ fontSize: 11, fill: '#6b7280' }}
                tickLine={{ stroke: '#e5e7eb' }}
                label={{
                  value: 'Count',
                  angle: -90,
                  position: 'insideLeft',
                  fontSize: 12,
                  fill: '#6b7280',
                }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {distributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>

      {/* Summary Stats */}
      <div className="mt-4 grid grid-cols-2 gap-4 border-t pt-4 md:grid-cols-4">
        {distributionData.map((item) => (
          <div key={item.name} className="text-center">
            <div
              className="text-2xl font-bold"
              style={{ color: item.color }}
            >
              {item.count}
            </div>
            <div className="text-xs text-gray-500">{item.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
