import { useState, useEffect } from 'react';
import api from '@/services/api';

interface WatchlistItem {
  id: number;
  ticker: string;
  added_at: string;
}

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWatchlist = async () => {
    try {
      setLoading(true);
      const data = await api.watchlist.getAll();
      setWatchlist(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch watchlist');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWatchlist();
  }, []);

  const addToWatchlist = async (ticker: string) => {
    try {
      const newItem = await api.watchlist.add(ticker);
      setWatchlist(prev => [...prev, newItem]);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add to watchlist');
      return false;
    }
  };

  const removeFromWatchlist = async (id: number) => {
    try {
      await api.watchlist.remove(id);
      setWatchlist(prev => prev.filter(item => item.id !== id));
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove from watchlist');
      return false;
    }
  };

  const isInWatchlist = (ticker: string) => {
    return watchlist.some(item => item.ticker === ticker);
  };

  return { 
    watchlist, 
    loading, 
    error, 
    addToWatchlist, 
    removeFromWatchlist, 
    isInWatchlist,
    refetch: fetchWatchlist 
  };
}
