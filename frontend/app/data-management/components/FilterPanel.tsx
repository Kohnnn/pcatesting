'use client';

import { useState, useEffect } from 'react';

interface FilterPanelProps {
  activeTable: string;
  filters: {
    ticker?: string;
    startDate?: string;
    endDate?: string;
    signalType?: string;
  };
  onFilterChange: (filters: {
    ticker?: string;
    startDate?: string;
    endDate?: string;
    signalType?: string;
  }) => void;
}

const SIGNAL_TYPES = [
  'Contrarian Dip Buy',
  'Momentum Breakout',
  'Retail Trap',
  'Neutral / No Edge',
];

export default function FilterPanel({ activeTable, filters, onFilterChange }: FilterPanelProps) {
  const [localFilters, setLocalFilters] = useState(filters);

  // Sync local filters with props
  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const handleInputChange = (key: string, value: string) => {
    setLocalFilters(prev => ({
      ...prev,
      [key]: value || undefined,
    }));
  };

  const handleApplyFilters = () => {
    onFilterChange(localFilters);
  };

  const handleClearFilters = () => {
    const cleared = {};
    setLocalFilters(cleared);
    onFilterChange(cleared);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleApplyFilters();
    }
  };

  // Determine which filters to show based on active table
  const showTickerFilter = ['instruments', 'market_data', 'analyst_recommendations', 'daily_sentiment', 'trading_signals'].includes(activeTable);
  const showDateFilter = ['market_data', 'analyst_recommendations', 'daily_sentiment', 'trading_signals', 'vnindex', 'risk_free_rate'].includes(activeTable);
  const showSignalTypeFilter = activeTable === 'trading_signals';

  const hasActiveFilters = Object.values(filters).some(v => v !== undefined && v !== '');

  return (
    <div className="rounded-lg bg-white p-4 shadow">
      <div className="flex flex-wrap items-end gap-4">
        {/* Ticker filter */}
        {showTickerFilter && (
          <div className="flex-1 min-w-[150px]">
            <label htmlFor="ticker" className="block text-sm font-medium text-gray-700 mb-1">
              Ticker
            </label>
            <input
              type="text"
              id="ticker"
              placeholder="e.g., VNM"
              value={localFilters.ticker || ''}
              onChange={(e) => handleInputChange('ticker', e.target.value.toUpperCase())}
              onKeyDown={handleKeyDown}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            />
          </div>
        )}

        {/* Date range filter */}
        {showDateFilter && (
          <>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
                From Date
              </label>
              <input
                type="date"
                id="startDate"
                value={localFilters.startDate || ''}
                onChange={(e) => handleInputChange('startDate', e.target.value)}
                onKeyDown={handleKeyDown}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div className="flex-1 min-w-[150px]">
              <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
                To Date
              </label>
              <input
                type="date"
                id="endDate"
                value={localFilters.endDate || ''}
                onChange={(e) => handleInputChange('endDate', e.target.value)}
                onKeyDown={handleKeyDown}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
          </>
        )}

        {/* Signal type filter */}
        {showSignalTypeFilter && (
          <div className="flex-1 min-w-[200px]">
            <label htmlFor="signalType" className="block text-sm font-medium text-gray-700 mb-1">
              Signal Type
            </label>
            <select
              id="signalType"
              value={localFilters.signalType || ''}
              onChange={(e) => handleInputChange('signalType', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            >
              <option value="">All Signal Types</option>
              {SIGNAL_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex gap-2">
          <button
            onClick={handleApplyFilters}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Apply Filters
          </button>
          {hasActiveFilters && (
            <button
              onClick={handleClearFilters}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
