'use client';

import { ColumnInfo } from '@/types';

interface DataTableProps {
  data: Record<string, unknown>[];
  columns: ColumnInfo[];
  loading: boolean;
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  sortBy?: string;
  sortOrder: 'asc' | 'desc';
  onPageChange: (page: number) => void;
  onSort: (column: string) => void;
  onRowClick?: (row: Record<string, unknown>) => void;
}

// Rating display mapping (per thesis Table 2 - five-point scale)
const RATING_LABELS: Record<number, { label: string; color: string }> = {
  5: { label: 'Buy', color: 'bg-green-100 text-green-800' },
  4: { label: 'Overweight', color: 'bg-green-50 text-green-700' },
  3: { label: 'Hold', color: 'bg-yellow-100 text-yellow-800' },
  2: { label: 'Underweight', color: 'bg-orange-100 text-orange-800' },
  1: { label: 'Sell', color: 'bg-red-100 text-red-800' },
};

export default function DataTable({
  data,
  columns,
  loading,
  page,
  pageSize,
  total,
  totalPages,
  sortBy,
  sortOrder,
  onPageChange,
  onSort,
  onRowClick,
}: DataTableProps) {
  const formatValue = (value: unknown, dataType: string, columnName?: string): string => {
    if (value === null || value === undefined) return '-';
    
    // Special handling for rating_numeric column (thesis five-point scale)
    if (columnName === 'rating_numeric' && typeof value === 'number') {
      const rating = RATING_LABELS[value];
      return rating ? `${rating.label} (${value})` : String(value);
    }
    
    switch (dataType) {
      case 'date':
      case 'datetime':
        return new Date(value as string).toLocaleDateString();
      case 'float':
        return typeof value === 'number' ? value.toLocaleString(undefined, { 
          minimumFractionDigits: 2, 
          maximumFractionDigits: 2 
        }) : String(value);
      case 'integer':
        return typeof value === 'number' ? value.toLocaleString() : String(value);
      default:
        return String(value);
    }
  };
  
  // Get rating badge styling for rating_numeric column
  const getRatingBadge = (value: unknown, columnName: string) => {
    if (columnName === 'rating_numeric' && typeof value === 'number') {
      const rating = RATING_LABELS[value];
      if (rating) {
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${rating.color}`}>
            {rating.label} ({value})
          </span>
        );
      }
    }
    return null;
  };

  const getSortIcon = (column: string, sortable: boolean) => {
    if (!sortable) return null;
    if (sortBy !== column) return '↕️';
    return sortOrder === 'asc' ? '↑' : '↓';
  };

  // Loading skeleton
  if (loading) {
    return (
      <div className="rounded-lg bg-white shadow">
        <div className="animate-pulse p-4">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          {[...Array(10)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-100 rounded mb-2"></div>
          ))}
        </div>
      </div>
    );
  }

  // Empty state
  if (data.length === 0) {
    return (
      <div className="rounded-lg bg-white shadow">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-4xl mb-4">📭</span>
          <p className="text-gray-500 text-lg">No data found</p>
          <p className="text-gray-400 text-sm mt-1">Try adjusting your filters</p>
        </div>
      </div>
    );
  }

  const startRecord = (page - 1) * pageSize + 1;
  const endRecord = Math.min(page * pageSize, total);

  return (
    <div className="rounded-lg bg-white shadow">
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.name}
                  scope="col"
                  className={`
                    px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider
                    ${column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''}
                  `}
                  onClick={() => column.sortable && onSort(column.name)}
                >
                  <div className="flex items-center gap-1">
                    {column.display_name}
                    <span className="text-gray-400">{getSortIcon(column.name, column.sortable)}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className={`
                  ${onRowClick ? 'cursor-pointer hover:bg-gray-50' : ''}
                  transition-colors
                `}
                onClick={() => onRowClick?.(row)}
              >
                {columns.map((column) => (
                  <td
                    key={column.name}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                  >
                    {getRatingBadge(row[column.name], column.name) || 
                     formatValue(row[column.name], column.data_type, column.name)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div className="flex-1 flex justify-between sm:hidden">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
            className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
        <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-700">
              Showing <span className="font-medium">{startRecord}</span> to{' '}
              <span className="font-medium">{endRecord}</span> of{' '}
              <span className="font-medium">{total.toLocaleString()}</span> results
            </p>
          </div>
          <div>
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                onClick={() => onPageChange(1)}
                disabled={page <= 1}
                className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ««
              </button>
              <button
                onClick={() => onPageChange(page - 1)}
                disabled={page <= 1}
                className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                «
              </button>
              <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => onPageChange(page + 1)}
                disabled={page >= totalPages}
                className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                »
              </button>
              <button
                onClick={() => onPageChange(totalPages)}
                disabled={page >= totalPages}
                className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                »»
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
}
