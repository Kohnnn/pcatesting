export default function AboutPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">About Vietnam SentimentAlpha by Daniel</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Academic methodology, thesis terminology, and signal explanations
        </p>
      </div>

      {/* Thesis Summary Section */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">Research Thesis</h2>
        <div className="prose dark:prose-invert max-w-none">
          <h3 className="text-lg font-semibold text-blue-800 dark:text-blue-400">
            Investor Sentiment and Analyst Recommendations in Vietnam Stock Market
          </h3>
          
          <div className="mt-4 space-y-4 text-gray-700 dark:text-gray-300">
            <p>
              This research investigates the relationship between investor sentiment and analyst recommendations 
              in the Vietnamese stock market, with a focus on understanding how sentiment dynamics influence 
              market reactions to analyst actions.
            </p>
            
            <h4 className="font-semibold text-gray-900 dark:text-white">Key Research Questions</h4>
            <ul className="list-disc ml-6 space-y-2">
              <li>How does investor sentiment respond to analyst recommendation changes?</li>
              <li>Does the &quot;Downgrade Puzzle&quot; exist in Vietnam&apos;s emerging market?</li>
              <li>Can sentiment indicators predict abnormal returns following analyst actions?</li>
              <li>What role do foreign institutional investors play in sentiment dynamics?</li>
            </ul>
            
            <h4 className="font-semibold text-gray-900 dark:text-white">Methodology</h4>
            <p>
              The study employs a composite sentiment index constructed from five proxies (BSI, ATR, LTV, RSI, PLI) 
              using Principal Component Analysis. Event study methodology is applied to measure Cumulative Abnormal 
              Returns (CAR) and Cumulative Abnormal Sentiment (CAS) around analyst recommendation changes.
            </p>
            
            <h4 className="font-semibold text-gray-900 dark:text-white">Key Findings</h4>
            <ul className="list-disc ml-6 space-y-2">
              <li>
                <strong>Downgrade Puzzle:</strong> Severe analyst downgrades in Vietnam paradoxically lead to 
                positive price drifts, contrary to efficient market expectations.
              </li>
              <li>
                <strong>Sentiment Predictability:</strong> High sentiment levels following downgrades, combined 
                with positive foreign flows, predict positive abnormal returns.
              </li>
              <li>
                <strong>Foreign vs Retail Divergence:</strong> When foreign institutional investors diverge from 
                retail sentiment, foreign flows tend to be more predictive of future returns.
              </li>
            </ul>
            
            <h4 className="font-semibold text-gray-900 dark:text-white">Practical Applications</h4>
            <p>
              The SentimentAlpha platform translates these academic findings into actionable trading signals:
            </p>
            <ul className="list-disc ml-6 space-y-2">
              <li><strong>Contrarian Dip Buy:</strong> Identifies downgrade overreactions with bullish sentiment</li>
              <li><strong>Momentum Breakout:</strong> Captures upgrade momentum with technical confirmation</li>
              <li><strong>Retail Trap:</strong> Warns of potential downside when retail diverges from institutions</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Comprehensive Glossary */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">Comprehensive Glossary</h2>
        
        {/* Sentiment Indicators */}
        <div className="mb-6">
          <h3 className="mb-3 text-lg font-semibold text-blue-800 dark:text-blue-400 border-b border-blue-200 dark:border-blue-800 pb-2">
            Sentiment Indicators (Five Proxies)
          </h3>
          <div className="space-y-4">
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">BSI (Buy-Sell Imbalance)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Ratio of buy volume to total volume, indicating buying pressure.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                BSI = Buy Volume / (Buy Volume + Sell Volume)
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Range: [0, 1] where 0.5 = neutral</p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">ATR (Adjusted Turnover Ratio)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Trading volume divided by shares outstanding, adjusted for price movements.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                ATR = Trading Volume / Shares Outstanding
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Higher values indicate more active trading</p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">LTV (Log Trading Volume)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Natural logarithm of trading volume for normalization across different stock sizes.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                LTV = ln(Trading Volume)
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Normalizes volume across different market caps</p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">RSI (Relative Strength Index)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                14-day momentum indicator measuring speed and magnitude of price changes.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                RSI = 100 - (100 / (1 + RS)), where RS = Avg Gain / Avg Loss
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Range: [0, 100] where &gt;70 = overbought, &lt;30 = oversold</p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">PLI (Psychological Line Index)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Proportion of recent trading days with price increases over a lookback period.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                PLI = (Days with Price Increase) / (Total Days in Period)
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Range: [0, 1] where &gt;0.75 = bullish, &lt;0.25 = bearish</p>
            </div>
          </div>
        </div>

        {/* PCA Sentiment Formula */}
        <div className="mb-6">
          <h3 className="mb-3 text-lg font-semibold text-purple-800 dark:text-purple-400 border-b border-purple-200 dark:border-purple-800 pb-2">
            PCA Composite Sentiment Index
          </h3>
          <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
              The five sentiment proxies are combined using Principal Component Analysis (PCA) 
              to create a single composite sentiment score:
            </p>
            <div className="bg-white dark:bg-gray-800 p-3 rounded font-mono text-sm overflow-x-auto text-gray-900 dark:text-gray-100">
              S<sub>i,t</sub> = F<sub>BSI</sub> × BSI + F<sub>ATR</sub> × ATR + F<sub>LTV</sub> × LTV + F<sub>RSI</sub> × RSI + F<sub>PLI</sub> × PLI
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Where F<sub>x</sub> represents the factor loading for each proxy from PCA
            </p>
          </div>
        </div>

        {/* Event Study Metrics */}
        <div className="mb-6">
          <h3 className="mb-3 text-lg font-semibold text-green-800 dark:text-green-400 border-b border-green-200 dark:border-green-800 pb-2">
            Event Study Metrics
          </h3>
          <div className="space-y-4">
            <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">CAR (Cumulative Abnormal Return)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Sum of daily abnormal returns over an event window, measuring price reaction 
                to analyst recommendations.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                CAR = Σ AR<sub>t</sub> for t in [-25, +25]
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                AR<sub>t</sub> = Actual Return - Expected Return (from market model)
              </p>
            </div>
            
            <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white">CAS (Cumulative Abnormal Sentiment)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Sum of daily abnormal sentiment scores over an event window, measuring 
                sentiment reaction to analyst recommendations.
              </p>
              <div className="mt-2 bg-white dark:bg-gray-800 p-2 rounded font-mono text-sm text-gray-900 dark:text-gray-100">
                CAS = Σ AS<sub>t</sub> for t in [-25, +25]
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                AS<sub>t</sub> = Actual Sentiment - Expected Sentiment
              </p>
            </div>
          </div>
        </div>

        {/* Other Key Terms */}
        <div className="mb-6">
          <h3 className="mb-3 text-lg font-semibold text-gray-800 dark:text-gray-200 border-b border-gray-200 dark:border-gray-700 pb-2">
            Other Key Terms
          </h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white">Pure Sentiment</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Sentiment residual after regressing against market returns, isolating 
                firm-specific sentiment from market-wide movements.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white">NFB (Net Foreign Buy)</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Net foreign institutional buying, critical for Vietnam market signals. 
                Positive NFB indicates foreign investors are net buyers.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white">Downgrade Puzzle</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Market anomaly where severe analyst downgrades lead to positive price 
                drifts in Vietnam, contrary to efficient market expectations.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white">Rating Standardization</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Mapping diverse brokerage rating terminology to a 1-5 numeric scale 
                for consistent analysis.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Rating Scale */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">Rating Scale (Five-Point)</h2>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
          Per thesis Table 2, analyst ratings are standardized to a five-point numeric scale:
        </p>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Grade</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Numeric</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Rating Terms</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300">Buy</span>
                </td>
                <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">5</td>
                <td className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">buy, strong buy, add, accumulate</td>
              </tr>
              <tr>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400">Overweight</span>
                </td>
                <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">4</td>
                <td className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">outperform, overweight, overwt/in-line</td>
              </tr>
              <tr>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300">Hold</span>
                </td>
                <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">3</td>
                <td className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">hold, market perform, neutral</td>
              </tr>
              <tr>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-100 dark:bg-orange-900/50 text-orange-800 dark:text-orange-300">Underweight</span>
                </td>
                <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">2</td>
                <td className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">underperform, underweight</td>
              </tr>
              <tr>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300">Sell</span>
                </td>
                <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">1</td>
                <td className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">reduce, sell, strong sell</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Signal Types */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">Signal Types</h2>
        <div className="space-y-6">
          <div className="border-l-4 border-green-500 bg-green-50 dark:bg-green-900/30 p-4">
            <h3 className="text-lg font-semibold text-green-900 dark:text-green-300">Contrarian Dip Buy</h3>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Thesis:</strong> When analysts downgrade a stock but sentiment remains high and foreign 
              investors are buying, it suggests the downgrade is overreaction and presents a buying opportunity.
            </p>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Conditions:</strong>
            </p>
            <ul className="ml-4 mt-1 list-disc text-sm text-gray-700 dark:text-gray-300">
              <li>Analyst issues a downgrade (rating decrease)</li>
              <li>Pure Sentiment &gt; 1.0 (elevated sentiment)</li>
              <li>NFB &gt; 0 (foreign investors net buying)</li>
            </ul>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Academic Support:</strong> Based on the &quot;Downgrade Puzzle&quot; phenomenon documented in 
              Vietnamese markets where severe downgrades lead to positive price drifts.
            </p>
          </div>

          <div className="border-l-4 border-blue-500 bg-blue-50 dark:bg-blue-900/30 p-4">
            <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-300">Momentum Breakout</h3>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Thesis:</strong> When analysts upgrade a stock with rising sentiment and RSI below 
              overbought levels, it indicates strong momentum with room to run.
            </p>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Conditions:</strong>
            </p>
            <ul className="ml-4 mt-1 list-disc text-sm text-gray-700 dark:text-gray-300">
              <li>Analyst issues an upgrade (rating increase)</li>
              <li>Sentiment slope &gt; 0 (rising sentiment trend)</li>
              <li>RSI &lt; 70 (not overbought)</li>
            </ul>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Academic Support:</strong> Momentum strategies combined with analyst upgrades have 
              shown positive returns in emerging markets.
            </p>
          </div>

          <div className="border-l-4 border-red-500 bg-red-50 dark:bg-red-900/30 p-4">
            <h3 className="text-lg font-semibold text-red-900 dark:text-red-300">Retail Trap</h3>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Thesis:</strong> When analysts downgrade but retail buying pressure remains high while 
              foreign investors are selling, it suggests retail investors are trapped and further downside is likely.
            </p>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Conditions:</strong>
            </p>
            <ul className="ml-4 mt-1 list-disc text-sm text-gray-700 dark:text-gray-300">
              <li>Analyst issues a downgrade (rating decrease)</li>
              <li>BSI &gt; 0.5 (retail buying pressure)</li>
              <li>NFB &lt; 0 (foreign investors net selling)</li>
            </ul>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Academic Support:</strong> Divergence between retail and institutional flows often 
              precedes negative returns in emerging markets.
            </p>
          </div>

          <div className="border-l-4 border-gray-500 bg-gray-50 dark:bg-gray-700/50 p-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Neutral / No Edge</h3>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Thesis:</strong> Conditions do not match any specific pattern with statistical edge 
              based on the thesis methodology.
            </p>
            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
              <strong className="text-gray-900 dark:text-white">Conditions:</strong> All other combinations of analyst actions and market conditions 
              that don&apos;t meet the criteria for actionable signals.
            </p>
          </div>
        </div>
      </section>

      {/* Downgrade Puzzle */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">The Downgrade Puzzle</h2>
        <div className="space-y-4 text-gray-700 dark:text-gray-300">
          <p>
            The &quot;Downgrade Puzzle&quot; is a market anomaly documented in Vietnamese stock markets where 
            severe analyst downgrades paradoxically lead to positive price drifts rather than the 
            expected negative returns.
          </p>
          <p>
            <strong className="text-gray-900 dark:text-white">Key Findings:</strong>
          </p>
          <ul className="ml-6 list-disc space-y-2">
            <li>
              Severe downgrades (from Buy to Sell) show positive cumulative abnormal returns (CAR) 
              in the 25 days following the announcement
            </li>
            <li>
              This effect is strongest when accompanied by high investor sentiment and positive 
              foreign institutional flows (NFB &gt; 0)
            </li>
            <li>
              The puzzle suggests that severe downgrades in Vietnam often represent overreaction, 
              creating contrarian buying opportunities
            </li>
            <li>
              Statistical significance has been confirmed through event study methodology with 
              T-tests on CAR and CAS values
            </li>
          </ul>
          <p>
            <strong className="text-gray-900 dark:text-white">Practical Application:</strong>
          </p>
          <p>
            The SentimentAlpha platform identifies these opportunities through the &quot;Contrarian Dip Buy&quot; 
            signal, which combines analyst downgrades with sentiment analysis and foreign flow data to 
            pinpoint potential mispricings.
          </p>
        </div>
      </section>

      {/* Methodology */}
      <section className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
        <h2 className="mb-4 text-2xl font-semibold text-gray-900 dark:text-white">Methodology</h2>
        <div className="space-y-4 text-gray-700 dark:text-gray-300">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">1. Data Collection</h3>
            <p className="text-sm">
              Market data including prices, volumes, analyst recommendations, and foreign flows 
              are collected from FiinPro and Bloomberg platforms for Vietnamese stock exchanges.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">2. Sentiment Index Construction</h3>
            <p className="text-sm">
              Five sentiment proxies (BSI, ATR, LTV, RSI, PLI) are calculated and combined 
              using Principal Component Analysis (PCA) to create a composite sentiment index.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">3. Sentiment Purification</h3>
            <p className="text-sm">
              Raw sentiment is purified by regressing against market returns to isolate 
              firm-specific sentiment from market-wide movements, producing &quot;Pure Sentiment&quot;.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">4. Event Study Analysis</h3>
            <p className="text-sm">
              CAR and CAS are calculated over event windows (-25 to +25 days) around analyst 
              recommendation changes to measure market and sentiment reactions.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">5. Signal Generation</h3>
            <p className="text-sm">
              Trading signals are generated by combining analyst actions with sentiment indicators 
              and foreign flow data (NFB) according to predefined rules validated by academic research.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
