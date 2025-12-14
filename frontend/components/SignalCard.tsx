'use client';

import { TradingSignal } from '@/types';
import Tooltip, { InfoIcon, TOOLTIP_CONTENT } from './Tooltip';

interface SignalCardProps {
  signal: TradingSignal;
  onClick?: () => void;
  isSelected?: boolean;
}

const signalColors = {
  'Contrarian Dip Buy': {
    bg: 'bg-green-50 dark:bg-green-900/30',
    border: 'border-green-500',
    text: 'text-green-700 dark:text-green-300',
    badge: 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300',
  },
  'Momentum Breakout': {
    bg: 'bg-blue-50 dark:bg-blue-900/30',
    border: 'border-blue-500',
    text: 'text-blue-700 dark:text-blue-300',
    badge: 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300',
  },
  'Retail Trap': {
    bg: 'bg-red-50 dark:bg-red-900/30',
    border: 'border-red-500',
    text: 'text-red-700 dark:text-red-300',
    badge: 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300',
  },
  'Neutral / No Edge': {
    bg: 'bg-gray-50 dark:bg-gray-800',
    border: 'border-gray-500',
    text: 'text-gray-700 dark:text-gray-300',
    badge: 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300',
  },
};

const signalTooltips = {
  'Contrarian Dip Buy': TOOLTIP_CONTENT.CONTRARIAN_DIP_BUY,
  'Momentum Breakout': TOOLTIP_CONTENT.MOMENTUM_BREAKOUT,
  'Retail Trap': TOOLTIP_CONTENT.RETAIL_TRAP,
};

export default function SignalCard({ signal, onClick, isSelected }: SignalCardProps) {
  const colors = signalColors[signal.signal_type as keyof typeof signalColors] || signalColors['Neutral / No Edge'];
  const tooltipContent = signalTooltips[signal.signal_type as keyof typeof signalTooltips];

  return (
    <div
      onClick={onClick}
      className={`
        rounded-lg border-l-4 p-4 shadow-sm transition-all cursor-pointer
        ${colors.bg} ${colors.border}
        ${isSelected ? 'ring-2 ring-offset-2 ring-blue-500 dark:ring-offset-gray-900' : 'hover:shadow-md'}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">{signal.ticker}</h3>
            <span className={`rounded-full px-2 py-1 text-xs font-medium ${colors.badge}`}>
              {signal.signal_type}
            </span>
            {tooltipContent && (
              <Tooltip content={tooltipContent}>
                <InfoIcon />
              </Tooltip>
            )}
          </div>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            {new Date(signal.date).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'short', 
              day: 'numeric' 
            })}
          </p>
          {signal.analyst_action && (
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <span className="font-medium">Action:</span> {signal.analyst_action}
            </p>
          )}
          <div className="mt-2 flex gap-4 text-xs text-gray-600 dark:text-gray-400">
            {signal.sentiment_score !== null && (
              <span className="flex items-center gap-1">
                Pure Sentiment: {signal.sentiment_score.toFixed(2)}
                <Tooltip content={TOOLTIP_CONTENT.PURE_SENTIMENT}>
                  <InfoIcon className="w-3 h-3" />
                </Tooltip>
              </span>
            )}
            {signal.foreign_flow_score !== null && (
              <span className="flex items-center gap-1">
                NFB: {signal.foreign_flow_score.toFixed(2)}
                <Tooltip content={TOOLTIP_CONTENT.NFB}>
                  <InfoIcon className="w-3 h-3" />
                </Tooltip>
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
