'use client';

import { useState, useRef, useEffect, ReactNode } from 'react';

interface TooltipProps {
  content: ReactNode;
  children: ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
  maxWidth?: string;
}

export default function Tooltip({
  content,
  children,
  position = 'top',
  delay = 200,
  maxWidth = '300px',
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const triggerRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  useEffect(() => {
    if (isVisible && triggerRef.current && tooltipRef.current) {
      const triggerRect = triggerRef.current.getBoundingClientRect();
      const tooltipRect = tooltipRef.current.getBoundingClientRect();
      
      let x = 0;
      let y = 0;

      switch (position) {
        case 'top':
          x = triggerRect.left + (triggerRect.width - tooltipRect.width) / 2;
          y = triggerRect.top - tooltipRect.height - 8;
          break;
        case 'bottom':
          x = triggerRect.left + (triggerRect.width - tooltipRect.width) / 2;
          y = triggerRect.bottom + 8;
          break;
        case 'left':
          x = triggerRect.left - tooltipRect.width - 8;
          y = triggerRect.top + (triggerRect.height - tooltipRect.height) / 2;
          break;
        case 'right':
          x = triggerRect.right + 8;
          y = triggerRect.top + (triggerRect.height - tooltipRect.height) / 2;
          break;
      }

      // Keep tooltip within viewport
      x = Math.max(8, Math.min(x, window.innerWidth - tooltipRect.width - 8));
      y = Math.max(8, Math.min(y, window.innerHeight - tooltipRect.height - 8));

      setCoords({ x, y });
    }
  }, [isVisible, position]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <>
      <div
        ref={triggerRef}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        onFocus={showTooltip}
        onBlur={hideTooltip}
        className="inline-flex items-center"
      >
        {children}
      </div>
      {isVisible && (
        <div
          ref={tooltipRef}
          className="fixed z-50 px-3 py-2 text-sm rounded-lg shadow-lg
            bg-gray-900 dark:bg-gray-100 
            text-white dark:text-gray-900
            border border-gray-700 dark:border-gray-300"
          style={{
            left: coords.x,
            top: coords.y,
            maxWidth,
          }}
        >
          {content}
          <div
            className={`absolute w-2 h-2 rotate-45 
              bg-gray-900 dark:bg-gray-100
              ${position === 'top' ? 'bottom-[-4px] left-1/2 -translate-x-1/2' : ''}
              ${position === 'bottom' ? 'top-[-4px] left-1/2 -translate-x-1/2' : ''}
              ${position === 'left' ? 'right-[-4px] top-1/2 -translate-y-1/2' : ''}
              ${position === 'right' ? 'left-[-4px] top-1/2 -translate-y-1/2' : ''}
            `}
          />
        </div>
      )}
    </>
  );
}

// Info icon component for tooltips
export function InfoIcon({ className = '' }: { className?: string }) {
  return (
    <svg
      className={`w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 cursor-help ${className}`}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" strokeWidth="2" />
      <path strokeWidth="2" d="M12 16v-4M12 8h.01" />
    </svg>
  );
}

// Pre-defined tooltip content for financial terms
export const TOOLTIP_CONTENT = {
  // Sentiment Indicators
  BSI: (
    <div>
      <strong>BSI (Buy-Sell Imbalance)</strong>
      <p className="mt-1">Ratio of buy volume to total volume, indicating buying pressure.</p>
      <p className="mt-1 font-mono text-xs">BSI = Buy Volume / (Buy + Sell Volume)</p>
      <p className="mt-1 text-xs opacity-80">Range: [0, 1] where 0.5 = neutral</p>
    </div>
  ),
  ATR: (
    <div>
      <strong>ATR (Adjusted Turnover Ratio)</strong>
      <p className="mt-1">Trading volume divided by shares outstanding.</p>
      <p className="mt-1 font-mono text-xs">ATR = Trading Volume / Shares Outstanding</p>
      <p className="mt-1 text-xs opacity-80">Higher values = more active trading</p>
    </div>
  ),
  LTV: (
    <div>
      <strong>LTV (Log Trading Volume)</strong>
      <p className="mt-1">Natural logarithm of trading volume for normalization.</p>
      <p className="mt-1 font-mono text-xs">LTV = ln(Trading Volume)</p>
      <p className="mt-1 text-xs opacity-80">Normalizes volume across market caps</p>
    </div>
  ),
  RSI: (
    <div>
      <strong>RSI (Relative Strength Index)</strong>
      <p className="mt-1">14-day momentum indicator measuring price change speed.</p>
      <p className="mt-1 font-mono text-xs">RSI = 100 - (100 / (1 + RS))</p>
      <p className="mt-1 text-xs opacity-80">&gt;70 = overbought, &lt;30 = oversold</p>
    </div>
  ),
  PLI: (
    <div>
      <strong>PLI (Psychological Line Index)</strong>
      <p className="mt-1">Proportion of recent days with price increases.</p>
      <p className="mt-1 font-mono text-xs">PLI = Up Days / Total Days</p>
      <p className="mt-1 text-xs opacity-80">&gt;0.75 = bullish, &lt;0.25 = bearish</p>
    </div>
  ),
  
  // Event Study Metrics
  CAR: (
    <div>
      <strong>CAR (Cumulative Abnormal Return)</strong>
      <p className="mt-1">Sum of daily abnormal returns over an event window.</p>
      <p className="mt-1 text-xs opacity-80">Measures price reaction to analyst recommendations</p>
    </div>
  ),
  CAS: (
    <div>
      <strong>CAS (Cumulative Abnormal Sentiment)</strong>
      <p className="mt-1">Sum of daily abnormal sentiment scores over an event window.</p>
      <p className="mt-1 text-xs opacity-80">Measures sentiment reaction to recommendations</p>
    </div>
  ),
  
  // Signal Types
  CONTRARIAN_DIP_BUY: (
    <div>
      <strong>Contrarian Dip Buy Signal</strong>
      <p className="mt-1">Triggered when analysts downgrade but sentiment remains high and foreign investors are buying.</p>
      <p className="mt-1 text-xs opacity-80">Based on the &quot;Downgrade Puzzle&quot; phenomenon</p>
    </div>
  ),
  MOMENTUM_BREAKOUT: (
    <div>
      <strong>Momentum Breakout Signal</strong>
      <p className="mt-1">Triggered when analysts upgrade with rising sentiment and RSI below overbought levels.</p>
      <p className="mt-1 text-xs opacity-80">Indicates strong momentum with room to run</p>
    </div>
  ),
  RETAIL_TRAP: (
    <div>
      <strong>Retail Trap Signal</strong>
      <p className="mt-1">Triggered when analysts downgrade but retail buying pressure remains high while foreign investors sell.</p>
      <p className="mt-1 text-xs opacity-80">Warning: Further downside likely</p>
    </div>
  ),
  
  // Other Terms
  NFB: (
    <div>
      <strong>NFB (Net Foreign Buy)</strong>
      <p className="mt-1">Net foreign institutional buying activity.</p>
      <p className="mt-1 text-xs opacity-80">Positive = foreign investors are net buyers</p>
    </div>
  ),
  PURE_SENTIMENT: (
    <div>
      <strong>Pure Sentiment</strong>
      <p className="mt-1">Sentiment residual after regressing against market returns.</p>
      <p className="mt-1 text-xs opacity-80">Isolates firm-specific sentiment from market-wide movements</p>
    </div>
  ),
  PCA_SENTIMENT: (
    <div>
      <strong>PCA Composite Sentiment</strong>
      <p className="mt-1">Five sentiment proxies combined using Principal Component Analysis.</p>
      <p className="mt-1 font-mono text-xs">S = F₁×BSI + F₂×ATR + F₃×LTV + F₄×RSI + F₅×PLI</p>
    </div>
  ),
};
