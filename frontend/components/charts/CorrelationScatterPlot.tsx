'use client';

import React from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
  Legend,
} from 'recharts';
import { formatNumber } from './chartUtils';

interface CorrelationScatterPlotProps {
  data: Array<{
    x: number;
    y: number;
    name?: string;
    size?: number;
    [key: string]: any;
  }>;
  title?: string;
  xAxisLabel?: string;
  yAxisLabel?: string;
  showGrid?: boolean;
  showTrendLine?: boolean;
  height?: number;
  color?: string;
  sizeRange?: [number, number];
}

export default function CorrelationScatterPlot({
  data,
  title,
  xAxisLabel,
  yAxisLabel,
  showGrid = true,
  showTrendLine = false,
  height = 400,
  color = '#3b82f6',
  sizeRange = [50, 400],
}: CorrelationScatterPlotProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  // Calculate trend line if requested
  let trendLineData: Array<{ x: number; y: number }> = [];
  if (showTrendLine && data.length > 1) {
    const n = data.length;
    const sumX = data.reduce((sum, point) => sum + point.x, 0);
    const sumY = data.reduce((sum, point) => sum + point.y, 0);
    const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);
    const sumX2 = data.reduce((sum, point) => sum + point.x * point.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const minX = Math.min(...data.map((p) => p.x));
    const maxX = Math.max(...data.map((p) => p.x));

    trendLineData = [
      { x: minX, y: slope * minX + intercept },
      { x: maxX, y: slope * maxX + intercept },
    ];
  }

  // Calculate correlation coefficient
  const calculateCorrelation = () => {
    const n = data.length;
    const sumX = data.reduce((sum, point) => sum + point.x, 0);
    const sumY = data.reduce((sum, point) => sum + point.y, 0);
    const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);
    const sumX2 = data.reduce((sum, point) => sum + point.x * point.x, 0);
    const sumY2 = data.reduce((sum, point) => sum + point.y * point.y, 0);

    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt(
      (n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY)
    );

    return denominator === 0 ? 0 : numerator / denominator;
  };

  const correlation = calculateCorrelation();

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-lg">
          {data.name && (
            <p className="font-semibold text-gray-900 mb-1">{data.name}</p>
          )}
          <p className="text-sm text-gray-600">
            {xAxisLabel || 'X'}: {formatNumber(data.x)}
          </p>
          <p className="text-sm text-gray-600">
            {yAxisLabel || 'Y'}: {formatNumber(data.y)}
          </p>
          {data.size && (
            <p className="text-sm text-gray-600">
              Size: {formatNumber(data.size)}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-4">
        {title && (
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        )}
        {showTrendLine && (
          <div className="text-sm text-gray-600">
            Correlation: <span className="font-semibold">{correlation.toFixed(3)}</span>
          </div>
        )}
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <ScatterChart margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          {showGrid && (
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          )}
          <XAxis
            type="number"
            dataKey="x"
            name={xAxisLabel || 'X'}
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
            type="number"
            dataKey="y"
            name={yAxisLabel || 'Y'}
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
          <ZAxis
            type="number"
            dataKey="size"
            range={sizeRange}
            name="Size"
          />
          <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
          <Legend />
          
          {/* Trend line */}
          {showTrendLine && trendLineData.length > 0 && (
            <Scatter
              name="Trend"
              data={trendLineData}
              fill="none"
              line={{ stroke: '#ef4444', strokeWidth: 2, strokeDasharray: '5 5' }}
              shape={false}
            />
          )}
          
          {/* Data points */}
          <Scatter
            name="Data Points"
            data={data}
            fill={color}
            fillOpacity={0.6}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
