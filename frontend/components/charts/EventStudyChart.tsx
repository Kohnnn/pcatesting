'use client';

import { useMemo, useCallback, useRef } from 'react';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceArea,
} from 'recharts';
import { EventStudyData } from '@/types';

interface EventStudyChartProps {
  data: EventStudyData;
  eventDate?: string;
  windowSize?: number;
  title?: string;
}

export default function EventStudyChart({
  data,
  eventDate,
  windowSize = 25,
  title = 'Event Study Analysis',
}: EventStudyChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);

  const chartData = useMemo(() => {
    if (!data || !data.days || data.days.length === 0) return [];
    
    return data.days.map((day, index) => ({
      day,
      dayLabel: day === 0 ? 'T=0' : day > 0 ? `T+${day}` : `T${day}`,
      car: data.car[index],
      cas: data.cas[index],
      isEventDay: day === 0,
      isPreEvent: day < 0,
      isPostEvent: day > 0,
    }));
  }, [data]);

  const exportToCSV = useCallback(() => {
    if (!chartData.length) return;
    
    const headers = ['Day', 'CAR', 'CAS'];
    const csvContent = [
      headers.join(','),
      ...chartData.map((d) => [d.day, d.car, d.cas].join(',')),
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `event_study_${eventDate || 'data'}_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }, [chartData, eventDate]);


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
      link.download = `event_study_${eventDate || 'data'}_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }, [eventDate]);

  if (!data || !data.days || data.days.length === 0) {
    return (
      <div className="rounded-lg bg-white p-6 shadow">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex h-64 items-center justify-center text-gray-500">
          No event study data available
        </div>
      </div>
    );
  }

  // Calculate min/max for better axis scaling
  const allValues = [...data.car, ...data.cas].filter((v) => v !== null && v !== undefined);
  const minValue = Math.min(...allValues);
  const maxValue = Math.max(...allValues);
  const padding = (maxValue - minValue) * 0.1;

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {eventDate && (
            <p className="text-sm text-gray-500">Event Date: {eventDate}</p>
          )}
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

      {/* Event Window Legend */}
      <div className="mb-4 flex items-center gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="h-3 w-6 rounded bg-blue-100" />
          <span className="text-gray-600">Pre-Event Window (T-{windowSize} to T-1)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-red-500" />
          <span className="text-gray-600">Event Day (T=0)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-6 rounded bg-green-100" />
          <span className="text-gray-600">Post-Event Window (T+1 to T+{windowSize})</span>
        </div>
      </div>

      <div ref={chartRef}>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            
            {/* Pre-event shading */}
            <ReferenceArea
              x1={-windowSize}
              x2={-1}
              fill="#dbeafe"
              fillOpacity={0.3}
            />
            
            {/* Post-event shading */}
            <ReferenceArea
              x1={1}
              x2={windowSize}
              fill="#dcfce7"
              fillOpacity={0.3}
            />
            
            <XAxis
              dataKey="day"
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              label={{
                value: 'Days from Event',
                position: 'insideBottom',
                offset: -10,
                fontSize: 12,
                fill: '#6b7280',
              }}
              ticks={[-windowSize, -15, -10, -5, 0, 5, 10, 15, windowSize]}
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#6b7280' }}
              tickLine={{ stroke: '#e5e7eb' }}
              domain={[minValue - padding, maxValue + padding]}
              tickFormatter={(value) => value.toFixed(3)}
              label={{
                value: 'Cumulative Value',
                angle: -90,
                position: 'insideLeft',
                fontSize: 12,
                fill: '#6b7280',
              }}
            />
            
            {/* Event day marker */}
            <ReferenceLine
              x={0}
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="5 5"
              label={{
                value: 'Event Day',
                position: 'top',
                fill: '#ef4444',
                fontSize: 11,
                fontWeight: 'bold',
              }}
            />
            
            {/* Zero line */}
            <ReferenceLine y={0} stroke="#9ca3af" strokeDasharray="3 3" />
            
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              }}
              formatter={(value: number, name: string) => [
                value?.toFixed(4) ?? 'N/A',
                name === 'car' ? 'CAR (Cumulative Abnormal Return)' : 'CAS (Cumulative Abnormal Sentiment)',
              ]}
              labelFormatter={(label) => {
                if (label === 0) return 'Event Day (T=0)';
                return label > 0 ? `T+${label}` : `T${label}`;
              }}
            />
            <Legend
              formatter={(value) =>
                value === 'car' ? 'CAR (Cumulative Abnormal Return)' : 'CAS (Cumulative Abnormal Sentiment)'
              }
            />
            
            <Line
              type="monotone"
              dataKey="car"
              name="car"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={(props) => {
                const { cx, cy, payload } = props;
                if (payload.isEventDay) {
                  return (
                    <circle
                      cx={cx}
                      cy={cy}
                      r={6}
                      fill="#ef4444"
                      stroke="#fff"
                      strokeWidth={2}
                    />
                  );
                }
                return <circle cx={cx} cy={cy} r={3} fill="#3b82f6" />;
              }}
              activeDot={{ r: 6, fill: '#3b82f6' }}
            />
            <Line
              type="monotone"
              dataKey="cas"
              name="cas"
              stroke="#10b981"
              strokeWidth={2}
              dot={(props) => {
                const { cx, cy, payload } = props;
                if (payload.isEventDay) {
                  return (
                    <circle
                      cx={cx}
                      cy={cy}
                      r={6}
                      fill="#ef4444"
                      stroke="#fff"
                      strokeWidth={2}
                    />
                  );
                }
                return <circle cx={cx} cy={cy} r={3} fill="#10b981" />;
              }}
              activeDot={{ r: 6, fill: '#10b981' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
