'use client';

import { useState, useEffect, useCallback } from 'react';
import TableTabs from './components/TableTabs';
import DataTable from './components/DataTable';
import FilterPanel from './components/FilterPanel';
import InstrumentDetail from './components/InstrumentDetail';
import PipelineControl from './components/PipelineControl';
import PipelineHistory from './components/PipelineHistory';
import PipelineReport from './components/PipelineReport';
import DataQualityDashboard from './components/DataQualityDashboard';
import api from '@/services/api';
import { TableInfo, PaginatedResponse, InstrumentDetail as InstrumentDetailType, PipelineRun } from '@/types';

export default function DataManagementPage() {
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [activeTable, setActiveTable] = useState<string>('instruments');
  const [tableData, setTableData] = useState<PaginatedResponse<Record<string, unknown>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(50);
  const [sortBy, setSortBy] = useState<string | undefined>(undefined);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filters, setFilters] = useState<{
    ticker?: string;
    startDate?: string;
    endDate?: string;
    signalType?: string;
  }>({});
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null);
  const [instrumentDetail, setInstrumentDetail] = useState<InstrumentDetailType | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [selectedPipelineRun, setSelectedPipelineRun] = useState<PipelineRun | null>(null);
  const [pipelineRefreshTrigger, setPipelineRefreshTrigger] = useState(0);

  const fetchTables = useCallback(async () => {
    try {
      const data = await api.dataManagement.getTables();
      setTables(data);
    } catch (error) {
      console.error('Failed to fetch tables:', error);
    }
  }, []);

  const fetchTableData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.dataManagement.getTableData(activeTable, {
        page,
        pageSize,
        sortBy,
        sortOrder,
        ...filters,
      });
      setTableData(data);
    } catch (error) {
      console.error('Failed to fetch table data:', error);
    } finally {
      setLoading(false);
    }
  }, [activeTable, page, pageSize, sortBy, sortOrder, filters]);

  const fetchInstrumentDetail = useCallback(async (ticker: string) => {
    setLoadingDetail(true);
    try {
      const data = await api.dataManagement.getInstrumentDetail(ticker);
      setInstrumentDetail(data);
    } catch (error) {
      console.error('Failed to fetch instrument detail:', error);
    } finally {
      setLoadingDetail(false);
    }
  }, []);

  // Fetch table list on mount
  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  // Fetch table data when active table, page, sort, or filters change
  useEffect(() => {
    fetchTableData();
  }, [fetchTableData]);

  // Fetch instrument detail when ticker is selected
  useEffect(() => {
    if (selectedTicker) {
      fetchInstrumentDetail(selectedTicker);
    } else {
      setInstrumentDetail(null);
    }
  }, [selectedTicker, fetchInstrumentDetail]);

  const handleTableChange = (tableName: string) => {
    setActiveTable(tableName);
    setPage(1);
    setSortBy(undefined);
    setFilters({});
    setSelectedTicker(null);
  };

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
    setPage(1);
  };

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
    setPage(1);
  };

  const handleRowClick = (row: Record<string, unknown>) => {
    if (row.ticker && typeof row.ticker === 'string') {
      setSelectedTicker(row.ticker);
    }
  };

  const handleCloseDetail = () => {
    setSelectedTicker(null);
  };

  const handlePipelineComplete = (run: PipelineRun) => {
    setSelectedPipelineRun(run);
    setPipelineRefreshTrigger(prev => prev + 1);
    // Refresh table data after pipeline completes
    fetchTables();
    fetchTableData();
  };

  const handleSelectPipelineRun = (run: PipelineRun) => {
    setSelectedPipelineRun(run);
  };

  const handleClosePipelineReport = () => {
    setSelectedPipelineRun(null);
  };

  const activeTableInfo = tables.find(t => t.name === activeTable);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Data Management</h1>
        <p className="mt-2 text-gray-600">
          Browse and manage database contents
        </p>
      </div>

      {/* Pipeline UI Section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <PipelineControl onPipelineComplete={handlePipelineComplete} />
        </div>
        <div className="lg:col-span-1">
          <PipelineHistory
            refreshTrigger={pipelineRefreshTrigger}
            onSelectRun={handleSelectPipelineRun}
          />
        </div>
        <div className="lg:col-span-1">
          <PipelineReport
            run={selectedPipelineRun}
            onClose={handleClosePipelineReport}
          />
        </div>
      </div>

      {/* Data Quality Dashboard */}
      <DataQualityDashboard />

      {/* Table tabs */}
      <TableTabs
        tables={tables}
        activeTable={activeTable}
        onTableChange={handleTableChange}
      />

      {/* Filter panel */}
      <FilterPanel
        activeTable={activeTable}
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Data table */}
        <div className={selectedTicker ? 'lg:col-span-2' : 'lg:col-span-3'}>
          <DataTable
            data={tableData?.data || []}
            columns={activeTableInfo?.columns || []}
            loading={loading}
            page={page}
            pageSize={pageSize}
            total={tableData?.total || 0}
            totalPages={tableData?.total_pages || 1}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onPageChange={setPage}
            onSort={handleSort}
            onRowClick={handleRowClick}
          />
        </div>

        {/* Instrument detail panel */}
        {selectedTicker && (
          <div className="lg:col-span-1">
            <InstrumentDetail
              detail={instrumentDetail}
              loading={loadingDetail}
              onClose={handleCloseDetail}
            />
          </div>
        )}
      </div>
    </div>
  );
}
