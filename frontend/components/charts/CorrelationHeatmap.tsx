'use client';

import { useMemo, useCallback, useRef } from 'react';
import { CorrelationMatrix } from '@/types';

interface CorrelationHeatmapProps {
  data: CorrelationMatrix;
  title?: string;
}

const PROXY_DESCRIPTIONS: Record<string, string> = {
  BSI: 'Buy-Sell Imbalance',
  ATR: 'Adjusted Turnover Ratio',
  LTV: 'Log Trading Volume',
  RSI: 'Relative Strength Index',
  PLI: 'Psychological Line Index',
};

// Color interpolation for correlation values (-1 to 1)
function getCorrelationColor(value: number): string {
  if (value === null || value === undefined || isNaN(value)) return '#f3f4f6';
  
  // Clamp value between -1 and 1
  const v = Math.max(-1, Math.min(1, value));
  
  if (v < 0) {
    // Negative correlation: blue
    const intensity = Math.abs(v);
    const r = Math.round(239 - intensity * 180);
    const g = Math.round(246 - intensity * 180);
    const b = Math.round(255);
    return `rgb(${r}, ${g}, ${b})`;
  } else {
    // Positive correlation: red
    const intensity = v;
    const r = 255;
    const g = Math.round(239 - intensity * 180);
    const b = Math.round(239 - intensity * 180);
    return `rgb(${r}, ${g}, ${b})`;
  }
}

export default function CorrelationHeatmap({
  data,
  title = 'Sentiment Proxy Correlations',
}: CorrelationHeatmapProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  const { labels, values } = data || { labels: [], values: [] };

  const exportToCSV = useCallback(() => {
    if (!labels.length || !values.length) return;
    
    const headers = ['', ...labels];
    const csvContent = [
      headers.join(','),
      ...values.map((row, i) => [labels[i], ...row.map((v) => v?.toFixed(4) || '')].join(',')),
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `correlation_matrix_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [labels, values]);


  const exportToImage = useCallback(() => {
    if (!chartRef.current) return;
    
    // For the heatmap, we'll create a canvas directly
    const container = chartRef.current;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const cellSize = 80;
    const labelWidth = 100;
    const padding = 20;
    const width = labelWidth + labels.length * cellSize + padding * 2;
    const height = labelWidth + labels.length * cellSize + padding * 2;
    
    canvas.width = width;
    canvas.height = height;
    
    // White background
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
    
    // Draw cells
    ctx.font = '12px sans-serif';
    labels.forEach((rowLabel, i) => {
      // Row label
      ctx.fillStyle = '#374151';
      ctx.textAlign = 'right';
      ctx.fillText(rowLabel, labelWidth - 10 + padding, labelWidth + i * cellSize + cellSize / 2 + 4 + padding);
      
      // Column label
      ctx.save();
      ctx.translate(labelWidth + i * cellSize + cellSize / 2 + padding, labelWidth - 10 + padding);
      ctx.rotate(-Math.PI / 4);
      ctx.textAlign = 'right';
      ctx.fillText(rowLabel, 0, 0);
      ctx.restore();
      
      labels.forEach((_, j) => {
        const value = values[i]?.[j];
        const x = labelWidth + j * cellSize + padding;
        const y = labelWidth + i * cellSize + padding;
        
        // Cell background
        ctx.fillStyle = getCorrelationColor(value);
        ctx.fillRect(x, y, cellSize - 2, cellSize - 2);
        
        // Cell value
        ctx.fillStyle = Math.abs(value) > 0.5 ? 'white' : '#374151';
        ctx.textAlign = 'center';
        ctx.fillText(value?.toFixed(2) || '', x + cellSize / 2, y + cellSize / 2 + 4);
      });
    });
    
    const link = document.createElement('a');
    link.download = `correlation_heatmap_${new Date().toISOString().split('T')[0]}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  }, [labels, values]);

  if (!labels.length || !values.length) {
    return (
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex h-64 items-center justify-center text-gray-500">
          No correlation data available
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

      {/* Color Scale Legend */}
      <div className="mb-4 flex items-center justify-center gap-2">
        <span className="text-sm text-gray-600">-1.0</span>
        <div className="flex h-4 w-48 overflow-hidden rounded">
          {Array.from({ length: 20 }).map((_, i) => (
            <div
              key={i}
              className="flex-1"
              style={{ backgroundColor: getCorrelationColor((i - 10) / 10) }}
            />
          ))}
        </div>
        <span className="text-sm text-gray-600">+1.0</span>
        <span className="ml-4 text-xs text-gray-500">
          (Blue = Negative, Red = Positive)
        </span>
      </div>

      <div ref={chartRef} className="overflow-x-auto">
        <table className="mx-auto border-collapse">
          <thead>
            <tr>
              <th className="p-2" />
              {labels.map((label) => (
                <th
                  key={label}
                  className="p-2 text-center text-sm font-medium text-gray-700"
                  title={PROXY_DESCRIPTIONS[label] || label}
                >
                  <div className="flex flex-col items-center">
                    <span>{label}</span>
                    <span className="text-xs font-normal text-gray-400">
                      {PROXY_DESCRIPTIONS[label]?.split(' ').map(w => w[0]).join('') || ''}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {labels.map((rowLabel, i) => (
              <tr key={rowLabel}>
                <th
                  className="p-2 text-right text-sm font-medium text-gray-700"
                  title={PROXY_DESCRIPTIONS[rowLabel] || rowLabel}
                >
                  {rowLabel}
                </th>
                {labels.map((colLabel, j) => {
                  const value = values[i]?.[j];
                  const isDiagonal = i === j;
                  return (
                    <td
                      key={colLabel}
                      className="relative p-0"
                      title={`${rowLabel} vs ${colLabel}: ${value?.toFixed(4) || 'N/A'}`}
                    >
                      <div
                        className={`flex h-16 w-16 items-center justify-center text-sm font-medium transition-transform hover:scale-105 ${
                          isDiagonal ? 'ring-2 ring-gray-300' : ''
                        }`}
                        style={{
                          backgroundColor: getCorrelationColor(value),
                          color: Math.abs(value) > 0.5 ? 'white' : '#374151',
                        }}
                      >
                        {value?.toFixed(2) || '-'}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Interpretation Guide */}
      <div className="mt-4 border-t pt-4">
        <h4 className="mb-2 text-sm font-semibold text-gray-700">Interpretation Guide</h4>
        <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 md:grid-cols-4">
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded" style={{ backgroundColor: getCorrelationColor(0.8) }} />
            <span>Strong Positive (0.7 to 1.0)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded" style={{ backgroundColor: getCorrelationColor(0.4) }} />
            <span>Moderate Positive (0.3 to 0.7)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded" style={{ backgroundColor: getCorrelationColor(-0.4) }} />
            <span>Moderate Negative (-0.7 to -0.3)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded" style={{ backgroundColor: getCorrelationColor(-0.8) }} />
            <span>Strong Negative (-1.0 to -0.7)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
