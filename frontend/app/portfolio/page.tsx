'use client';

import { useState, useEffect } from 'react';
import { useWatchlist } from '@/hooks/useWatchlist';
import { TradingSignal } from '@/types';
import SignalCard from '@/components/SignalCard';
import LoadingSkeleton from '@/components/LoadingSkeleton';
import api from '@/services/api';

export default function PortfolioPage() {
  const { watchlist, loading, addToWatchlist, removeFromWatchlist, isInWatchlist } = useWatchlist();
  const [watchlistSignals, setWatchlistSignals] = useState<Record<string, TradingSignal | null>>({});
  const [newTicker, setNewTicker] = useState('');
  const [addingTicker, setAddingTicker] = useState(false);

  useEffect(() => {
    // Fetch latest signals for each watchlist item
    const fetchSignals = async () => {
      const signals: Record<string, TradingSignal | null> = {};
      for (const item of watchlist) {
        try {
          const signal = await api.signals.getByTicker(item.ticker);
          signals[item.ticker] = signal;
        } catch (error) {
          signals[item.ticker] = null;
        }
      }
      setWatchlistSignals(signals);
    };

    if (watchlist.length > 0) {
      fetchSignals();
    }
  }, [watchlist]);

  const handleAddTicker = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTicker.trim()) return;

    setAddingTicker(true);
    const success = await addToWatchlist(newTicker.toUpperCase());
    if (success) {
      setNewTicker('');
    }
    setAddingTicker(false);
  };

  const handleRemove = async (id: number) => {
    await removeFromWatchlist(id);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Portfolio Watchlist</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Track your favorite stocks and their latest signals
        </p>
      </div>

      {/* Add to watchlist form */}
      <div className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Add Stock to Watchlist</h2>
        <form onSubmit={handleAddTicker} className="flex gap-2">
          <input
            type="text"
            value={newTicker}
            onChange={(e) => setNewTicker(e.target.value)}
            placeholder="Enter ticker symbol (e.g., VNM, AAA)"
            className="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            disabled={addingTicker}
          />
          <button
            type="submit"
            disabled={addingTicker || !newTicker.trim()}
            className="rounded-lg bg-blue-600 px-6 py-2 font-medium text-white hover:bg-blue-700 disabled:bg-gray-400"
          >
            {addingTicker ? 'Adding...' : 'Add'}
          </button>
        </form>
      </div>

      {/* Watchlist items */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Your Watchlist ({watchlist.length})
        </h2>

        {loading ? (
          <LoadingSkeleton />
        ) : watchlist.length === 0 ? (
          <div className="rounded-lg bg-white dark:bg-gray-800 p-8 text-center text-gray-500 dark:text-gray-400 shadow">
            Your watchlist is empty. Add stocks to start tracking them.
          </div>
        ) : (
          <div className="space-y-3">
            {watchlist.map((item) => {
              const signal = watchlistSignals[item.ticker];
              return (
                <div key={item.id} className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">{item.ticker}</h3>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          Added {new Date(item.added_at).toLocaleDateString()}
                        </span>
                      </div>
                      
                      {signal ? (
                        <div className="mt-3">
                          <SignalCard signal={signal} />
                        </div>
                      ) : (
                        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">No recent signals</p>
                      )}
                    </div>
                    
                    <button
                      onClick={() => handleRemove(item.id)}
                      className="ml-4 rounded-lg bg-red-100 px-3 py-1 text-sm font-medium text-red-700 hover:bg-red-200"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
