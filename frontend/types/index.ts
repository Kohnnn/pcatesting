/**
 * Type definitions for SentimentAlpha Vietnam
 * Based on design document specifications
 */

export interface TradingSignal {
  id: number;
  ticker: string;
  date: string;
  signal_type: 'Contrarian Dip Buy' | 'Momentum Breakout' | 'Retail Trap' | 'Neutral / No Edge';
  sentiment_score: number | null;
  foreign_flow_score: number | null;
  analyst_action: string | null;
}

export interface DailySentiment {
  ticker: string;
  date: string;
  rsi: number | null;
  bsi: number | null;
  atr: number | null;
  ltv: number | null;
  pli: number | null;
  raw_sentiment: number | null;
  pure_sentiment: number | null;
}

export interface EventStudyData {
  days: number[];
  car: number[];
  cas: number[];
}

export interface SignalThresholds {
  sentiment_min: number;
  rsi_max: number;
  rsi_min: number;
  bsi_min: number;
  bsi_max: number;
}

export interface Instrument {
  ticker: string;
  name: string;
  created_at: string;
}

export interface WatchlistItem {
  id: number;
  ticker: string;
  added_at: string;
}

export interface AnalystRecommendation {
  id: number;
  ticker: string;
  analyst_firm: string;
  analyst_name: string;
  recommendation: string;
  rating_numeric: number;
  target_price: number | null;
  issue_date: string;
}

// Data Management Types
export interface ColumnInfo {
  name: string;
  display_name: string;
  data_type: string;
  sortable: boolean;
  filterable: boolean;
}

export interface TableInfo {
  name: string;
  display_name: string;
  record_count: number;
  last_updated: string | null;
  columns: ColumnInfo[];
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface InstrumentDetail {
  ticker: string;
  name: string | null;
  market_data_count: number;
  recommendations_count: number;
  signals_count: number;
  latest_price: number | null;
  latest_sentiment: DailySentiment | null;
  recent_signals: TradingSignal[];
}

export interface DataQualityMetric {
  table_name: string;
  display_name: string;
  total_records: number;
  completeness_pct: number;
  anomaly_count: number;
  last_updated: string | null;
}

export interface PipelineRun {
  id: number;
  started_at: string;
  completed_at: string | null;
  status: 'running' | 'success' | 'partial' | 'failed';
  files_processed: number;
  records_inserted: number;
  records_updated: number;
  errors_count: number;
  error_details: string[] | null;
}

// VNIndex data for market overview
export interface VNIndexData {
  date: string;
  close_index: number;
  buy_volume: number;
  sell_volume: number;
  total_volume: number;
}

// Correlation matrix for sentiment proxies
export interface CorrelationMatrix {
  labels: string[];
  values: number[][];
}

// Market data for instruments
export interface MarketData {
  ticker: string;
  date: string;
  close_price: number;
  buy_volume: number;
  sell_volume: number;
  total_volume: number;
  shares_outstanding: number;
}

// Signal distribution data
export interface SignalDistribution {
  signal_type: string;
  count: number;
  percentage: number;
}
