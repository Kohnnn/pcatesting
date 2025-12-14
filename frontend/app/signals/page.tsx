'use client';

import { useSignals } from '@/hooks/useSignals';
import SignalList from '@/components/SignalList';
import { useState } from 'react';

export default function SignalsPage() {
  const { signals, loading, error } = useSignals(100);
  const [selectedType, setSelectedType] = useState<string>('All');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">All Signals</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Complete list of trading signals with advanced filtering
        </p>
      </div>
      
      {error && (
        <div className="rounded-lg bg-red-50 dark:bg-red-900/30 p-4 border border-red-200 dark:border-red-800">
          <p className="text-red-800 dark:text-red-300 text-sm">
            ⚠️ Unable to connect to backend API. Please ensure the backend server is running on port 8000.
          </p>
          <p className="text-red-600 dark:text-red-400 text-xs mt-1">
            Run: <code className="bg-red-100 dark:bg-red-900 px-1 rounded">python backend/main.py</code>
          </p>
        </div>
      )}

      <div className="rounded-lg bg-white p-6 shadow">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">
              Showing {signals.length} signals
            </p>
          </div>
          <a
            href="/export/daily_signals.csv"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Export CSV
          </a>
        </div>

        <SignalList signals={signals} loading={loading} />
      </div>
    </div>
  );
}
