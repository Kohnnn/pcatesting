import { useState, useEffect, useCallback, useMemo } from 'react';
import { DataQualityMetric } from '@/types';
import api from '@/services/api';

export interface DataQualitySummary {
  totalRecords: number;
  totalAnomalies: number;
  avgCompleteness: number;
}

export interface UseDataQualityReturn {
  metrics: DataQualityMetric[];
  summary: DataQualitySummary;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useDataQuality(): UseDataQualityReturn {
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
      setError(err instanceof Error ? err.message : 'Failed to fetch data quality metrics');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  // Calculate summary statistics
  const summary = useMemo<DataQualitySummary>(() => {
    const totalRecords = metrics.reduce((sum, m) => sum + m.total_records, 0);
    const totalAnomalies = metrics.reduce((sum, m) => sum + m.anomaly_count, 0);
    const avgCompleteness = metrics.length > 0
      ? metrics.reduce((sum, m) => sum + m.completeness_pct, 0) / metrics.length
      : 100;

    return {
      totalRecords,
      totalAnomalies,
      avgCompleteness,
    };
  }, [metrics]);

  return {
    metrics,
    summary,
    loading,
    error,
    refetch: fetchMetrics,
  };
}
