import { useState, useEffect } from 'react';
import { SignalThresholds } from '@/types';
import api from '@/services/api';

const DEFAULT_SETTINGS: SignalThresholds = {
  sentiment_min: 1.0,
  rsi_max: 70,
  rsi_min: 30,
  bsi_min: 0.4,
  bsi_max: 0.6,
};

export function useSettings() {
  const [settings, setSettings] = useState<SignalThresholds>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setLoading(true);
        const data = await api.settings.get();
        setSettings(data);
        // Cache in localStorage
        localStorage.setItem('settings', JSON.stringify(data));
        setError(null);
      } catch (err) {
        // Fall back to localStorage if API fails
        const cached = localStorage.getItem('settings');
        if (cached) {
          setSettings(JSON.parse(cached));
        }
        setError(err instanceof Error ? err.message : 'Failed to fetch settings');
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const updateSettings = async (newSettings: SignalThresholds) => {
    try {
      setSaving(true);
      const data = await api.settings.update(newSettings);
      setSettings(data);
      // Update localStorage cache
      localStorage.setItem('settings', JSON.stringify(data));
      setError(null);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update settings');
      return false;
    } finally {
      setSaving(false);
    }
  };

  return { settings, loading, error, saving, updateSettings };
}
