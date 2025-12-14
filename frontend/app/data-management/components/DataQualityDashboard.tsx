'use client';

import { useState, useEffect, useCallback } from 'react';
import api from '@/services/api';
import { DataQualityMetric } from '@/types';

export default function DataQualityDashboard() {
  const [metrics, setMetrics] = useState<DataQualityMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.dataManagement.getDataQuality();
      setMetrics(data);
    } catch (err) {
      console.error('Failed to fetch data quality metrics:', err);
      setError('Failed to load data quality metrics');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  const getCompletenessColor = (pct: number) => {
    if (pct >= 99) return 'text-green-600 bg-green-100';
    if (pct >= 95) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getCompletenessBarColor = (pct: number) => {
    if (pct >= 99) return 'bg-green-500';
    if (pct >= 95) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getAnomalyBadgeColor = (count: number) => {
    if (count === 0) return 'text-green-700 bg-green-100';
    if (count <= 10) return 'text-yellow-700 bg-yellow-100';
    return 'text-red-700 bg-red-100';
  };

  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'Never';
    return new Date(dateStr).toLocaleString();
  };

  // Calculate overall statistics
  const totalRecords = metrics.reduce((sum, m) => sum + m.total_records, 0);
  const totalAnomalies = metrics.reduce((sum, m) => sum + m.anomaly_count, 0);
  const avgCompleteness = metrics.length > 0
    ? metrics.reduce((sum, m) => sum + m.completeness_pct, 0) / metrics.length
    : 100;

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Quality</h3>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Quality</h3>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
          <button
            onClick={fetchMetrics}
            className="mt-2 text-sm text-red-700 underline hover:no-underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Data Quality Dashboard</h3>
        <button
          onClick={fetchMetrics}
          className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-500">Total Records</p>
          <p className="text-2xl font-bold text-gray-900">{formatNumber(totalRecords)}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-500">Avg Completeness</p>
          <p className={`text-2xl font-bold ${avgCompleteness >= 99 ? 'text-green-600' : avgCompleteness >= 95 ? 'text-yellow-600' : 'text-red-600'}`}>
            {avgCompleteness.toFixed(1)}%
          </p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-500">Total Anomalies</p>
          <p className={`text-2xl font-bold ${totalAnomalies === 0 ? 'text-green-600' : totalAnomalies <= 10 ? 'text-yellow-600' : 'text-red-600'}`}>
            {formatNumber(totalAnomalies)}
          </p>
        </div>
      </div>

      {/* Table Metrics */}
      <div className="space-y-4">
        <h4 className="text-sm font-medium text-gray-700">Completeness by Table</h4>
        {metrics.map((metric) => (
          <div key={metric.table_name} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div>
                <span className="font-medium text-gray-900">{metric.display_name}</span>
                <span className="ml-2 text-sm text-gray-500">
                  ({formatNumber(metric.total_records)} records)
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCompletenessColor(metric.completeness_pct)}`}>
                  {metric.completeness_pct.toFixed(1)}%
                </span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAnomalyBadgeColor(metric.anomaly_count)}`}>
                  {metric.anomaly_count} anomalies
                </span>
              </div>
            </div>
            
            {/* Progress bar */}
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-300 ${getCompletenessBarColor(metric.completeness_pct)}`}
                style={{ width: `${Math.min(metric.completeness_pct, 100)}%` }}
              ></div>
            </div>
            
            {metric.last_updated && (
              <p className="mt-2 text-xs text-gray-400">
                Last updated: {formatDate(metric.last_updated)}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 mb-2">Completeness Legend:</p>
        <div className="flex gap-4 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-green-500"></span>
            <span className="text-gray-600">≥99% (Excellent)</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
            <span className="text-gray-600">95-99% (Good)</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="text-gray-600">&lt;95% (Needs Attention)</span>
          </span>
        </div>
      </div>
    </div>
  );
}
