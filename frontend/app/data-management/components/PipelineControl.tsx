'use client';

import { useState, useEffect, useCallback } from 'react';
import api from '@/services/api';
import { PipelineRun } from '@/types';

interface PipelineControlProps {
  onPipelineComplete?: (run: PipelineRun) => void;
}

export default function PipelineControl({ onPipelineComplete }: PipelineControlProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [currentRun, setCurrentRun] = useState<PipelineRun | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [forceFull, setForceFull] = useState(false);

  // Poll for status updates when pipeline is running
  useEffect(() => {
    if (!isRunning || !currentRun) return;

    const pollInterval = setInterval(async () => {
      try {
        const status = await api.pipeline.getStatus(currentRun.id);
        setCurrentRun(status);

        if (status.status !== 'running') {
          setIsRunning(false);
          clearInterval(pollInterval);
          onPipelineComplete?.(status);
        }
      } catch (err) {
        console.error('Failed to poll pipeline status:', err);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [isRunning, currentRun, onPipelineComplete]);

  const handleRunPipeline = useCallback(async () => {
    setError(null);
    setIsRunning(true);

    try {
      const response = await api.pipeline.run(forceFull);
      // Fetch the full run details
      const run = await api.pipeline.getStatus(response.id);
      setCurrentRun(run);
    } catch (err: unknown) {
      setIsRunning(false);
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosError = err as { response?: { status?: number; data?: { detail?: string } } };
        if (axiosError.response?.status === 409) {
          setError('Pipeline is already running. Please wait for it to complete.');
        } else {
          setError(axiosError.response?.data?.detail || 'Failed to start pipeline');
        }
      } else {
        setError('Failed to start pipeline');
      }
    }
  }, [forceFull]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'text-blue-600';
      case 'success':
        return 'text-green-600';
      case 'partial':
        return 'text-yellow-600';
      case 'failed':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return (
          <svg className="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        );
      case 'success':
        return (
          <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
          </svg>
        );
      case 'partial':
        return (
          <svg className="h-5 w-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
        );
      case 'failed':
        return (
          <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Pipeline Control</h3>
        {currentRun && (
          <div className="flex items-center gap-2">
            {getStatusIcon(currentRun.status)}
            <span className={`font-medium capitalize ${getStatusColor(currentRun.status)}`}>
              {currentRun.status}
            </span>
          </div>
        )}
      </div>

      {/* Force full update checkbox */}
      <div className="mb-4">
        <label className="flex items-center gap-2 text-sm text-gray-600">
          <input
            type="checkbox"
            checked={forceFull}
            onChange={(e) => setForceFull(e.target.checked)}
            disabled={isRunning}
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          Force full update (reprocess all files)
        </label>
      </div>

      {/* Run button */}
      <button
        onClick={handleRunPipeline}
        disabled={isRunning}
        className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
          isRunning
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isRunning ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Running Pipeline...
          </span>
        ) : (
          'Run Pipeline'
        )}
      </button>

      {/* Error message */}
      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Progress status during execution */}
      {isRunning && currentRun && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800 font-medium mb-2">Processing...</p>
          <div className="space-y-1 text-sm text-blue-700">
            <p>Files processed: {currentRun.files_processed}</p>
            <p>Records inserted: {currentRun.records_inserted}</p>
            <p>Records updated: {currentRun.records_updated}</p>
            {currentRun.errors_count > 0 && (
              <p className="text-red-600">Errors: {currentRun.errors_count}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
