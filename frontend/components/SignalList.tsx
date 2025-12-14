'use client';

import { useState } from 'react';
import { TradingSignal } from '@/types';
import SignalCard from './SignalCard';
import { SignalCardSkeleton } from './LoadingSkeleton';

interface SignalListProps {
  signals: TradingSignal[];
  loading?: boolean;
  onSignalClick?: (signal: TradingSignal) => void;
  selectedSignalId?: number;
}

const SIGNAL_TYPES = [
  'All',
  'Contrarian Dip Buy',
  'Momentum Breakout',
  'Retail Trap',
  'Neutral / No Edge',
];

export default function SignalList({ 
  signals, 
  loading, 
  onSignalClick,
  selectedSignalId 
}: SignalListProps) {
  const [filter, setFilter] = useState('All');

  const filteredSignals = filter === 'All' 
    ? signals 
    : signals.filter(s => s.signal_type === filter);

  return (
    <div className="space-y-4">
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2">
        {SIGNAL_TYPES.map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            className={`
              rounded-lg px-4 py-2 text-sm font-medium transition-colors
              ${filter === type
                ? 'bg-blue-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600'
              }
            `}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Signal list */}
      <div className="space-y-3">
        {loading ? (
          <>
            <SignalCardSkeleton />
            <SignalCardSkeleton />
            <SignalCardSkeleton />
          </>
        ) : filteredSignals.length === 0 ? (
          <div className="rounded-lg bg-white dark:bg-gray-800 p-8 text-center text-gray-500 dark:text-gray-400">
            No signals found for the selected filter.
          </div>
        ) : (
          filteredSignals.map((signal) => (
            <SignalCard
              key={signal.id}
              signal={signal}
              onClick={() => onSignalClick?.(signal)}
              isSelected={signal.id === selectedSignalId}
            />
          ))
        )}
      </div>
    </div>
  );
}
