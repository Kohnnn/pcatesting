'use client';

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { formatDate, formatNumber } from './chartUtils';

interface TrendLineChartProps {
  data: Array<{
    date: string;
    value: number;
    [key: string]: any;
  }>;
  lines?: Array<{
    dataKey: string;
    name: string;
    color: string;
    strokeWidth?: number;
  }>;
  title?: string;
  yAxisLabel?: string;
  showGrid?: boolean;
  showLegend?: boolean;
  height?: number;
  referenceLines?: Array<{
    y: number;
    label: string;
    color: string;
  }>;
}

export default function TrendLineChart({
  data,
  lines = [{ dataKey: 'value', name: 'Value', color: '#3b82f6' }],
  title,
  yAxisLabel,
  showGrid = true,
  showLegend = true,
  height = 400,
  referenceLines = [],
}: TrendLineChartProps) {
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
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
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
          
          {/* Reference lines */}
          {referenceLines.map((refLine, index) => (
            <ReferenceLine
              key={index}
              y={refLine.y}
              label={refLine.label}
              stroke={refLine.color}
              strokeDasharray="3 3"
            />
          ))}
          
          {/* Data lines */}
          {lines.map((line, index) => (
            <Line
              key={index}
              type="monotone"
              dataKey={line.dataKey}
              name={line.name}
              stroke={line.color}
              strokeWidth={line.strokeWidth || 2}
              dot={false}
              activeDot={{ r: 6 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
