import axios from 'axios';
import { 
  TradingSignal, 
  DailySentiment, 
  EventStudyData, 
  SignalThresholds,
  TableInfo,
  PaginatedResponse,
  InstrumentDetail,
  DataQualityMetric,
  PipelineRun,
  VNIndexData,
  CorrelationMatrix,
  AnalystRecommendation,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Signals endpoints
  signals: {
    getAll: async (limit?: number, offset?: number) => {
      const params = new URLSearchParams();
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      const response = await apiClient.get<TradingSignal[]>(`/signals?${params.toString()}`);
      return response.data;
    },
    getByTicker: async (ticker: string) => {
      const response = await apiClient.get<TradingSignal>(`/signals/${ticker}`);
      return response.data;
    },
  },

  // Sentiment endpoints
  sentiment: {
    getByTicker: async (ticker: string) => {
      const response = await apiClient.get<DailySentiment[]>(`/sentiment/${ticker}`);
      return response.data;
    },
  },

  // Event study endpoints
  eventStudy: {
    get: async (ticker: string, date: string) => {
      const response = await apiClient.get<EventStudyData>(`/event-study/${ticker}/${date}`);
      return response.data;
    },
  },

  // Settings endpoints
  settings: {
    get: async () => {
      const response = await apiClient.get<SignalThresholds>('/settings');
      return response.data;
    },
    update: async (settings: SignalThresholds) => {
      const response = await apiClient.post<SignalThresholds>('/settings', settings);
      return response.data;
    },
  },

  // Watchlist endpoints
  watchlist: {
    getAll: async () => {
      const response = await apiClient.get<Array<{ id: number; ticker: string; added_at: string }>>('/watchlist');
      return response.data;
    },
    add: async (ticker: string) => {
      const response = await apiClient.post<{ id: number; ticker: string; added_at: string }>('/watchlist', { ticker });
      return response.data;
    },
    remove: async (id: number) => {
      await apiClient.delete(`/watchlist/${id}`);
    },
  },

  // Export endpoints
  export: {
    getDailySignalsCSV: () => {
      return `${API_BASE_URL}/export/daily_signals.csv`;
    },
  },

  // Data Management endpoints
  dataManagement: {
    getTables: async () => {
      const response = await apiClient.get<TableInfo[]>('/data-management/tables');
      return response.data;
    },
    getTableData: async (
      tableName: string,
      options: {
        page?: number;
        pageSize?: number;
        sortBy?: string;
        sortOrder?: 'asc' | 'desc';
        ticker?: string;
        startDate?: string;
        endDate?: string;
        signalType?: string;
      } = {}
    ) => {
      const params = new URLSearchParams();
      if (options.page) params.append('page', options.page.toString());
      if (options.pageSize) params.append('page_size', options.pageSize.toString());
      if (options.sortBy) params.append('sort_by', options.sortBy);
      if (options.sortOrder) params.append('sort_order', options.sortOrder);
      if (options.ticker) params.append('ticker', options.ticker);
      if (options.startDate) params.append('start_date', options.startDate);
      if (options.endDate) params.append('end_date', options.endDate);
      if (options.signalType) params.append('signal_type', options.signalType);
      const response = await apiClient.get<PaginatedResponse<Record<string, unknown>>>(
        `/data-management/tables/${tableName}?${params.toString()}`
      );
      return response.data;
    },
    getInstrumentDetail: async (ticker: string) => {
      const response = await apiClient.get<InstrumentDetail>(`/data-management/instruments/${ticker}`);
      return response.data;
    },
    getDataQuality: async () => {
      const response = await apiClient.get<DataQualityMetric[]>('/data-management/quality');
      return response.data;
    },
  },

  // Pipeline endpoints
  pipeline: {
    run: async (forceFull: boolean = false) => {
      const response = await apiClient.post<PipelineRun>('/pipeline/run', null, {
        params: { force_full: forceFull }
      });
      return response.data;
    },
    getStatus: async (runId: number) => {
      const response = await apiClient.get<PipelineRun>(`/pipeline/status/${runId}`);
      return response.data;
    },
    getHistory: async (limit: number = 20) => {
      const response = await apiClient.get<PipelineRun[]>('/pipeline/history', {
        params: { limit }
      });
      return response.data;
    },
  },

  // Market data endpoints
  market: {
    getVNIndex: async (startDate?: string, endDate?: string) => {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate);
      if (endDate) params.append('end_date', endDate);
      const response = await apiClient.get<VNIndexData[]>(`/market/vnindex?${params.toString()}`);
      return response.data;
    },
    getCorrelationMatrix: async (ticker?: string) => {
      const params = new URLSearchParams();
      if (ticker) params.append('ticker', ticker);
      const response = await apiClient.get<CorrelationMatrix>(`/market/correlations?${params.toString()}`);
      return response.data;
    },
  },

  // Recommendations endpoints
  recommendations: {
    getByTicker: async (ticker: string) => {
      const response = await apiClient.get<AnalystRecommendation[]>(`/recommendations/${ticker}`);
      return response.data;
    },
    getAll: async (limit?: number, offset?: number) => {
      const params = new URLSearchParams();
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      const response = await apiClient.get<AnalystRecommendation[]>(`/recommendations?${params.toString()}`);
      return response.data;
    },
  },
};

export default api;
