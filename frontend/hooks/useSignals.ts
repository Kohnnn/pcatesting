import { useState, useEffect } from 'react';
import { TradingSignal } from '@/types';
import api from '@/services/api';

export function useSignals(limit?: number, offset?: number) {
  const [signals, setSignals] = useState<TradingSignal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        setLoading(true);
        const data = await api.signals.getAll(limit, offset);
        setSignals(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch signals');
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
  }, [limit, offset]);

  const filterSignals = (signalType?: string) => {
    if (!signalType || signalType === 'All') {
      return signals;
    }
    return signals.filter(signal => signal.signal_type === signalType);
  };

  return { signals, loading, error, filterSignals };
}
