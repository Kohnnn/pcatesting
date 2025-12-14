'use client';

import { useState, useMemo, useCallback, useRef } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Brush,
} from 'recharts';
import { VNIndexData } from '@/types';

interface MarketOverviewChartProps {
  data: VNIndexData[];
  title?: string;
}

type DateRange = '1M' | '3M' | '6M' | '1Y' | 'ALL';

export default function MarketOverviewChart({ data, title = 'VNIndex Performance' }: MarketOverviewChartProps) {
  const [dateRange, setDateRange] = useState<DateRange>('ALL');
  const chartRef = useRef<HTMLDivElement>(null);

  const filteredData = useMemo(() => {
    if (!data || data.length === 0) return [];
    
    const now = new Date();
    let startDate: Date;
    
    switch (dateRange) {
      case '1M':
        startDate = new Date(now.setMonth(now.getMonth() - 1));
        break;
      case '3M':
        startDate = new Date(now.setMonth(now.getMonth() - 3));
        break;
      case '6M':
        startDate = new Date(now.setMonth(now.getMonth() - 6));
        break;
      case '1Y':
        startDate = new Date(now.setFullYear(now.getFullYear() - 1));
        break;
      default:
        return data.map(d => ({
          ...d,
          dateFormatted: new Date(d.date).toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
        }));
    }
    
    return data
      .filter(d => new Date(d.date) >= startDate)
      .map(d => ({
        ...d,
        dateFormatted: new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      }));
  }, [data, dateRange]);


  const exportToCSV = useCallback(() => {
    if (!filteredData.length) return;
    
    const headers = ['Date', 'Close Index', 'Buy Volume', 'Sell Volume', 'Total Volume'];
    const csvContent = [
      headers.join(','),
      ...filteredData.map(d => 
        [d.date, d.close_index, d.buy_volume, d.sell_volume, d.total_volume].join(',')
      )
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `vnindex_${dateRange.toLowerCase()}_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [filteredData, dateRange]);

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
      link.download = `vnindex_${dateRange.toLowerCase()}_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }, [dateRange]);

  if (!data || data.length === 0) {
    return (
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex h-64 items-center justify-center text-gray-500">
          No data available
        </div>
      </div>
    );
  }

  const dateRangeOptions: DateRange[] = ['1M', '3M', '6M', '1Y', 'ALL'];

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex items-center gap-4">
          <div className="flex gap-1">
            {dateRangeOptions.map((range) => (
              <button
                key={range}
                onClick={() => setDateRange(range)}
                className={`rounded px-3 py-1 text-sm font-medium transition-colors ${
                  dateRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {range}
              </button>
            ))}
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
          <AreaChart data={filteredData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorIndex" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="dateFormatted"
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              tickFormatter={(value) => value.toLocaleString()}
              domain={['auto', 'auto']}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              }}
              formatter={(value: number) => [value.toLocaleString(), 'VNIndex']}
              labelFormatter={(label) => `Date: ${label}`}
            />
            <Area
              type="monotone"
              dataKey="close_index"
              stroke="#3b82f6"
              strokeWidth={2}
              fill="url(#colorIndex)"
            />
            {dateRange === 'ALL' && (
              <Brush
                dataKey="dateFormatted"
                height={30}
                stroke="#3b82f6"
                fill="#f3f4f6"
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
