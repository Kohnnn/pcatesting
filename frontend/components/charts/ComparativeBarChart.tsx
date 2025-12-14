'use client';

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { formatNumber } from './chartUtils';

interface ComparativeBarChartProps {
  data: Array<{
    name: string;
    [key: string]: any;
  }>;
  bars?: Array<{
    dataKey: string;
    name: string;
    color: string;
  }>;
  title?: string;
  yAxisLabel?: string;
  xAxisLabel?: string;
  showGrid?: boolean;
  showLegend?: boolean;
  height?: number;
  horizontal?: boolean;
  colorByValue?: boolean;
  thresholds?: {
    positive: number;
    negative: number;
  };
}

export default function ComparativeBarChart({
  data,
  bars = [{ dataKey: 'value', name: 'Value', color: '#3b82f6' }],
  title,
  yAxisLabel,
  xAxisLabel,
  showGrid = true,
  showLegend = true,
  height = 400,
  horizontal = false,
  colorByValue = false,
  thresholds = { positive: 0, negative: 0 },
}: ComparativeBarChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const getBarColor = (value: number) => {
    if (!colorByValue) return bars[0].color;
    if (value > thresholds.positive) return '#10b981'; // green
    if (value < thresholds.negative) return '#ef4444'; // red
    return '#f59e0b'; // amber
  };

  const ChartComponent = horizontal ? BarChart : BarChart;
  const layout = horizontal ? 'horizontal' : 'vertical';

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-gray-900">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <ChartComponent
          data={data}
          layout={layout}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          {showGrid && (
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          )}
          
          {horizontal ? (
            <>
              <XAxis
                type="number"
                tickFormatter={(value) => formatNumber(value)}
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={
                  xAxisLabel
                    ? {
                        value: xAxisLabel,
                        position: 'insideBottom',
                        offset: -5,
                        style: { fontSize: '12px', fill: '#6b7280' },
                      }
                    : undefined
                }
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                width={100}
              />
            </>
          ) : (
            <>
              <XAxis
                dataKey="name"
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={
                  xAxisLabel
                    ? {
                        value: xAxisLabel,
                        position: 'insideBottom',
                        offset: -5,
                        style: { fontSize: '12px', fill: '#6b7280' },
                      }
                    : undefined
                }
              />
              <YAxis
                tickFormatter={(value) => formatNumber(value)}
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={
                  yAxisLabel
                    ? {
                        value: yAxisLabel,
                        angle: -90,
                        position: 'insideLeft',
                        style: { fontSize: '12px', fill: '#6b7280' },
                      }
                    : undefined
                }
              />
            </>
          )}
          
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px',
            }}
            formatter={(value: any) => [formatNumber(value), '']}
          />
          {showLegend && <Legend />}
          
          {bars.map((bar, index) => (
            <Bar
              key={index}
              dataKey={bar.dataKey}
              name={bar.name}
              fill={bar.color}
              radius={[4, 4, 0, 0]}
            >
              {colorByValue && (
                data.map((entry, idx) => (
                  <Cell key={`cell-${idx}`} fill={getBarColor(entry[bar.dataKey])} />
                ))
              )}
            </Bar>
          ))}
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  );
}
