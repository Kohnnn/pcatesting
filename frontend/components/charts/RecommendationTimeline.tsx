'use client';

import { useMemo, useCallback, useRef } from 'react';
import {
  ComposedChart,
  Line,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { AnalystRecommendation } from '@/types';

interface RecommendationTimelineProps {
  ticker: string;
  recommendations: AnalystRecommendation[];
  title?: string;
}

const RATING_LABELS: Record<number, string> = {
  5: 'Buy',
  4: 'Overweight',
  3: 'Hold',
  2: 'Underweight',
  1: 'Sell',
};

const RATING_COLORS: Record<number, string> = {
  5: '#10b981', // Green
  4: '#22c55e', // Light green
  3: '#f59e0b', // Yellow
  2: '#f97316', // Orange
  1: '#ef4444', // Red
};

export default function RecommendationTimeline({
  ticker,
  recommendations,
  title,
}: RecommendationTimelineProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  const chartData = useMemo(() => {
    if (!recommendations || recommendations.length === 0) return [];
    
    // Sort by date
    const sorted = [...recommendations].sort(
      (a, b) => new Date(a.issue_date).getTime() - new Date(b.issue_date).getTime()
    );
    
    return sorted.map((rec, index) => ({
      date: new Date(rec.issue_date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: '2-digit',
      }),
      fullDate: rec.issue_date,
      rating: rec.rating_numeric,
      ratingLabel: RATING_LABELS[rec.rating_numeric] || 'Unknown',
      originalRating: rec.recommendation,
      analyst: rec.analyst_name,
      firm: rec.analyst_firm,
      targetPrice: rec.target_price,
      color: RATING_COLORS[rec.rating_numeric] || '#6b7280',
      // Calculate change from previous
      change: index > 0 ? rec.rating_numeric - sorted[index - 1].rating_numeric : 0,
    }));
  }, [recommendations]);


  const exportToCSV = useCallback(() => {
    if (!chartData.length) return;
    
    const headers = ['Date', 'Rating', 'Rating Label', 'Original Rating', 'Analyst', 'Firm', 'Target Price'];
    const csvContent = [
      headers.join(','),
      ...chartData.map((d) =>
        [d.fullDate, d.rating, d.ratingLabel, `"${d.originalRating}"`, `"${d.analyst}"`, `"${d.firm}"`, d.targetPrice || ''].join(',')
      ),
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `recommendations_${ticker}_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [chartData, ticker]);

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
      link.download = `recommendations_${ticker}_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }, [ticker]);

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="text-lg font-semibold text-gray-900">
          {title || `Recommendation Timeline - ${ticker}`}
        </h3>
        <div className="flex h-64 items-center justify-center text-gray-500">
          No recommendation data available
        </div>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: typeof chartData[0] }> }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="rounded-lg border border-gray-200 bg-white p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{data.fullDate}</p>
          <div className="mt-2 space-y-1 text-sm">
            <p>
              <span className="text-gray-500">Rating:</span>{' '}
              <span className="font-medium" style={{ color: data.color }}>
                {data.ratingLabel} ({data.rating})
              </span>
            </p>
            <p>
              <span className="text-gray-500">Original:</span>{' '}
              <span className="font-medium">{data.originalRating}</span>
            </p>
            <p>
              <span className="text-gray-500">Analyst:</span>{' '}
              <span className="font-medium">{data.analyst}</span>
            </p>
            <p>
              <span className="text-gray-500">Firm:</span>{' '}
              <span className="font-medium">{data.firm}</span>
            </p>
            {data.targetPrice && (
              <p>
                <span className="text-gray-500">Target:</span>{' '}
                <span className="font-medium">
                  {data.targetPrice.toLocaleString()} VND
                </span>
              </p>
            )}
            {data.change !== 0 && (
              <p>
                <span className="text-gray-500">Change:</span>{' '}
                <span
                  className={`font-medium ${
                    data.change > 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {data.change > 0 ? '+' : ''}{data.change}
                </span>
              </p>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          {title || `Recommendation Timeline - ${ticker}`}
        </h3>
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

      {/* Rating Scale Legend */}
      <div className="mb-4 flex items-center justify-center gap-4 text-sm">
        {[5, 4, 3, 2, 1].map((rating) => (
          <div key={rating} className="flex items-center gap-1">
            <div
              className="h-3 w-3 rounded-full"
              style={{ backgroundColor: RATING_COLORS[rating] }}
            />
            <span className="text-gray-600">
              {rating} - {RATING_LABELS[rating]}
            </span>
          </div>
        ))}
      </div>

      <div ref={chartRef}>
        <ResponsiveContainer width="100%" height={350}>
          <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            
            {/* Reference lines for rating levels */}
            {[1, 2, 3, 4, 5].map((level) => (
              <ReferenceLine
                key={level}
                y={level}
                stroke="#e5e7eb"
                strokeDasharray="3 3"
              />
            ))}
            
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis
              domain={[0.5, 5.5]}
              ticks={[1, 2, 3, 4, 5]}
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              tickFormatter={(value) => RATING_LABELS[value] || ''}
              width={80}
            />
            <Tooltip content={<CustomTooltip />} />
            
            {/* Line connecting ratings */}
            <Line
              type="stepAfter"
              dataKey="rating"
              stroke="#6b7280"
              strokeWidth={2}
              dot={false}
              connectNulls
            />
            
            {/* Scatter points for each recommendation */}
            <Scatter
              dataKey="rating"
              fill="#3b82f6"
              shape={(props: unknown) => {
                const { cx, cy, payload } = props as { cx: number; cy: number; payload: typeof chartData[0] };
                return (
                  <circle
                    cx={cx}
                    cy={cy}
                    r={8}
                    fill={payload.color}
                    stroke="#fff"
                    strokeWidth={2}
                  />
                );
              }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Recommendations Table */}
      <div className="mt-4 border-t pt-4">
        <h4 className="mb-2 text-sm font-semibold text-gray-700">Recent Recommendations</h4>
        <div className="max-h-48 overflow-y-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-2 py-1 text-left text-gray-600">Date</th>
                <th className="px-2 py-1 text-left text-gray-600">Rating</th>
                <th className="px-2 py-1 text-left text-gray-600">Analyst</th>
                <th className="px-2 py-1 text-left text-gray-600">Firm</th>
              </tr>
            </thead>
            <tbody>
              {chartData.slice(-5).reverse().map((rec, index) => (
                <tr key={index} className="border-b border-gray-100">
                  <td className="px-2 py-1">{rec.date}</td>
                  <td className="px-2 py-1">
                    <span
                      className="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium text-white"
                      style={{ backgroundColor: rec.color }}
                    >
                      {rec.ratingLabel}
                    </span>
                  </td>
                  <td className="px-2 py-1 text-gray-600">{rec.analyst}</td>
                  <td className="px-2 py-1 text-gray-600">{rec.firm}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
