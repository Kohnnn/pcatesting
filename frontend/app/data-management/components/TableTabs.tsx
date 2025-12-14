'use client';

import { TableInfo } from '@/types';

interface TableTabsProps {
  tables: TableInfo[];
  activeTable: string;
  onTableChange: (tableName: string) => void;
}

// Define the order and which tables to show in tabs
const TAB_ORDER = [
  'instruments',
  'market_data',
  'analyst_recommendations',
  'daily_sentiment',
  'trading_signals',
];

export default function TableTabs({ tables, activeTable, onTableChange }: TableTabsProps) {
  // Filter and order tables according to TAB_ORDER
  const orderedTables = TAB_ORDER
    .map(name => tables.find(t => t.name === name))
    .filter((t): t is TableInfo => t !== undefined);

  return (
    <div className="border-b border-gray-200">
      <nav className="-mb-px flex space-x-8" aria-label="Tabs">
        {orderedTables.map((table) => {
          const isActive = activeTable === table.name;
          return (
            <button
              key={table.name}
              onClick={() => onTableChange(table.name)}
              className={`
                whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors
                ${isActive
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }
              `}
            >
              {table.display_name}
              <span
                className={`ml-2 rounded-full px-2.5 py-0.5 text-xs font-medium
                  ${isActive ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'}
                `}
              >
                {table.record_count.toLocaleString()}
              </span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
