'use client';

import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatDate, formatNumber } from './chartUtils';

interface CumulativeAreaChartProps {
  data: Array<{
    date: string;
    [key: string]: any;
  }>;
  areas?: Array<{
    dataKey: string;
    name: string;
    color: string;
    stackId?: string;
  }>;
  title?: string;
  yAxisLabel?: string;
  showGrid?: boolean;
  showLegend?: boolean;
  height?: number;
  stacked?: boolean;
}

export default function CumulativeAreaChart({
  data,
  areas = [{ dataKey: 'value', name: 'Value', color: '#3b82f6' }],
  title,
  yAxisLabel,
  showGrid = true,
  showLegend = true,
  height = 400,
  stacked = false,
}: CumulativeAreaChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-gray-900">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            {areas.map((area, index) => (
              <linearGradient
                key={index}
                id={`color${index}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="5%" stopColor={area.color} stopOpacity={0.8} />
                <stop offset="95%" stopColor={area.color} stopOpacity={0.1} />
              </linearGradient>
            ))}
          </defs>
          {showGrid && (
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          )}
          <XAxis
            dataKey="date"
            tickFormatter={(value) => formatDate(value)}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis
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
            tickFormatter={(value) => formatNumber(value)}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px',
            }}
            labelFormatter={(value) => formatDate(value)}
            formatter={(value: any) => [formatNumber(value), '']}
          />
          {showLegend && <Legend />}
          
          {areas.map((area, index) => (
            <Area
              key={index}
              type="monotone"
              dataKey={area.dataKey}
              name={area.name}
              stackId={stacked ? (area.stackId || '1') : undefined}
              stroke={area.color}
              fill={`url(#color${index})`}
              fillOpacity={1}
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
