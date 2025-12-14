'use client';

import { useState, useMemo, useCallback, useRef } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { DailySentiment } from '@/types';

interface SentimentProxyChartProps {
  data: DailySentiment[];
  title?: string;
  showLegend?: boolean;
}

type ProxyKey = 'bsi' | 'atr' | 'ltv' | 'rsi' | 'pli';

interface ProxyConfig {
  key: ProxyKey;
  label: string;
  color: string;
  description: string;
}

const PROXY_CONFIGS: ProxyConfig[] = [
  { key: 'bsi', label: 'BSI', color: '#3b82f6', description: 'Buy-Sell Imbalance' },
  { key: 'atr', label: 'ATR', color: '#10b981', description: 'Adjusted Turnover Ratio' },
  { key: 'ltv', label: 'LTV', color: '#f59e0b', description: 'Log Trading Volume' },
  { key: 'rsi', label: 'RSI', color: '#8b5cf6', description: 'Relative Strength Index' },
  { key: 'pli', label: 'PLI', color: '#ef4444', description: 'Psychological Line Index' },
];

export default function SentimentProxyChart({
  data,
  title = 'Sentiment Proxies',
  showLegend = true,
}: SentimentProxyChartProps) {
  const [activeProxies, setActiveProxies] = useState<Set<ProxyKey>>(
    new Set(['bsi', 'rsi', 'pli'])
  );
  const chartRef = useRef<HTMLDivElement>(null);

  const toggleProxy = (proxy: ProxyKey) => {
    setActiveProxies((prev) => {
      const next = new Set(prev);
      if (next.has(proxy)) {
        next.delete(proxy);
      } else {
        next.add(proxy);
      }
      return next;
    });
  };


  const chartData = useMemo(() => {
    if (!data || data.length === 0) return [];
    
    return data.map((d) => ({
      date: new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      fullDate: d.date,
      bsi: d.bsi !== null ? d.bsi * 100 : null, // Scale to 0-100
      atr: d.atr,
      ltv: d.ltv,
      rsi: d.rsi,
      pli: d.pli !== null ? d.pli * 100 : null, // Scale to 0-100
    }));
  }, [data]);

  const exportToCSV = useCallback(() => {
    if (!data.length) return;
    
    const headers = ['Date', 'BSI', 'ATR', 'LTV', 'RSI', 'PLI'];
    const csvContent = [
      headers.join(','),
      ...data.map((d) =>
        [d.date, d.bsi, d.atr, d.ltv, d.rsi, d.pli].join(',')
      ),
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `sentiment_proxies_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [data]);

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
      link.download = `sentiment_proxies_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }, []);

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

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
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

      {/* Proxy Toggles */}
      <div className="mb-4 flex flex-wrap gap-2">
        {PROXY_CONFIGS.map((config) => (
          <button
            key={config.key}
            onClick={() => toggleProxy(config.key)}
            className={`flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium transition-all ${
              activeProxies.has(config.key)
                ? 'bg-opacity-100 text-white'
                : 'bg-gray-100 text-gray-500'
            }`}
            style={{
              backgroundColor: activeProxies.has(config.key) ? config.color : undefined,
            }}
            title={config.description}
          >
            <span
              className="h-2 w-2 rounded-full"
              style={{ backgroundColor: config.color }}
            />
            {config.label}
          </button>
        ))}
      </div>

      <div ref={chartRef}>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              domain={['auto', 'auto']}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              }}
              formatter={(value: number, name: string) => {
                const config = PROXY_CONFIGS.find((c) => c.key === name.toLowerCase());
                return [value?.toFixed(2) ?? 'N/A', config?.description ?? name];
              }}
            />
            {showLegend && <Legend />}
            {PROXY_CONFIGS.map((config) =>
              activeProxies.has(config.key) ? (
                <Line
                  key={config.key}
                  type="monotone"
                  dataKey={config.key}
                  name={config.label}
                  stroke={config.color}
                  strokeWidth={2}
                  dot={false}
                  connectNulls
                />
              ) : null
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
