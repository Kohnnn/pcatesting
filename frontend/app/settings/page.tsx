'use client';

import { useState, useEffect } from 'react';
import { useSettings } from '@/hooks/useSettings';
import { SignalThresholds } from '@/types';
import LoadingSkeleton from '@/components/LoadingSkeleton';

export default function SettingsPage() {
  const { settings, loading, saving, updateSettings } = useSettings();
  const [formData, setFormData] = useState<SignalThresholds>(settings);
  const [saveMessage, setSaveMessage] = useState('');

  useEffect(() => {
    setFormData(settings);
  }, [settings]);

  const handleChange = (key: keyof SignalThresholds, value: string) => {
    setFormData(prev => ({
      ...prev,
      [key]: parseFloat(value) || 0,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await updateSettings(formData);
    if (success) {
      setSaveMessage('Settings saved successfully!');
      setTimeout(() => setSaveMessage(''), 3000);
    } else {
      setSaveMessage('Failed to save settings. Please try again.');
      setTimeout(() => setSaveMessage(''), 3000);
    }
  };

  const handleReset = () => {
    setFormData(settings);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <LoadingSkeleton />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Configure signal thresholds and display preferences
        </p>
      </div>

      <div className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-6 text-xl font-semibold text-gray-900 dark:text-white">Signal Thresholds</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Sentiment Minimum */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Minimum Sentiment Score
            </label>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Minimum pure sentiment score for Contrarian Dip Buy signals
            </p>
            <input
              type="number"
              step="0.1"
              value={formData.sentiment_min}
              onChange={(e) => handleChange('sentiment_min', e.target.value)}
              className="mt-2 w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* RSI Maximum */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Maximum RSI
            </label>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Maximum RSI value for Momentum Breakout signals (0-100)
            </p>
            <input
              type="number"
              step="1"
              min="0"
              max="100"
              value={formData.rsi_max}
              onChange={(e) => handleChange('rsi_max', e.target.value)}
              className="mt-2 w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* RSI Minimum */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Minimum RSI
            </label>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Minimum RSI value for oversold conditions (0-100)
            </p>
            <input
              type="number"
              step="1"
              min="0"
              max="100"
              value={formData.rsi_min}
              onChange={(e) => handleChange('rsi_min', e.target.value)}
              className="mt-2 w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* BSI Minimum */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Minimum BSI
            </label>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Minimum Buy-Sell Imbalance for Retail Trap signals (0-1)
            </p>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={formData.bsi_min}
              onChange={(e) => handleChange('bsi_min', e.target.value)}
              className="mt-2 w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* BSI Maximum */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Maximum BSI
            </label>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Maximum Buy-Sell Imbalance threshold (0-1)
            </p>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={formData.bsi_max}
              onChange={(e) => handleChange('bsi_max', e.target.value)}
              className="mt-2 w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-between border-t border-gray-200 dark:border-gray-700 pt-6">
            <button
              type="button"
              onClick={handleReset}
              className="rounded-lg border border-gray-300 dark:border-gray-600 px-6 py-2 font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Reset
            </button>
            <button
              type="submit"
              disabled={saving}
              className="rounded-lg bg-blue-600 px-6 py-2 font-medium text-white hover:bg-blue-700 disabled:bg-gray-400"
            >
              {saving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>

          {/* Save message */}
          {saveMessage && (
            <div className={`rounded-lg p-4 text-center ${
              saveMessage.includes('success') 
                ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300' 
                : 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300'
            }`}>
              {saveMessage}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
