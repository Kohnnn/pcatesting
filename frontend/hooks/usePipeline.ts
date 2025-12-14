import { useState, useEffect, useCallback, useRef } from 'react';
import { PipelineRun } from '@/types';
import api from '@/services/api';

const POLL_INTERVAL = 2000; // 2 seconds

export interface UsePipelineReturn {
  // Current run state
  currentRun: PipelineRun | null;
  isRunning: boolean;
  error: string | null;
  
  // Pipeline history
  history: PipelineRun[];
  historyLoading: boolean;
  historyError: string | null;
  
  // Actions
  runPipeline: (forceFull?: boolean) => Promise<PipelineRun | null>;
  fetchHistory: (limit?: number) => Promise<void>;
  getRunStatus: (runId: number) => Promise<PipelineRun | null>;
  clearError: () => void;
}

export function usePipeline(): UsePipelineReturn {
  // Current run state
  const [currentRun, setCurrentRun] = useState<PipelineRun | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // History state
  const [history, setHistory] = useState<PipelineRun[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);
  
  // Polling ref
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  // Poll for status updates when pipeline is running
  useEffect(() => {
    if (!isRunning || !currentRun) {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      return;
    }

    pollIntervalRef.current = setInterval(async () => {
      try {
        const status = await api.pipeline.getStatus(currentRun.id);
        setCurrentRun(status);

        if (status.status !== 'running') {
          setIsRunning(false);
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
          // Refresh history after completion
          fetchHistory();
        }
      } catch (err) {
        console.error('Failed to poll pipeline status:', err);
      }
    }, POLL_INTERVAL);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [isRunning, currentRun?.id]);

  /**
   * Trigger pipeline execution
   */
  const runPipeline = useCallback(async (forceFull: boolean = false): Promise<PipelineRun | null> => {
    setError(null);
    setIsRunning(true);

    try {
      const response = await api.pipeline.run(forceFull);
      // Fetch the full run details
      const run = await api.pipeline.getStatus(response.id);
      setCurrentRun(run);
      return run;
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
        setError(err instanceof Error ? err.message : 'Failed to start pipeline');
      }
      return null;
    }
  }, []);

  /**
   * Fetch pipeline history
   */
  const fetchHistory = useCallback(async (limit: number = 20): Promise<void> => {
    setHistoryLoading(true);
    setHistoryError(null);

    try {
      const data = await api.pipeline.getHistory(limit);
      setHistory(data);
    } catch (err) {
      setHistoryError(err instanceof Error ? err.message : 'Failed to fetch pipeline history');
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  /**
   * Get status of a specific pipeline run
   */
  const getRunStatus = useCallback(async (runId: number): Promise<PipelineRun | null> => {
    try {
      const status = await api.pipeline.getStatus(runId);
      return status;
    } catch (err) {
      console.error('Failed to get pipeline status:', err);
      return null;
    }
  }, []);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Fetch history on mount
  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    currentRun,
    isRunning,
    error,
    history,
    historyLoading,
    historyError,
    runPipeline,
    fetchHistory,
    getRunStatus,
    clearError,
  };
}
