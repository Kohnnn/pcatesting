/**
 * Shared utilities for chart components
 * Provides export functionality and common helpers
 */

/**
 * Export data to CSV file
 */
export function exportToCSV(
  data: Record<string, unknown>[],
  headers: string[],
  filename: string
): void {
  if (!data.length) return;

  const csvContent = [
    headers.join(','),
    ...data.map((row) =>
      headers.map((header) => {
        const value = row[header];
        // Handle strings with commas or quotes
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value ?? '';
      }).join(',')
    ),
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}_${new Date().toISOString().split('T')[0]}.csv`;
  link.click();
  URL.revokeObjectURL(link.href);
}

/**
 * Export chart SVG to PNG image
 */
export function exportChartToImage(
  chartRef: React.RefObject<HTMLDivElement>,
  filename: string
): void {
  if (!chartRef.current) return;

  const svg = chartRef.current.querySelector('svg');
  if (!svg) return;

  const svgData = new XMLSerializer().serializeToString(svg);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const img = new Image();

  img.onload = () => {
    canvas.width = img.width * 2; // 2x for better quality
    canvas.height = img.height * 2;
    ctx?.scale(2, 2);
    ctx?.drawImage(img, 0, 0);
    const link = document.createElement('a');
    link.download = `${filename}_${new Date().toISOString().split('T')[0]}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  };

  img.src = 'data:image/svg+xml;base64,' + btoa(decodeURIComponent(encodeURIComponent(svgData)));
}

/**
 * Format number for display in tooltips
 */
export function formatNumber(value: number | null | undefined, decimals: number = 2): string {
  if (value === null || value === undefined || isNaN(value)) return 'N/A';
  return value.toFixed(decimals);
}

/**
 * Format percentage for display
 */
export function formatPercent(value: number | null | undefined, decimals: number = 1): string {
  if (value === null || value === undefined || isNaN(value)) return 'N/A';
  return (value * 100).toFixed(decimals) + '%';
}

/**
 * Format large numbers with K/M/B suffixes
 */
export function formatCompactNumber(value: number | null | undefined): string {
  if (value === null || value === undefined || isNaN(value)) return 'N/A';
  
  const absValue = Math.abs(value);
  if (absValue >= 1e9) return (value / 1e9).toFixed(1) + 'B';
  if (absValue >= 1e6) return (value / 1e6).toFixed(1) + 'M';
  if (absValue >= 1e3) return (value / 1e3).toFixed(1) + 'K';
  return value.toFixed(0);
}

/**
 * Format date for display
 */
export function formatDate(date: string | Date, format: 'short' | 'medium' | 'long' = 'medium'): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  
  switch (format) {
    case 'short':
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    case 'long':
      return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    default:
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: '2-digit' });
  }
}

/**
 * Common chart colors
 */
export const CHART_COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  tertiary: '#f59e0b',
  quaternary: '#8b5cf6',
  danger: '#ef4444',
  neutral: '#6b7280',
  grid: '#e5e7eb',
  background: '#f9fafb',
};

/**
 * Signal type colors
 */
export const SIGNAL_COLORS: Record<string, string> = {
  'Contrarian Dip Buy': '#10b981',
  'Momentum Breakout': '#3b82f6',
  'Retail Trap': '#ef4444',
  'Neutral / No Edge': '#9ca3af',
};

/**
 * Rating colors (1-5 scale)
 */
export const RATING_COLORS: Record<number, string> = {
  5: '#10b981', // Buy - Green
  4: '#22c55e', // Overweight - Light green
  3: '#f59e0b', // Hold - Yellow
  2: '#f97316', // Underweight - Orange
  1: '#ef4444', // Sell - Red
};

/**
 * Sentiment proxy colors
 */
export const PROXY_COLORS: Record<string, string> = {
  bsi: '#3b82f6',
  atr: '#10b981',
  ltv: '#f59e0b',
  rsi: '#8b5cf6',
  pli: '#ef4444',
};

/**
 * Common tooltip styles for recharts
 */
export const TOOLTIP_STYLE = {
  contentStyle: {
    backgroundColor: 'white',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    padding: '12px',
  },
  labelStyle: {
    fontWeight: 600,
    marginBottom: '4px',
  },
};
