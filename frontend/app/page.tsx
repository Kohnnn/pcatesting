'use client';

import { useState, useEffect } from 'react';
import { useSignals } from '@/hooks/useSignals';
import { TradingSignal, DailySentiment, EventStudyData } from '@/types';
import SignalList from '@/components/SignalList';
import SentimentChart from '@/components/SentimentChart';
import EventStudySparkline from '@/components/EventStudySparkline';
import LoadingSkeleton from '@/components/LoadingSkeleton';
import Tooltip, { InfoIcon, TOOLTIP_CONTENT } from '@/components/Tooltip';
import api from '@/services/api';

export default function Home() {
  const { signals, loading: signalsLoading } = useSignals(50);
  const [selectedSignal, setSelectedSignal] = useState<TradingSignal | null>(null);
  const [sentimentData, setSentimentData] = useState<DailySentiment[]>([]);
  const [eventStudyData, setEventStudyData] = useState<EventStudyData | null>(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  useEffect(() => {
    if (selectedSignal) {
      fetchSignalDetails(selectedSignal);
    }
  }, [selectedSignal]);

  const fetchSignalDetails = async (signal: TradingSignal) => {
    setLoadingDetails(true);
    try {
      // Fetch sentiment history
      const sentiment = await api.sentiment.getByTicker(signal.ticker);
      setSentimentData(sentiment);

      // Fetch event study data
      const eventStudy = await api.eventStudy.get(signal.ticker, signal.date);
      setEventStudyData(eventStudy);
    } catch (error) {
      console.error('Failed to fetch signal details:', error);
    } finally {
      setLoadingDetails(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Trading signals based on analyst recommendations and sentiment analysis
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Left column: Signal list */}
        <div>
          <h2 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Recent Signals</h2>
          <SignalList
            signals={signals}
            loading={signalsLoading}
            onSignalClick={setSelectedSignal}
            selectedSignalId={selectedSignal?.id}
          />
        </div>

        {/* Right column: Signal details */}
        <div className="space-y-6">
          {selectedSignal ? (
            <>
              <div className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {selectedSignal.ticker} Details
                </h2>
                <div className="mt-4 space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-400 flex items-center gap-1">
                      Signal Type:
                      <Tooltip content={
                        selectedSignal.signal_type === 'Contrarian Dip Buy' ? TOOLTIP_CONTENT.CONTRARIAN_DIP_BUY :
                        selectedSignal.signal_type === 'Momentum Breakout' ? TOOLTIP_CONTENT.MOMENTUM_BREAKOUT :
                        selectedSignal.signal_type === 'Retail Trap' ? TOOLTIP_CONTENT.RETAIL_TRAP :
                        <span>Signal classification based on market conditions</span>
                      }>
                        <InfoIcon />
                      </Tooltip>
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">{selectedSignal.signal_type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Date:</span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {new Date(selectedSignal.date).toLocaleDateString()}
                    </span>
                  </div>
                  {selectedSignal.analyst_action && (
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Analyst Action:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{selectedSignal.analyst_action}</span>
                    </div>
                  )}
                  {selectedSignal.sentiment_score !== null && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-1">
                        Pure Sentiment Score:
                        <Tooltip content={TOOLTIP_CONTENT.PURE_SENTIMENT}>
                          <InfoIcon />
                        </Tooltip>
                      </span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {selectedSignal.sentiment_score.toFixed(2)}
                      </span>
                    </div>
                  )}
                  {selectedSignal.foreign_flow_score !== null && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-1">
                        NFB (Net Foreign Buy):
                        <Tooltip content={TOOLTIP_CONTENT.NFB}>
                          <InfoIcon />
                        </Tooltip>
                      </span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {selectedSignal.foreign_flow_score.toFixed(2)}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {loadingDetails ? (
                <LoadingSkeleton />
              ) : (
                <>
                  {sentimentData.length > 0 && (
                    <SentimentChart data={sentimentData.slice(-30)} />
                  )}

                  {eventStudyData && (
                    <div className="space-y-4">
                      <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                            Cumulative Abnormal Returns (CAR)
                          </h3>
                          <Tooltip content={TOOLTIP_CONTENT.CAR}>
                            <InfoIcon />
                          </Tooltip>
                        </div>
                        <EventStudySparkline
                          data={eventStudyData}
                          title=""
                          dataKey="car"
                          color="#8884d8"
                        />
                      </div>
                      <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                            Cumulative Abnormal Sentiment (CAS)
                          </h3>
                          <Tooltip content={TOOLTIP_CONTENT.CAS}>
                            <InfoIcon />
                          </Tooltip>
                        </div>
                        <EventStudySparkline
                          data={eventStudyData}
                          title=""
                          dataKey="cas"
                          color="#82ca9d"
                        />
                      </div>
                    </div>
                  )}
                </>
              )}
            </>
          ) : (
            <div className="flex h-64 items-center justify-center rounded-lg bg-white dark:bg-gray-800 shadow">
              <p className="text-gray-500 dark:text-gray-400">Select a signal to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
