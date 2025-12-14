'use client';

import { useSignals } from '@/hooks/useSignals';
import SignalList from '@/components/SignalList';

export default function SignalsPage() {
  const { signals, loading } = useSignals(100);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">All Signals</h1>
        <p className="mt-2 text-gray-600">
          Complete list of trading signals with advanced filtering
        </p>
      </div>

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
