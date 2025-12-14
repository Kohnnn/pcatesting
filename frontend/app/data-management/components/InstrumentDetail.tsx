'use client';

import { InstrumentDetail as InstrumentDetailType, TradingSignal } from '@/types';

interface InstrumentDetailProps {
  detail: InstrumentDetailType | null;
  loading: boolean;
  onClose: () => void;
}

// Rating display mapping (per thesis Table 2)
const RATING_LABELS: Record<number, { label: string; color: string }> = {
  5: { label: 'Buy', color: 'bg-green-100 text-green-800' },
  4: { label: 'Overweight', color: 'bg-green-50 text-green-700' },
  3: { label: 'Hold', color: 'bg-yellow-100 text-yellow-800' },
  2: { label: 'Underweight', color: 'bg-orange-100 text-orange-800' },
  1: { label: 'Sell', color: 'bg-red-100 text-red-800' },
};

const getSignalTypeColor = (signalType: string): string => {
  switch (signalType) {
    case 'Contrarian Dip Buy':
      return 'bg-green-100 text-green-800';
    case 'Momentum Breakout':
      return 'bg-blue-100 text-blue-800';
    case 'Retail Trap':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function InstrumentDetail({ detail, loading, onClose }: InstrumentDetailProps) {
  if (loading) {
    return (
      <div className="rounded-lg bg-white shadow p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-100 rounded"></div>
            <div className="h-4 bg-gray-100 rounded w-3/4"></div>
            <div className="h-4 bg-gray-100 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!detail) {
    return null;
  }

  return (
    <div className="rounded-lg bg-white shadow">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{detail.ticker}</h3>
          {detail.name && (
            <p className="text-sm text-gray-500">{detail.name}</p>
          )}
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-500"
        >
          <span className="sr-only">Close</span>
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Stats */}
      <div className="px-6 py-4 border-b border-gray-200">
        <dl className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-sm font-medium text-gray-500">Latest Price</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {detail.latest_price 
                ? `₫${detail.latest_price.toLocaleString()}` 
                : '-'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Market Data</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {detail.market_data_count.toLocaleString()} records
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Recommendations</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {detail.recommendations_count.toLocaleString()}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Signals</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {detail.signals_count.toLocaleString()}
            </dd>
          </div>
        </dl>
      </div>

      {/* Latest Sentiment - Using thesis terminology */}
      {detail.latest_sentiment && (
        <div className="px-6 py-4 border-b border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Latest Sentiment Indicators</h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="flex justify-between" title="Buy-Sell Imbalance">
              <span className="text-gray-500">BSI:</span>
              <span className="font-medium">
                {detail.latest_sentiment.bsi?.toFixed(3) ?? '-'}
              </span>
            </div>
            <div className="flex justify-between" title="Relative Strength Index">
              <span className="text-gray-500">RSI:</span>
              <span className="font-medium">
                {detail.latest_sentiment.rsi?.toFixed(2) ?? '-'}
              </span>
            </div>
            <div className="flex justify-between" title="Adjusted Turnover Ratio">
              <span className="text-gray-500">ATR:</span>
              <span className="font-medium">
                {detail.latest_sentiment.atr?.toFixed(4) ?? '-'}
              </span>
            </div>
            <div className="flex justify-between" title="Log Trading Volume">
              <span className="text-gray-500">LTV:</span>
              <span className="font-medium">
                {detail.latest_sentiment.ltv?.toFixed(2) ?? '-'}
              </span>
            </div>
            <div className="flex justify-between" title="Psychological Line Index">
              <span className="text-gray-500">PLI:</span>
              <span className="font-medium">
                {detail.latest_sentiment.pli?.toFixed(2) ?? '-'}
              </span>
            </div>
            <div className="flex justify-between" title="Pure Sentiment (Market-Adjusted)">
              <span className="text-gray-500">Pure Sentiment:</span>
              <span className="font-medium">
                {detail.latest_sentiment.pure_sentiment?.toFixed(3) ?? '-'}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Recent Signals */}
      {detail.recent_signals.length > 0 && (
        <div className="px-6 py-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Recent Signals</h4>
          <div className="space-y-2">
            {detail.recent_signals.slice(0, 5).map((signal: TradingSignal) => (
              <div
                key={signal.id}
                className="flex items-center justify-between text-sm"
              >
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getSignalTypeColor(signal.signal_type)}`}>
                    {signal.signal_type}
                  </span>
                </div>
                <span className="text-gray-500">
                  {new Date(signal.date).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Export rating labels for use in other components
export { RATING_LABELS };
