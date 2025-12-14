'use client';

import { useState, useEffect, useCallback } from 'react';
import api from '@/services/api';
import { PipelineRun } from '@/types';

interface PipelineHistoryProps {
  refreshTrigger?: number;
  onSelectRun?: (run: PipelineRun) => void;
}

export default function PipelineHistory({ refreshTrigger, onSelectRun }: PipelineHistoryProps) {
  const [history, setHistory] = useState<PipelineRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.pipeline.getHistory(20);
      setHistory(data);
    } catch (err) {
      console.error('Failed to fetch pipeline history:', err);
      setError('Failed to load pipeline history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory, refreshTrigger]);

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDuration = (startedAt: string, completedAt: string | null) => {
    if (!completedAt) return 'In progress';
    const start = new Date(startedAt).getTime();
    const end = new Date(completedAt).getTime();
    const durationMs = end - start;
    
    if (durationMs < 1000) return `${durationMs}ms`;
    if (durationMs < 60000) return `${Math.round(durationMs / 1000)}s`;
    return `${Math.round(durationMs / 60000)}m ${Math.round((durationMs % 60000) / 1000)}s`;
  };

  const getStatusBadge = (status: string) => {
    const baseClasses = 'px-2 py-1 text-xs font-medium rounded-full';
    switch (status) {
      case 'running':
        return `${baseClasses} bg-blue-100 text-blue-800`;
      case 'success':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'partial':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case 'failed':
        return `${baseClasses} bg-red-100 text-red-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Pipeline History</h3>
        <div className="animate-pulse space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Pipeline History</h3>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
          <button
            onClick={fetchHistory}
            className="mt-2 text-sm text-red-700 underline hover:no-underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Pipeline History</h3>
        <button
          onClick={fetchHistory}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Refresh
        </button>
      </div>

      {history.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No pipeline runs yet</p>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {history.map((run) => (
            <div
              key={run.id}
              onClick={() => onSelectRun?.(run)}
              className={`p-4 border rounded-lg transition-colors ${
                onSelectRun ? 'cursor-pointer hover:bg-gray-50' : ''
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-900">
                  Run #{run.id}
                </span>
                <span className={getStatusBadge(run.status)}>
                  {run.status}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div>
                  <span className="text-gray-400">Started:</span>{' '}
                  {formatDate(run.started_at)}
                </div>
                <div>
                  <span className="text-gray-400">Duration:</span>{' '}
                  {formatDuration(run.started_at, run.completed_at)}
                </div>
              </div>

              <div className="mt-2 flex flex-wrap gap-3 text-xs">
                <span className="text-gray-600">
                  <span className="font-medium">{run.files_processed}</span> files
                </span>
                <span className="text-green-600">
                  <span className="font-medium">{run.records_inserted}</span> inserted
                </span>
                <span className="text-blue-600">
                  <span className="font-medium">{run.records_updated}</span> updated
                </span>
                {run.errors_count > 0 && (
                  <span className="text-red-600">
                    <span className="font-medium">{run.errors_count}</span> errors
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
