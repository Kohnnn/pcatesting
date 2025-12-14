'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { formatNumber } from './chartUtils';

interface RealTimeChartProps {
  fetchData: () => Promise<{ value: number; timestamp: Date }>;
  interval?: number;
  maxDataPoints?: number;
  title?: string;
  yAxisLabel?: string;
  color?: string;
  height?: number;
}

export default function RealTimeChart({
  fetchData,
  interval = 5000,
  maxDataPoints = 50,
  title,
  yAxisLabel,
  color = '#3b82f6',
  height = 300,
}: RealTimeChartProps) {
  const [data, setData] = useState<Array<{ time: string; value: number }>>([]);
  const [isLive, setIsLive] = useState(true);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!isLive) return;

    const updateData = async () => {
      try {
        const newPoint = await fetchData();
        const timeStr = new Date(newPoint.timestamp).toLocaleTimeString();
        
        setData((prevData) => {
          const newData = [...prevData, { time: timeStr, value: newPoint.value }];
          return newData.slice(-maxDataPoints);
        });
      } catch (error) {
        console.error('Error fetching real-time data:', error);
      }
    };

    updateData();
    intervalRef.current = setInterval(updateData, interval);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isLive, fetchData, interval, maxDataPoints]);

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-4">
        {title && (
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        )}
        <button
          onClick={() => setIsLive(!isLive)}
          className={`px-3 py-1 rounded text-sm font-medium ${
            isLive
              ? 'bg-green-100 text-green-700'
              : 'bg-gray-100 text-gray-700'
          }`}
        >
          {isLive ? '● Live' : 'Paused'}
        </button>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="time"
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
            formatter={(value: any) => [formatNumber(value), 'Value']}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
