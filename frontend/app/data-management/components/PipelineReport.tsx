'use client';

import { PipelineRun } from '@/types';

interface PipelineReportProps {
  run: PipelineRun | null;
  onClose?: () => void;
}

export default function PipelineReport({ run, onClose }: PipelineReportProps) {
  if (!run) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Pipeline Report</h3>
        <p className="text-gray-500 text-center py-8">
          Select a pipeline run to view its report
        </p>
      </div>
    );
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const formatDuration = (startedAt: string, completedAt: string | null) => {
    if (!completedAt) return 'In progress';
    const start = new Date(startedAt).getTime();
    const end = new Date(completedAt).getTime();
    const durationMs = end - start;
    
    if (durationMs < 1000) return `${durationMs} milliseconds`;
    if (durationMs < 60000) return `${Math.round(durationMs / 1000)} seconds`;
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.round((durationMs % 60000) / 1000);
    return `${minutes} minute${minutes !== 1 ? 's' : ''} ${seconds} second${seconds !== 1 ? 's' : ''}`;
  };

  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'running':
        return {
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          textColor: 'text-blue-800',
          icon: (
            <svg className="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ),
          label: 'Running',
        };
      case 'success':
        return {
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          textColor: 'text-green-800',
          icon: (
            <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          ),
          label: 'Completed Successfully',
        };
      case 'partial':
        return {
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          textColor: 'text-yellow-800',
          icon: (
            <svg className="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
          ),
          label: 'Completed with Warnings',
        };
      case 'failed':
        return {
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          textColor: 'text-red-800',
          icon: (
            <svg className="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          ),
          label: 'Failed',
        };
      default:
        return {
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
          textColor: 'text-gray-800',
          icon: null,
          label: status,
        };
    }
  };

  const statusConfig = getStatusConfig(run.status);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Pipeline Report</h3>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        )}
      </div>

      {/* Status banner */}
      <div className={`p-4 rounded-lg border ${statusConfig.bgColor} ${statusConfig.borderColor} mb-6`}>
        <div className="flex items-center gap-3">
          {statusConfig.icon}
          <div>
            <p className={`font-semibold ${statusConfig.textColor}`}>
              {statusConfig.label}
            </p>
            <p className="text-sm text-gray-600">
              Run #{run.id}
            </p>
          </div>
        </div>
      </div>

      {/* Timing information */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Timing</h4>
        <div className="grid grid-cols-1 gap-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500">Started:</span>
            <span className="text-gray-900">{formatDate(run.started_at)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Completed:</span>
            <span className="text-gray-900">{formatDate(run.completed_at)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Duration:</span>
            <span className="text-gray-900">{formatDuration(run.started_at, run.completed_at)}</span>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Statistics</h4>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-gray-900">{run.files_processed}</p>
            <p className="text-xs text-gray-500">Files Processed</p>
          </div>
          <div className="bg-green-50 rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-green-600">{run.records_inserted}</p>
            <p className="text-xs text-gray-500">Records Inserted</p>
          </div>
          <div className="bg-blue-50 rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-blue-600">{run.records_updated}</p>
            <p className="text-xs text-gray-500">Records Updated</p>
          </div>
          <div className={`rounded-lg p-3 text-center ${run.errors_count > 0 ? 'bg-red-50' : 'bg-gray-50'}`}>
            <p className={`text-2xl font-bold ${run.errors_count > 0 ? 'text-red-600' : 'text-gray-400'}`}>
              {run.errors_count}
            </p>
            <p className="text-xs text-gray-500">Errors</p>
          </div>
        </div>
      </div>

      {/* Error details */}
      {run.error_details && run.error_details.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Error Details</h4>
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 max-h-48 overflow-y-auto">
            <ul className="space-y-2">
              {run.error_details.map((error, index) => (
                <li key={index} className="text-sm text-red-700 flex items-start gap-2">
                  <svg className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{error}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Success message when no errors */}
      {run.status === 'success' && run.errors_count === 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <svg className="h-8 w-8 text-green-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <p className="text-sm text-green-700">
            Pipeline completed successfully with no errors!
          </p>
        </div>
      )}
    </div>
  );
}
