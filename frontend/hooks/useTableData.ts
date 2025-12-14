import { useState, useEffect, useCallback } from 'react';
import { PaginatedResponse, TableInfo } from '@/types';
import api from '@/services/api';

export interface TableFilters {
  ticker?: string;
  startDate?: string;
  endDate?: string;
  signalType?: string;
}

export interface UseTableDataOptions {
  tableName: string;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  filters?: TableFilters;
}

export interface UseTableDataReturn {
  data: Record<string, unknown>[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useTableData(options: UseTableDataOptions): UseTableDataReturn {
  const {
    tableName,
    page = 1,
    pageSize = 50,
    sortBy,
    sortOrder = 'desc',
    filters = {},
  } = options;

  const [response, setResponse] = useState<PaginatedResponse<Record<string, unknown>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.dataManagement.getTableData(tableName, {
        page,
        pageSize,
        sortBy,
        sortOrder,
        ...filters,
      });
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch table data');
    } finally {
      setLoading(false);
    }
  }, [tableName, page, pageSize, sortBy, sortOrder, filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    data: response?.data || [],
    total: response?.total || 0,
    page: response?.page || page,
    pageSize: response?.page_size || pageSize,
    totalPages: response?.total_pages || 1,
    loading,
    error,
    refetch: fetchData,
  };
}

/**
 * Hook to fetch the list of available tables
 */
export function useTableList() {
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTables = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.dataManagement.getTables();
      setTables(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tables');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  return {
    tables,
    loading,
    error,
    refetch: fetchTables,
  };
}
