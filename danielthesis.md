**LIST OF TABLES**

[Table 1: VNIndex's trading value by investor types (VNDbn) 21](#_Toc200485280)

[Table 2: Summary of collected ratings 24](#_Toc200485281)

[Table 3: Summary of recommendations changes 26](#_Toc200485282)

[Table 4: Proxies for the investor sentiment index 29](#_Toc200485283)

[Table 5: PCA explained variance ratio 31](#_Toc200485284)

[Table 6: PCA descriptive summary 31](#_Toc200485285)

[Table 7: PCA loadings 31](#_Toc200485286)

[Table 8: Correlation between PC1 and each proxy 32](#_Toc200485287)

[Table 9: Investor sentiment descriptive summary 35](#_Toc200485288)

[Table 10: Summary of upgrades' impact on CAR 42](#_Toc200485289)

[Table 11: Summary of downgrades' impact on CAR 46](#_Toc200485290)

[Table 12: Summary of upgrades' impact on CAS 51](#_Toc200485291)

[Table 13: Summary of downgrades' impact on CAS 54](#_Toc200485292)

**LIST OF FIGURES**

[Figure 1: Visualization of CAR for each category 50](#_Toc200485300)

[Figure 2: Visualization of CAS for each category 57](#_Toc200485301)

**REACTION OF STOCK PRICES TO CHANGES IN ANALYSTS' RECOMMENDATIONS**

**IN THE VIETNAMESE STOCK MARKET**

**ABSTRACT**

This thesis investigates the dual impact of financial analyst recommendations on stock prices, as expressed directly through stock returns and indirectly through investor sentiment within the unique context of the Vietnamese stock market - a frontier market on the verge of an emerging market upgrade, characterized by significant retail investor participation and documented herding behavior. Addressing a gap in contemporary research, this study analyzes how expert opinions shape market dynamics in this rapidly evolving economy.

Employing a comprehensive dataset of 7,185 recommendation changes from 2015 to 2024, this study utilizes a two-pronged event-study framework: one for the direct investigation into stock prices' reaction, the other looks for the indirect effect through investors' sentiment. The research first confirms a pervasive optimism bias, with positive ratings overwhelmingly outnumbering negative ones. In line with financial theory, strong upgrades to "Buy" generate significant and sustained positive reactions in both stock returns (CAR) and investor sentiment (CAS). However, the study's central contribution is the identification of a significant "downgrade puzzle": negative recommendations, including downgrades to "Hold" and even "Sell," frequently fail to produce negative stock returns and are often associated with perplexing price resilience or positive drifts. This price anomaly is further complicated by a frequent divergence between returns and sentiment.

These findings challenge the direct applicability of conventional market efficiency theories to Vietnam's unique environment. The results suggest that the impact of analyst signals is heavily moderated by factors such as the absence of effective short-selling mechanisms, strong contrarian behavior from retail investors, and analysts acting as trend-followers rather than predictors.

# INTRODUCTION

## Research Background and Motivation

In the modern capital markets, financial analysts serve as essential intermediaries, tasked with the critical function of distilling vast and often opaque corporate and economic data into accessible, actionable insights. By issuing detailed reports, price targets, and explicit recommendations, they reduce information asymmetry and, in theory, enhance market efficiency. The influence of these professional opinions on investor behavior and, consequently, on stock valuations has been a cornerstone of financial research for decades. Foundational studies by Stickel (1995) and Womack (1996) provided early, compelling evidence that stock prices exhibit statistically and economically significant reactions to the announcement of recommendation changes. Womack (1996), for instance, documented that analyst upgrades could lead to predictable short-term gains, while downgrades often triggered a more pronounced and prolonged negative price drift, suggesting that sell-side recommendations contained valuable, market-moving information. This line of inquiry was further advanced by Barber et al. (2001), who demonstrated that a strategy of investing in stocks most favored by analysts while shorting the least favored could, before transaction costs, yield significant abnormal returns, thereby questioning the strong form of market efficiency.

However, the role of an analyst is not without its complexities and potential conflicts of interest. Subsequent research has scrutinized the motivations behind recommendation revisions, suggesting they are not always driven by the pure pursuit of new information. Altınkılıç & Hansen (2009) argued that a significant portion of revisions occur in the wake of public corporate news, such as earnings announcements, rather than providing novel insights. This indicates that analysts may sometimes act as interpreters of existing information rather than generators of new intelligence. Furthermore, they posited that career-oriented incentives, such as the desire to improve industry rankings for better compensation and employment prospects, could influence the timing and nature of their recommendations, potentially prioritizing brand marketing over objective investor guidance. The credibility and impact of a recommendation are also heavily moderated by the analyst's reputation and the perceived strength of their signal. Research has consistently shown that recommendations from highly ranked analysts carry more weight and can generate larger, albeit sometimes temporary, price movements (Stickel, 1995; Fang and Yasuda, 2014). Sorescu and Subrahmanyam (2006) added further nuance, finding that minor revisions from reputable analysts often led to a sustained price drift, while bold predictions from less-established analysts could trigger overreactions that subsequently reversed. Expanding on this, Asquith, Mikhail and Au (2005) found that the full content of an analyst's report, particularly new price targets and the justifications provided, can be more influential than the rating change itself.

Beyond these direct price effects, analyst recommendations are deeply interwoven with the broader, more intangible concept of investor sentiment - the collective optimism or pessimism that can drive markets independently of fundamental value. The seminal work of Baker and Wurgler (2006) established investor sentiment as a powerful, systematic risk factor, showing that it could predict cross-sectional returns, particularly for stocks that are difficult to value and prone to speculation. Later studies have explicitly linked analyst activities to these psychological tides. Kim, Ryu, and Seo (2014) and Kim, Ryu, and Yang (2019) demonstrated that analyst upgrades can act as powerful catalysts for investor sentiment, amplifying market swings, especially in optimistic or "hot" market conditions. This suggests that analysts do not merely inform rational investors; they also influence the emotional state of the market, a role that becomes particularly salient in markets with high levels of retail participation.

While these dynamics have been extensively studied in developed markets like the United States or South Korea, their applicability to emerging and frontier markets, such as Vietnam, cannot be taken for granted. Emerging markets present a unique laboratory for financial research, characterized by distinct institutional structures, regulatory environments, and investor behaviors. The Vietnamese stock market, in particular, exhibits several notable characteristics that make it a compelling case study. It is heavily dominated by local individual investors, whose trading decisions are often shaped by demographic factors like age and education, as well as psychological biases such as overconfidence and emotional trading (Morgan and Trinh, 2019; Quang, Linh, Van Nguyen, and Khoa, 2023). Moreover, there is strong empirical evidence of herding behavior, especially during market downturns and periods of economic uncertainty, suggesting that investors often follow the crowd rather than conducting independent analysis (Vo and Phan, 2017, 2019).

Despite these unique features, research on the role and impact of analyst recommendations in Vietnam remains nascent and is often constrained by outdated or limited data. A key study in this area by Van Huy Bui et al. (2021) analyzed the Vietnamese market using data from 2010 to 2015. While finding evidence of a positive analyst bias and significant market reactions to upgrades, their sample was limited to just 1,268 observations. This dataset may no longer accurately reflect the realities of a market that has undergone substantial growth and structural change in the subsequent decade, particularly as it stands on the cusp of being upgraded to emerging-market status.

This study is directly motivated by this conspicuous research gap. The Vietnamese financial landscape has evolved dramatically, and a contemporary, large-scale investigation is required to understand the current influence of analyst recommendations. By leveraging a comprehensive dataset of over 7,000 recommendation changes from 2015 to 2024, this research aims to provide fresh, robust insights into the dual impact of analyst revisions on both stock returns and investor sentiment within this unique and rapidly developing market context. We believe that by doing so, this study will offer a more accurate and nuanced perspective on how expert opinions shape market dynamics in one of Southeast Asia's most promising economies.

## Research Objectives

To address the identified gaps in the literature and provide a comprehensive analysis of the contemporary Vietnamese stock market, this thesis is guided by three primary research objectives. Each objective is designed to build upon the last, moving from a foundational analysis of analyst behavior to a nuanced examination of market reactions.

- **Bias Analysis:** To study the distribution of analyst recommendations in the current Vietnamese stock market to identify any systematic patterns or biases, such as the widely documented "optimism bias," where positive ratings far outnumber negative ones. Understanding this baseline is critical for correctly interpreting the informational content of any subsequent changes.
- **Dual Influence Investigation:** To investigate how changes in analyst recommendations - specifically upgrades and downgrades - influence both stock returns (the price impact) and investor sentiment (the psychological impact). This dual-pronged approach aims to assess whether analyst revisions primarily trigger a rational price adjustment, a psychological mood shift, or a complex combination of both.
- **Comparative Analysis:** To systematically compare and contrast the market's reaction in terms of stock returns (measured by Cumulative Abnormal Returns, CAR) and investor sentiment (measured by Cumulative Abnormal Sentiment, CAS). The goal is to determine whether these responses converge or diverge, thereby uncovering the unique and potentially counterintuitive ways in which the Vietnamese market processes and responds to analyst guidance.

## Research Scope

The scope of this study is carefully defined to ensure a focused and rigorous investigation. The research is centered exclusively on 728 companies listed on the Vietnamese stock exchanges, including the Ho Chi Minh Stock Exchange (HOSE) and the Hanoi Stock Exchange (HNX). The primary period for data collection spans ten years, from the beginning of 2015 to the end of 2024. This extensive timeframe allows for the observation of market behavior across various economic cycles and stages of market development.

We also collected data from 2014 to serve as a crucial baseline year, used to establish a history for each analyst-firm pair. This allows us to accurately identify true recommendation changes and distinguish them from initial coverage ratings or simple reiterations, a methodological refinement that strengthens the validity of an event study, as argued by MacKinlay (1997).

Thematically, the scope is deliberately narrowed to the market impact of recommendation revisions (i.e., upgrades and downgrades). This focus is based on the well-supported premise in financial literature that changes in recommendations are more likely to contain new, material information compared to static or reiterated ratings, which often have minimal market impact. By concentrating on these specific "event days," we can more effectively isolate the market's reaction to the new information being conveyed by the analyst.

## Research Data and Sample

The empirical foundation of this research rests on a large and meticulously compiled dataset gathered from multiple high-quality sources.

**Analyst Recommendations:** The primary data on analyst recommendations for Vietnamese listed companies were sourced from the Bloomberg platform, a recognized provider of comprehensive financial data. The raw data collected covered the period from 2014 to 2024. A critical step in preparing this data was standardization. Because different brokerage houses use their own proprietary rating terminology (e.g., "Accumulate," "Outperform," "Market Perform"), all recommendations were mapped onto a standardized five-point numerical scale, ranging from 1 ("Sell") to 5 ("Buy"). This process is essential for enabling a consistent. After a filtering process - which involved identifying true changes in ratings, ensuring a rating history of at least one year, and excluding a single institution with a non-standard and outlier recommendation methodology - the final sample for the event study was constructed. This final dataset comprises 7,185 distinct recommendation changes that occurred between January 2015 and December 2024. This sample is divided into 3,613 upgrades and 3,572 downgrades, providing a large and balanced foundation for statistical analysis and representing a significant improvement over the smaller samples used in prior research on this market.

**Stock Returns and Sentiment Data:** To measure the impact of these recommendation changes, daily trading data for 728 companies listed on the Vietnamese stock market were collected using FiinPro platform for the same 2014 - 2024 period. This dataset includes crucial variables for each firm-day, such as total trading volumes, the volume of buy and sell orders, adjusted closing prices (corrected for dividends and stock splits), and the number of outstanding shares. This comprehensive trading data serves as the raw material for calculating both the stock return metrics and the proxies required for constructing the investor sentiment index.

## Methodology Framework

The framework combines the construction of a novel sentiment index with a classic event-study approach.

**Part I: Construction of a Firm-Level Investor Sentiment Index**

Recognizing that investor sentiment is a multifaceted construct, this research moves beyond single-proxy measures to develop a comprehensive, composite firm-level sentiment index. This is achieved through a multi-step process:

**Selection of Proxies:** Following established principles in the sentiment literature, five distinct and complementary market-based proxies are calculated for each firm-day. Each proxy is chosen to reflect a different facet of investor behavior or market activity:

- **Buy-Sell Imbalance (BSI):** Calculated from daily buy and sell order volumes, this proxy directly measures net buying pressure.
- **Adjusted Turnover Ratio (ATR):** This measures trading intensity relative to the company's size.
- **Logarithm of Trading Volume (LTV):** A normalized measure of market participation and interest.
- **Relative Strength Index (RSI):** A classic momentum oscillator used to gauge recent price changes.
- **Psychological Line Index (PLI):** This measures the proportion of recent trading days with price increases, reflecting the consistency of upward momentum.

**Index Creation via Principal Component Analysis (PCA):** To synthesize these five correlated proxies into a single, unified measure of sentiment, Principal Component Analysis (PCA) is employed. PCA is a statistical technique that transforms correlated variables into uncorrelated principal components. The first principal component (PC1), which captures the maximum common variance, is extracted to serve as our composite firm-level sentiment index (S<sub>i,t</sub>). This method is well-established in influential sentiment studies (e.g., Baker and Wurgler, 2006; Kim, Ryu, and Yang, 2019) and ensures a representation of the underlying sentiment dimension.

**Isolating Firm-Specific Sentiment:** Since firm-level sentiment can be heavily influenced by broad market movements, a final purification step is taken. The firm-level sentiment index (S<sub>i,t)</sub> is regressed against the excess return of the overall market. The residuals from this regression represent the portion of investor sentiment that is idiosyncratic to the firm and independent to general market sentiment. This refined, firm-specific sentiment measure is what we use in our final analysis to ensure we are capturing reactions to company-specific news rather than market-wide mood swings.

**Part II: Event Study Framework**

A classic event-study methodology is used to systematically measure the market's reaction to recommendation changes. This framework is applied in parallel to both stock returns and our investor sentiment index.

**Measuring Price Impact (Cumulative Abnormal Returns - CAR):** To assess the impact on stock prices, we calculate the Cumulative Abnormal Return (CAR) for each category of recommendation change.

**Measuring Sentiment Impact (Cumulative Abnormal Sentiment - CAS):** In an identical manner, we measure the impact on investor psychology by calculating the Cumulative Abnormal Sentiment (CAS).

**Analyzing the CAR and CAS values across different event windows** (pre-event, event, post-event) for various types of upgrades and downgrades: this framework enables a detailed deconstruction of how analyst recommendations influence market dynamics, from pre-event anticipation to immediate impact and post-event drift.

## Contribution of Research

This thesis is poised to make several significant and original contributions to the academic literature on behavioral finance and emerging markets, as well as to offer practical insights for market participants.

- **Provides a Current and Comprehensive Analysis for Vietnam:** This study will deliver the most up-to-date and extensive analysis of analyst recommendation impact in the Vietnamese stock market to date. By using a large dataset spanning a recent and transformative decade (2015-2024), it overcomes the primary limitation of previous research, which relied on older, smaller samples, thereby providing a more accurate reflection of the market's current state.
- **Introduces a Novel Firm-Level Sentiment Index:** Methodologically, a key contribution is the construction and application of a robust, multi-proxy, firm-level investor sentiment index specifically for the Vietnamese market. This moves beyond market-wide sentiment measures and allows for a more granular analysis of how investor psychology for individual stocks shifts in response to analyst signals.
- **Uncovers and Documents the "Downgrade Puzzle":** A central empirical contribution is the identification of a significant market anomaly we term the "downgrade puzzle." The research demonstrates that negative recommendations (downgrades to "Hold" or "Sell") frequently fail to produce the expected negative stock returns and, in many cases, are associated with surprising price resilience or even positive drifts. These finding challenges conventional market efficiency theories and points to unique behavioral or institutional factors at play in Vietnam.
- **Highlights the Divergence Between Returns and Sentiment:** The study's comparative framework reveals a frequent and economically significant divergence between stock returns (CAR) and investor sentiment (CAS). This finding is critical as it refutes the simplistic assumption that price movements are a direct mirror of collective investor psychology. It suggests that in Vietnam, analyst signals are processed through a more complex filter, where factors like herding, retail investor behavior, and institutional constraints can cause prices and sentiment to follow separate paths.
- **Offers Practical Implications for Investors and Regulators:** The findings have direct practical relevance. For investors, the research serves as a clear warning that traditional trading signals may not apply in Vietnam. For regulators and policymakers, the study sheds light on market inefficiencies and the powerful influence of behavioral biases, highlighting areas that may require attention to enhance market transparency and education.

## Research Structure

The thesis is organized into the following chapters:

- **Chapter 1: Introduction**

This opening chapter, which you are currently reading, sets the stage for the entire study. It establishes the research background by contextualizing the role of financial analysts and investor sentiment in capital markets. It clearly outlines the motivation for the research, highlighting the specific gaps in the literature concerning the Vietnamese market. The chapter then specifies the core research objectives, defines the scope of the investigation, provides an overview of the data and methodology, and concludes by summarizing the key contributions of the thesis.

- **Chapter 2: Literature Review**

This chapter provides a deep and comprehensive review of the existing academic literature relevant to the research questions. It is structured into three main sections. The first section explores the foundational and contemporary research on the impact of analyst recommendations on stock prices and market efficiency. The second section delves into the theory and measurement of investor sentiment, examining its role as a behavioral factor in asset pricing. The final section synthesizes literature specific to the Vietnamese market, focusing on documented investor characteristics like herding behavior, the development of its stock exchanges, and a critical review of prior studies on analyst recommendations and sentiment in Vietnam.

- **Chapter 3: Data and Methodology**

This chapter details the "how" of the research, providing a transparent and replicable account of the empirical framework. It begins by describing the data collection process, including the sources (Bloomberg, FiinPro), the sample selection criteria, and the process of standardizing and cleaning the analyst recommendation data. It then presents the core methodological components: (1) the construction of the five proxies for the firm-level investor sentiment index, including their formulas and theoretical underpinnings; (2) the application of Principal Component Analysis (PCA) to create a unified sentiment index; and (3) the event-study framework used to calculate Cumulative Abnormal Returns (CAR) and Cumulative Abnormal Sentiment (CAS) across various event windows.

- **Chapter 4: Empirical Results and Analysis**

This chapter is the core of the thesis, where the findings of the empirical investigation are presented objectively. It is divided into two main parts. The first part presents the results of the CAR analysis, using tables and figures to illustrate how stock returns react to different categories of analyst upgrades and downgrades. The second part presents the results of the CAS analysis, showing how investor sentiment shifts in response to the same recommendation changes. This chapter focuses on presenting the data and statistical results without extensive interpretation, thereby laying the factual groundwork for the subsequent discussion.

- **Chapter 5: Further Discussion**

In this chapter, the results presented in Chapter 4 are interpreted and contextualized. It moves beyond "what" was found to "what it means." The chapter systematically compares and contrasts the findings for CAR and CAS, explicitly addressing the convergences and, more importantly, the frequent divergences between them. It discusses the implications of key findings, such as the "downgrade puzzle," and relates these anomalies back to the theories and market characteristics discussed in the literature review. This section addresses the study's limitations and offers potential explanations for the observed phenomena, connecting the empirical results to the broader research question.

- **Chapter 6: Conclusion and Suggestions for Future Research**

The final chapter provides a concise summary of the entire research project. It restates the principal findings in relation to the initial research objectives and reiterates the main contributions of the thesis to the field. It synthesizes the key takeaways and their practical implications for investors, analysts, and regulators. Finally, based on the study's findings and limitations, it proposes several concrete and promising directions for future research, such as further investigation into the "downgrade puzzle," analysis of retail versus institutional investor reactions, and the use of alternative sentiment measures.

# LITERATURE REVIEW

## The Informational Role and Impact of Analyst Recommendations

The role of financial analysts as information intermediaries in capital markets has been a subject of intense academic debate for over three decades. The central question revolves around whether their recommendations provide new, value-relevant information to investors or merely echo existing market trends. This section traces the evolution of this discourse, from the initial studies that established their market-moving power to more recent work that explores the nuances and complexities of their influence.

### Foundational Evidence: Do Recommendations Move Markets?

Initial academic inquiries sought to answer a fundamental question: do analyst recommendations influence stock prices? The seminal work in this area provided a resounding affirmative. Stickel (1995) was among the first to systematically document this effect, finding that buying recommendations were associated with average stock price increases of 1.16%, while selling recommendations led to decreases of 1.28% in the days following the announcement. However, Stickel pointed out that these averages could be misleading, as the impact was often entangled with other corporate news like earnings announcements, and that the magnitude of the price change was conditional on the strength of the rating and the size of the firm, with smaller firms reacting more strongly.

Building directly on this, Womack (1996) conducted a landmark study that not only confirmed the immediate price impact but also uncovered a crucial asymmetry in their longevity. He demonstrated that while the positive returns from upgrades were significant and predictable in the short term, the negative price impact from downgrades was often more pronounced and exhibited a longer post-event drift, filtering into the market over several months. This suggested that sell recommendations, being rarer and carrying greater career risk for the analyst, contained more potent and valuable information than buy recommendations.

The question then shifted from whether recommendations had an impact to whether investors could profit from them. Barber, Lehavy, McNichols, and Trueman (2001) addressed this by constructing portfolios based on consensus analyst ratings. Their findings were striking: a strategy of buying the most highly rated stocks and shorting the least-favored ones would have theoretically generated abnormal returns of 75 basis points per month. However, they provided a crucial reality check: once realistic transaction costs were factored in, this profitability largely vanished due to the high portfolio turnover required. This led them to conclude that while markets may not be perfectly efficient in processing analyst information before costs, trading frictions are generally sufficient to prevent investors from easily exploiting these temporary inefficiencies.

### Nuances and Conditioning Factors: Beyond the Headline Rating

As the basic price impact of recommendations became established, research evolved to explore the moderating factors that determine the magnitude and persistence of the market's reaction. It became clear that not all recommendations are created equal.

Sorescu and Subrahmanyam (2006) introduced a framework from behavioral decision theory, measuring recommendation changes along two dimensions: "strength" (the magnitude of the rating change) and "weight" (the reputation of the analyst and their brokerage house). Their findings revealed a complex interplay: high-strength but low-weight revisions (e.g., a large upgrade from an inexperienced analyst) often led to a price overreaction that subsequently reversed, suggesting investors were initially swayed by the bold call but later corrected their assessment. Conversely, low-strength but high-weight revisions (e.g., a small change from a prominent, reputable analyst) were more likely to be followed by a sustained, albeit smaller, price drift in the direction of the call.

The importance of analyst skill and reputation is a recurring theme. Fang and Yasuda (2014) showed that top-tier analysts, such as those nominated for Institutional Investor's "All-American" team, consistently generated superior risk-adjusted returns for their clients, particularly with their buy recommendations, suggesting their expertise provides genuine value. Further complicating the picture, researchers began to look inside the "black box" of the analyst report itself. Asquith, Mikhail, and Au (2005) argued compellingly that the market reacts to the full content of the report, not just the headline rating. They found that revisions to price targets and the textual justifications provided by the analyst were often more powerful drivers of stock returns than the rating change alone, with the impact of each element varying depending on whether it was an upgrade, downgrade, or reiteration.

### The Analyst's Dilemma: Information Provider vs. Trend Follower

A more critical stream of literature began to question the true informational novelty of analyst recommendations. Altınkılıç and Hansen (2009), using high-frequency intraday data, argued that a significant portion of recommendation changes simply follow on the heels of public corporate news, suggesting analysts often act as interpreters of existing information rather than generators of new insights. They contended that career incentives, such as the desire for better compensation and industry rankings, could be a primary driver of revisions, diminishing their value to investors. Ivković and Jegadeesh (2004) added to this by showing that the timing of a recommendation relative to an earnings announcement is crucial, with revisions made well before or after the announcement carrying more informational weight than those issued in its immediate vicinity.

This debate - whether analysts lead the market with new information or simply follow existing trends - remains central to the field. Jegadeesh et al. (2004) tackled this by acknowledging that analysts exhibit a clear preference for growth and high-momentum stocks, yet they found that consensus recommendations still possess strong predictive power for future returns, suggesting they contain valuable information not captured by other known factors. A synthesis of these views was offered by Loh and Stulz (2011), who found that only a small fraction - around 12% - of recommendation changes are truly "bold" enough to generate noticeable changes after accounting for confounding news. They concluded that it is these rare, high-impact, contrarian calls from reputable analysts that genuinely shift investor perceptions and drive market revaluations. This body of work paints a complex picture where analyst recommendations are not a monolithic source of information but a diverse set of signals whose value depends critically on the analyst's reputation, the timing and content of their report, and its novelty relative to existing market trends.

## The Behavioral Dimension: The Theory and Measurement of Investor Sentiment

Parallel to the research on analyst recommendations, the field of behavioral finance has established investor sentiment - the collective optimism or pessimism of market participants - as a powerful force in asset pricing. This section reviews the theoretical foundations of sentiment, the evolution of its empirical measurement, and its direct interplay with the actions of financial analysts.

### Theoretical Foundations and Empirical Measurement

The formal study of investor sentiment gained significant traction when it became clear that psychological biases could systematically affect asset prices, especially in markets with limits to arbitrage. A pioneering theoretical model by Baker and Stein (2004) proposed that market liquidity could serve as a proxy for sentiment. They argued that in markets with short-sale constraints, waves of irrational optimism from speculative traders lead to increased trading volume (liquidity), which can cause stocks to become temporarily overpriced, leading to lower future returns. This model provided a rational explanation for several observed market anomalies.

The empirical breakthrough came with the work of Baker and Wurgler (2006), who moved beyond single proxies to construct a composite sentiment index using multiple market-based indicators (such as IPO first-day returns, trading volume, and the dividend premium). Their study demonstrated that this sentiment index was a powerful predictor of cross-sectional stock returns. Specifically, they found that during periods of high investor sentiment, speculative, hard-to-value stocks tended to earn lower subsequent returns than their more stable counterparts, establishing sentiment as a systematic risk factor. This work spawned a new wave of research focused on creating and refining sentiment indices, with a recent meta-analysis confirming that while more complex sentiment models tend to have higher explanatory power (R-squared), there is insufficient evidence that they offer superior predictive power over more established, robust methods. This underscores the value of using a well-grounded approach like Principal Component Analysis (PCA) on multiple proxies, as employed in this thesis.

### The Interplay Between Analyst Actions and Investor Sentiment

These two streams of literature - analyst recommendations and investor sentiment - are not independent; they are deeply intertwined. A growing body of research has shown that analyst actions can be both a cause and a consequence of shifts in investor mood.

A landmark study by Kim, Ryu, and Yang (2019) explicitly connected these two domains. They found that analyst recommendation changes act as powerful catalysts for investor sentiment, particularly in the Korean market. Their results showed that while sentiment shifted more strongly in response to upgrades, the ultimate effect on stock returns was actually stronger for downgrades that were accompanied by a negative shift in sentiment. This highlights a crucial feedback loop: an analyst's action can influence investor sentiment, and that sentiment, in turn, moderates the final impact on the stock's price. Research from the Korean market, which serves as a useful proxy for a retail-dominated Asian market, has consistently shown that sentiment is a powerful explanatory variable, especially for small-cap, high book-to-market, and heavily retail-owned stocks.

This interplay becomes particularly important in markets like those in Asia, where institutional factors such as restrictions on arbitrage and short-selling are more prevalent. As noted by Choe and Yang (2010), these constraints prevent rational traders from fully correcting mispricings caused by waves of sentiment, making these markets more susceptible to sentiment-driven fluctuations than their developed counterparts.

## The Vietnamese Market Context: A Unique Laboratory

While the global literature provides a robust theoretical framework, its principles must be tested and adapted within the unique institutional and behavioral landscape of Vietnam. This section synthesizes the existing research on the Vietnamese market to establish the specific context for this thesis.

### A Market in Historic Transition

Vietnamese stock market is a relatively young and rapidly evolving entity. Following the "Doi Moi" economic reforms of 1986, the first official trading center was established in Ho Chi Minh City in 2000, followed by the Hanoi Stock Exchange in 2005. In the quarter-century since its inception, the market has grown exponentially to include over 728 listed companies with a capitalization approaching US\$270 billion.

Crucially, this study is being conducted at a pivotal moment in the market's history. Vietnam stands on the verge of a historic upgrade from "frontier" to "emerging market" status, with FTSE Russell widely expected to announce this reclassification in September 2025. This transition is not merely symbolic; it is projected to unlock substantial foreign capital inflows, fundamentally reshaping investment dynamics and elevating the importance of credible financial information and analysis. This impending upgrade provides a powerful and timely motivation for understanding the current role and impact of analyst recommendations.

### The State of Research on Analyst Recommendations and Sentiment in Vietnam

Despite its growing importance, research on analyst recommendations in Vietnam is sparse. A key study by Van Huy Bui et al. (2021) examined the market from 2010-2015 and found evidence of a strong positive bias and significant market reactions to upgrades. However, their work, while foundational, is now dated and was based on a relatively small sample, highlighting the urgent need for a more current and comprehensive analysis. On a broader scale, research on emerging markets has shown that analyst recommendations often generate larger abnormal returns compared to developed G7 countries, suggesting their influence is magnified in less informationally efficient environments.

Research on constructing investor sentiment indices in Vietnam has followed two main paths. One approach has utilized novel data from internet search traffic (Google Trends) and social media (Facebook) to capture investor mood. Another has adapted established methodologies, such as creating composite indices from market proxies via PCA or using technical indicators like the Relative Strength Index (RSI). The existence of these diverse approaches validates the methodology of this thesis while also indicating that there is no single, settled way to measure sentiment in the Vietnamese context.

### The Behavioral Landscape: Herding and Retail Dominance

Perhaps the most defining characteristic of the Vietnamese market is the behavior of its participants. The market is dominated by domestic retail investors (see Table 1), and numerous studies have documented the profound impact of their behavioral biases.

The most consistently identified phenomenon is herding. Multiple studies by Vo and Phan (2017, 2019) have provided robust evidence of herding behavior on both Vietnamese exchanges, particularly during market downturns when investors seek the perceived safety of the crowd. This tendency is amplified by a lack of market transparency and is influenced by movements in global markets. Further research by Bui et al. (2018) confirmed that herding is pervasive across almost all industry sectors, especially during periods of high market volatility.

This collective behavior is rooted in individual psychological traits. Quang et al. (2023) found that overconfidence and emotional trading are prevalent among individual Vietnamese investors, with age and experience only partially mitigating these biases. Complementing this, Morgan and Trinh (2019) showed that financial literacy levels can influence investor behavior, suggesting that a lack of financial sophistication may contribute to more reactive and less rational decision-making.

## Conclusion and Identification of the Research Gap

This review of the literature has established three key points. First, the global research provides a rich theoretical framework for understanding the impact of analyst recommendations, the importance of moderating factors like reputation, and the complexities of their informational role. Second, the field of behavioral finance has firmly established investor sentiment as a critical pricing factor, especially in markets with limits to arbitrage, and has developed robust methods for its measurement. Third, the existing literature on Vietnam paints a clear picture of a unique market: one that is structurally immature, on the verge of a major upgrade, and dominated by retail investors who exhibit strong herding tendencies and other behavioral biases.

The conspicuous research gap emerges at the intersection of these three streams. While the component parts have been studied, there exists no contemporary, large-scale study that comprehensively investigates the dual impact of analyst recommendation changes on both stock returns (CAR) and investor sentiment (CAS) simultaneously within the modern Vietnamese context. Prior research has either focused on price impact alone using dated information or has studied sentiment in isolation. This thesis aims to fill this critical gap by providing the first integrated analysis of how analyst signals are processed by the Vietnamese market, both in terms of price discovery and psychological reaction, during this pivotal period of its development.

Table : VNIndex's trading value by investor types (VNDbn)

|     | **Buy value** |     |     |     |
| --- | --- |     |     |     | --- | --- | --- |
|     | Local individual | Foreign individual | Local institution | Foreign institution |
| 2024 | 1,281,262 | 7,804 | 308,122 | 188,817 |
| 2023 | 3,824,173 | 11,917 | 397,850 | 426,871 |
| 2022 | 3,209,954 | 11,271 | 269,803 | 302,958 |
| 2021 | 3,671,328 | 11,551 | 290,876 | 368,056 |
| 2020 | 4,700,107 | 15,459 | 342,489 | 378,115 |
| 2019 | 1,191,313 | 5,860 | 129,255 | 178,849 |
| 2018 | 628,710 | 4,312 | 132,498 | 147,815 |
| 2017 | 917,224 | 6,764 | 89,629 | 233,735 |
| 2016 | 709,186 | 5,391 | 81,147 | 153,014 |
|     | **Sell value** |     |     |     |
|     | Local individual | Foreign individual | Local institution | Foreign institution |
| 2024 | 1,237,324 | 7,144 | 315,178 | 226,358 |
| 2023 | 3,746,408 | 14,801 | 385,345 | 514,256 |
| 2022 | 3,183,707 | 10,554 | 271,718 | 328,007 |
| 2021 | 3,687,844 | 11,199 | 303,912 | 338,856 |
| 2020 | 4,609,663 | 17,232 | 373,630 | 435,644 |
| 2019 | 1,201,729 | 6,281 | 128,132 | 197,447 |
| 2018 | 670,698 | 4,325 | 119,782 | 147,030 |
| 2017 | 964,351 | 7,117 | 101,423 | 207,029 |
| 2016 | 749,422 | 5,432 | 82,649 | 127,880 |

# DATA SAMPLE AND METHODOLOGY

## Introduction

This chapter details the empirical architecture of the thesis, providing a transparent and replicable account of the data collection process and the analytical framework employed to answer the core research questions. The primary objective is to describe how the final data sample was constructed and how the dual impacts of analyst recommendations on stock returns and investor sentiment were measured. The chapter is structured to follow the logical progression of the research process. First, we describe the acquisition of analyst recommendations and market data, detailing the filtering and standardization procedures used to create a robust final sample. Second, we present a descriptive analysis of this sample, confirming the presence of systematic biases that characterize the informational environment of the Vietnamese market. Finally, we outline the two-pronged methodological framework, explaining the construction of our investor sentiment index and the application of the event-study methodology to calculate both Cumulative Abnormal Returns (CAR) and Cumulative Abnormal Sentiment (CAS). This chapter lays the essential groundwork for the empirical results that will be presented in the subsequent chapter.

## Data Acquisition

The primary data for this study were sourced from globally recognized and reliable providers. Analyst recommendation data for all companies listed on the Vietnamese stock exchanges were gathered from the Bloomberg platform. To measure the market's reaction, corresponding daily trading data - including closing prices, trading volumes, and buy/sell order volumes - were also collected using FiinPro for the same set of firms.

The data collection period spans a full decade, from January 1, 2015, to December 31, 2024. The initial year (2014) was used as a baseline period. This allows for the establishment of a rating history for each analyst-firm pair, which is crucial for accurately identifying genuine recommendation changes as distinct from initial coverage ratings or simple reiterations. The core observation period for the event study therefore runs from January 2015 to December 2024. A summary of these recommendations can be found in Table 2.

## Variables Construction And Descriptive Statistics Analysis

### Analysts' Recommendations Changes

To ensure the integrity and relevance of the final sample, a multi-step filtering protocol was applied.

- **Defining a Recommendation Change:** The central "event" in this study is a change in an analyst's recommendation. A change was strictly defined as any instance where an analyst's rating for a specific stock on a given day differed from their most recent prior rating for that same stock. This focus on revisions is theoretically grounded, as influential research by Loh and Stulz (2011) reveals that new, value-relevant information is more likely to be communicated through changes in recommendations rather than through static or reiterated ratings. This approach allows us to better isolate the market's reaction to novel information.
- **Standardization of Ratings:** A significant challenge in cross-brokerage analysis is the lack of uniform rating terminology. Firms use a wide variety of terms like "Accumulate," "Outperform," or "Market Perform." To create a consistent analytical framework, every recommendation was mapped onto a standardized five-point numerical scale, ranging from 1 ("Sell") to 5 ("Buy"). This practice is common in empirical finance and follows the precedent set by seminal works like Womack (1996), enabling a clear and objective classification of upgrades and downgrades across the entire sample.
- **Final Filtering Criteria:** Two final filters were applied to enhance the quality of the sample. First, only recommendation changes that occurred within one year of a prior rating from the same analyst-firm pair were included. This temporal filter increases the likelihood that the observed revision reflects a considered and current reassessment by the analyst. Second, data from one specific financial institution was excluded because its proprietary rating methodology was a significant outlier from industry norms and was not included in the Bloomberg Consensus ratings. Including this data would have introduced noise and potentially skewed the aggregate results.

After applying this comprehensive protocol, the final dataset for the event study comprises 7,185 distinct recommendation changes, providing a large and robust sample for statistical analysis.

Table : Summary of collected ratings

| **Grade** | **Ratings** | **Ratings by brokerage houses** | **Count** | **%** |
| --- | --- | --- | --- | --- |
| 5   | Buy | Buy, Strong buy, Add, Accumulate… | 14,664 | 48.2% |
| 4   | Overweight | Outperform, Overweight, Overwt/in-line… | 4,303 | 14.1% |
| 3   | Hold | Hold, Market perform, Neutral… | 8,802 | 28.9% |
| 2   | Underweight | Underperform, Underweight… | 625 | 2.1% |
| 1   | Sell | Reduce, Sell, Strong sel… | 1,583 | 5.2% |
| 0   | Unrated |     | 438 | 1.4% |
|     | Total |     | 30,415 | 100.0% |

#### Descriptive Analysis of the Final Sample

Before proceeding to the event study, it is crucial to understand the fundamental characteristics of the data itself. This descriptive analysis reveals systematic patterns in how analysts issue ratings in Vietnam, providing essential context for interpreting the market's reaction.

#### Static Ratings and the Pervasive Optimism Bias

A preliminary analysis of the more than 30,000 individual ratings collected (Table 2) reveals a clear and profound optimism bias. As shown in the data summary table, positive recommendations overwhelmingly dominate the landscape. "Buy" ratings alone account for 48.2% of all recommendations, and when combined with "Overweight" ratings (14.1%), it becomes clear that analysts in our sample assigned favorable ratings to nearly two-thirds (62.3%) of the stocks they covered. In contrast, negative ratings are exceptionally rare, with "Sell" and "Underweight" recommendations together constituting a mere 7.3% of the sample.

This optimistic skew is not unique to Vietnam but is a well-documented global phenomenon, particularly in emerging markets. Moshirian, Ng, and Wu (2009) observe that analysts in emerging markets tend to issue more positive recommendations, potentially due to conflicts of interest, the need to maintain access to company management, or weaker regulatory oversight. Research by Jegadeesh and Kim (2006) confirms this global tendency, and this pattern has been observed even in developed markets like the U.S. (Womack, 1996). In the specific context of Vietnam, a retail-dominated market where investors may rely heavily on analyst guidance, this ingrained optimism can have significant implications for herd behavior and price formation, making it a critical feature of the information environment.

#### The Dynamics of Recommendation Changes

Examining the 7,185 recommendation changes provides further insight into analyst behavior (Table 3). The data reveals a near-perfect balance between positive and negative revisions, with 3,613 upgrades and 3,572 downgrades. However, the nature of these revisions differs significantly.

Upgrades are heavily skewed towards the most positive ratings, with a majority resulting in a final rating of "Buy" or "Overweight." This reinforces the theme of analyst optimism, showing that when analysts do revise their ratings upward, they tend to do so with strong conviction.

The distribution of downgrades, however, tells a story of caution and moderation. The most common outcome of a downgrade is a move to a neutral "Hold" rating, which accounts for approximately 53% of all downgrades. The second most common outcome is a downgrade to "Overweight" (around 30%), a rating that is still fundamentally positive. Overtly pessimistic ratings like "Sell" or "Underweight" are far less frequent outcomes. This pattern strongly suggests that analysts are reluctant to issue severely negative ratings, preferring to temper their pessimism with moderate downgrades. This cautious approach to downgrading aligns with the findings of Jegadeesh and Kim (2006), who noted that analysts often issue warnings more carefully than they issue endorsements, possibly due to concerns about damaging relationships with management or their own reputation. This reluctance to be overtly negative is a key dynamic that will be seen to have a profound impact on the market's reaction.

Table 3: Summary of recommendations changes

| **Summary of upgrades and ratings after changes** |     |     |     |     |     |
| --- |     |     |     |     |     | --- | --- | --- | --- | --- |
| **Year** | **Buy** | **Overweight** | **Hold** | **Underweight** | **Total** |
| **2015** | 142 | 41  | 28  | 6   | **217** |
| **2016** | 162 | 73  | 28  | 14  | **277** |
| **2017** | 149 | 91  | 21  | 7   | **268** |
| **2018** | 147 | 80  | 39  | 7   | **273** |
| **2019** | 236 | 70  | 26  | 2   | **334** |
| **2020** | 321 | 37  | 35  | 3   | **396** |
| **2021** | 390 | 40  | 38  | 4   | **472** |
| **2022** | 336 | 35  | 17  | 0   | **388** |
| **2023** | 396 | 46  | 28  | 3   | **473** |
| **2024** | 428 | 69  | 18  | 0   | **515** |
| **Total** | **2,707** | **582** | **278** | **46** | **3,613** |
| **Summary of downgrades and ratings after changes** |     |     |     |     |     |
| **Year** | **Sell** | **Underweight** | **Hold** | **Overweight** | **Total** |
| **2015** | 35  | 18  | 96  | 59  | **208** |
| **2016** | 28  | 24  | 150 | 46  | **248** |
| **2017** | 33  | 21  | 148 | 77  | **279** |
| **2018** | 29  | 30  | 115 | 89  | **263** |
| **2019** | 22  | 34  | 173 | 133 | **362** |
| **2020** | 41  | 26  | 204 | 116 | **387** |
| **2021** | 64  | 32  | 258 | 135 | **489** |
| **2022** | 39  | 12  | 182 | 145 | **378** |
| **2023** | 53  | 12  | 267 | 118 | **450** |
| **2024** | 48  | 12  | 283 | 165 | **508** |
| **Total** | **392** | **221** | **1,876** | **1,083** | **3,572** |

### Investor Sentiment and Stock Returns

#### Construction of sentiment proxies

Investor sentiment, reflecting the collective attitudes and expectations of market participants, is recognized as a significant driver of market behavior and asset pricing (Baker and Wurgler, 2006; Yang, Ryu, and Ryu, 2017). To investigate its impact in the Vietnamese stock market, a context characterized by substantial retail investor participation similar to markets like Korea (see Kim, Ryu, and Yang, 2019 for a study on Korean sentiment), this study constructs a firm-level investor sentiment index. This approach allows for a granular examination of sentiment dynamics specific to individual securities.

Daily trading data for 728 companies listed on the Vietnamese stock exchange were collected for the period spanning December 2014 to December 2024. For each firm-day, the dataset includes the total volume of buy and sell orders, total trading volume, adjusted closing prices (accounting for dividends and stock splits), and the number of outstanding shares. While direct observation of individual investor trades is often a limitation in empirical finance due to data privacy, the methodology for constructing the sentiment index draws upon established principles. Notably, the use of multiple, market-based proxies to capture the multifaceted nature of investor sentiment is a well-regarded approach (Baker and Wurgler, (2006), Zhu and Niu (2016), Lan (2018), Kim, Ryu, and Yang, (2019)).

Following this principle, a composite firm-level sentiment indicator was developed by aggregating five distinct proxies, each reflecting a different facet of investor behavior or market activity (See Table 4 for formula):

- **Buy-Sell Imbalance (BSI):** Calculated from daily buy and sell order volumes, the BSI aims to capture net buying pressure, which is often interpreted as a reflection of prevailing investor optimism or pessimism towards a specific stock.
- **Adjusted Turnover Ratio (ATR):** This ratio, derived by dividing trading volume by the number of outstanding shares and adjusting for price, measures trading intensity.
- **Logarithm of Trading Volume (LTV):** The logarithm of daily trading volume is included to provide a normalized measure of market participation and interest in a stock.
- **Relative Strength Index (RSI):** A widely-used momentum oscillator, the 14-day RSI gauges the speed and change of price movements, indicating potential overbought or oversold conditions. Its utility in capturing short-term investor reactions and sentiment has been demonstrated in the Vietnamese context by Phuong (2021).
- **Psychological Line Index (PLI):** The PLI assesses the proportion of advancing days over a recent period (e.g., 12 days), reflecting short-term price trends that can mirror collective investor psychology. This measure is intended to complement other momentum indicators like the RSI.

By combining these five complementary proxies, this study aims to construct a comprehensive and robust firm-level investor sentiment index for the Vietnamese market. This index, in conjunction with daily stock market returns, will facilitate an analysis of the interplay between analyst communications, investor psychology, and stock price dynamics.

Table 4: Proxies for the investor sentiment index

| Investors' buy-sell imbalance (BSI) | BSI<sub>i, t</sub> \= |
| --- | --- |
| Adjusted turnover ratio (ATR) | ATR<sub>i, t</sub> \= |
| Logarithm of trading volume (LTV) | LTV<sub>i, t</sub> \= |
| Relative strength index (RSI) | RSI<sub>i, t</sub> \= ,<br><br>where RS<sub>i, t</sub> = |
| Psychological line index (PLI) | PLI<sub>i, t</sub> \= |

_Note: For stock i on day t, BV<sub>i, t</sub> (SV<sub>i, t</sub>) is the total volume of buy (sell) trades by investors, V<sub>i, t</sub> is the trading volume, R<sub>i,t</sub> is the stock return, and P<sub>i,t</sub> is the closing price._

#### Creation of a Unified Sentiment Index using Principal Component Analysis (PCA)

With these five distinctive sentiment proxies - the Buy-Sell Imbalance (BSI), Adjusted Turnover Ratio (ATR), Logarithm of Trading Volume (LTV), Relative Strength Index (RSI) and Psychological Line Index (PLI) - identified, the process became merging them into a single formula. To prevent these individual indicators from giving unclear results (due to their similarities and at times providing correlated signals), it was necessary to create a firm-level index that combined all the available information.

For this reason, the technique of Principal Component Analysis (PCA) was applied. PCA allows a set of correlated variables to be turned into a set of uncorrelated variables which are called principal components. In this situation, the aim is to find the first principal component (PC1) which explains the greatest amount of common change among the original proxies. With this method, multiple indicators are changed into a single index that is easier to use but still includes the main information.

Combining several financial variables into composite indices by using PCA is a well-known and trusted practice in empirical finance. Baker and Wurgler (2006), Lan (2018), Kim, Ryu, and Yang, (2019) carried out influential studies where they used PCA to analyze things like investor sentiment. PCA makes it possible to combine different ways of measuring sentiment into a single index, so the overall mood of the market is easier to see and understand. Conforming to the procedure, PCA was applied to the mentioned sentiment proxies to get the first principal component which became our firm-level sentiment index (S<sub>i,t</sub>). The building of this index is based on a weighted combination of the standardized proxy scores and the weights for each proxy are the factor loadings from PC1.

_S<sub>i,t</sub> \= F<sub>t,BSI</sub> × BSI<sub>i, t</sub> + F<sub>t,ATR</sub> × ATR<sub>i,t</sub> + F<sub>t,LTV</sub> × LTV<sub>i,t</sub> + F<sub>t,RSI</sub> × RSI<sub>i,t</sub> + F<sub>t,PLI</sub> × PLI<sub>i,t</sub>_. (1)

#### Discussing the Results from PCA for the Sentiment Index

The aim of PCA was to pick out the most important factor from the five sentiment proxies which best describes how much they agree. A clear and strong first principal component (PC1) was revealed through the analysis. As you can see from Table 5, PC1 is responsible for nearly half (52.84%) of the variation in all five indicators. This shows that more than half the variation in the various chart indicators can be traced back to this one simple factor which is taken as the main indicator of investor sentiment at a firm level. Afterwards, additional parts represent an increasingly smaller part of the remaining variance, but PC1 is the best representation of the main feeling tone. This reflects the usual procedure in constructing indexes which consists of selecting the first principal component if it represents a significant part of the variance (Jolliffe and Cadima, 2016).

Table 5: PCA explained variance ratio

| **Component** | **Explained Variance Ratio** |
| --- | --- |
| PC1 | 52.84% |
| PC2 | 24.37% |
| PC3 | 13.14% |
| PC4 | 7.53% |
| PC5 | 2.13% |
| **Cumulative (PC1…PC5)** | **100.00%** |

Table 6: PCA descriptive summary

| **Statistic** | **PC1** | **PC2** | **PC3** | **PC4** | **PC5** |
| --- | --- | --- | --- | --- | --- |
| count | 2747 | 2747 | 2747 | 2747 | 2747 |
| mean | 0.0000 | −0.0000 | 0.0000 | 0.0000 | −0.0000 |
| std | 1.6257 | 1.1040 | 0.8107 | 0.6135 | 0.3263 |
| min | −5.3236 | −6.0040 | −3.9911 | −2.5891 | −1.2790 |
| 25% | −1.1303 | −0.4724 | −0.4222 | −0.4048 | −0.2098 |
| 50% | −0.3136 | 0.1216 | 0.0800 | −0.0099 | 0.0036 |
| 75% | 1.0105 | 0.6171 | 0.5131 | 0.3738 | 0.2084 |
| max | 6.2303 | 3.9051 | 4.0950 | 2.8621 | 1.8908 |

Table 7: PCA loadings

|     | **BSI** | **ATR** | **LTV** | **RSI** | **PLI** |
| --- | --- | --- | --- | --- | --- |
| **PC1** | 0.4997 | 0.3091 | 0.4651 | 0.4134 | 0.5172 |
| **PC2** | 0.2894 | 0.6412 | −0.5332 | 0.2602 | −0.3912 |
| **PC3** | −0.1154 | −0.4998 | −0.2224 | 0.8275 | −0.0511 |
| **PC4** | 0.7699 | −0.4578 | 0.078 | −0.1730 | −0.4022 |
| **PC5** | −0.2460 | 0.1842 | 0.6662 | 0.2162 | −0.6442 |

Table 8: Correlation between PC1 and each proxy

| **Proxy** | **Correlation with PC1** |
| --- | --- |
| BSI | 0.8122 |
| ATR | 0.5024 |
| LTV | 0.756 |
| RSI | 0.6718 |
| PLI | 0.8407 |

Further evidence for this interpretation comes from the factor loadings of each proxy on PC1 (see Table 7). They show how each variable contributes to the creation of the first principal component. All of them show positive and important loadings on PC1.

- Buy-Sell Imbalance (BSI): 0.4997
- Adjusted turnover ratio (ATR): 0.3091.
- Logarithm of Trading Volume (LTV): 0.4651
- Relative Strength Index (RSI): 0.4134.
- Psychological Line Index (PLI): 0.5172.

It is very important that all these loadings point in the same positive direction. Simply stated, as our sentiment index (PC1) goes up, conditions such as greater net buying pressure (BSI), more trading activity (ATR), stronger trading intensity (LTV), strong recent stock performance (RSI) and good short-term movement (PLI) tend to show up. The two factors - the Psychological Line Index and Buy-Sell Imbalance - appear to make the greatest difference, which makes sense because they may directly express investor psychology and the way the market is buying and selling. The agreement among proxies pointing to PC1, derived from various market and investor behaviors, indicates that PC1 really captures a general market sentiment.

Additional evidence in favor of the model is revealed by the strong correlation between PC1 and the individual proxies (see Table 8). Strengths revealed by PC1 are its high positive correlations with the PLI (0.8407) and BSI (0.8122) and strong positive correlations with LTV (0.7560) and RSI (0.6718). The ATR, with the lowest volume, also shows a good positive correlation (0.5024). On the basis of the correlations, PC1 blends the details of each proxy and often goes along with signs of positive sentiment.

Researchers have well documented in the literature that using PCA to develop a sentiment index is valid and reliable. As an example, Baker and Wurgler (2006) used PCA to develop a popular sentiment index for the markets, showing that it is valuable for predicting different companies' returns. The authors' procedure was to distill a main sentiment factor by using a similar technique, despite the index's scope being different and using other proxies. Therefore, our firm-level study, inspired by Kim, Ryu and Yang (2019), who studied a market with a big retail investor presence, uses well-established methods.

Because of these findings, the first principal component (PC1) is chosen to represent daily sentiment of investors in the Vietnamese market. PC1 also has a mean of ~0 and a standard deviation of about 1.63, as is common in PCA outputs.

#### Focusing on Mood Within the Company

While the index derived from PCA shows us investor feelings for each company, we realize that each stock is affected by other factors. Sometimes, if the market as a whole moves up or down, it can make a company's own outlook look different from what it truly is. For a better view of what influences each firm's psychology, we must isolate the firm-specific influence from the feelings in the market. This approach is also conducted by Kim, Ryu, and Yang, (2019).

The scores we get from PCA for every firm are then used in a new way: we regress them against the excess returns of the market. Calculating a "risk-free rate" in Vietnam should be done with practical methods. While government bonds within reach of all investors are scarce, we have come up with the risk-free rate by using the bottom end of interest rates offered by banks for different periods of up to six months (collected using FiinPro). So, it can be used as a reasonable estimate for what investors might earn with little risk.

After performing the regression (sentiment index as dependent, market excess return as independent), our main attention is on the residuals. These residuals, as outlined in equation (2) and in the work of Kim, Ryu, and Yang, (2019), contain the part of a firm's sentiment that is not influenced by general market movements. They mainly show the company-specific variations in how investors feel about that firm. It singles out the true feelings of the company, not influenced by wider market changes. We think the individualized character of investor attitudes is what will add robustness to our analysis when we look at analyst recommendation changes.

| S<sub>i, t</sub> = | (2) |
| --- | --- |
|     |     |

Table 9: Investor sentiment descriptive summary

|     | **Upgrade to Buy** |     |     |     |     |     |
| --- | --- |     |     |     |     |     | --- | --- | --- | --- | --- |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0274 | 0.0010 | 13.9724 | 2.9975 | \-3.9466 | 1.5976 |     |
| std | 0.1542 | 0.0098 | 1.8807 | 17.5669 | 14.9584 | 13.2156 |     |
| min | \-0.8444 | \-0.0753 | 4.0943 | \-50.0000 | \-50.0000 | \-41.2720 |     |
| 25% | \-0.1145 | \-0.0017 | 12.9105 | \-9.3064 | \-16.6667 | \-7.8240 |     |
| 50% | \-0.0317 | 0.0000 | 14.1542 | 3.3402 | 0.0000 | 1.5730 |     |
| 75% | 0.0557 | 0.0027 | 15.3147 | 15.9089 | 8.3333 | 10.9974 |     |
| max | 0.8025 | 0.1302 | 18.3826 | 47.7274 | 41.6667 | 41.4037 |     |
|     | **Upgrade to Overweight** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0371 | 0.0007 | 13.6091 | 3.9699 | \-5.0687 | 2.0903 |     |
| std | 0.1578 | 0.0097 | 1.8339 | 18.4902 | 16.4380 | 13.8860 |     |
| min | \-0.7633 | \-0.0758 | 6.5367 | \-50.0000 | \-50.0000 | \-40.5405 |     |
| 25% | \-0.1219 | \-0.0011 | 12.7312 | \-9.2332 | \-16.6667 | \-7.3437 |     |
| 50% | \-0.0290 | 0.0000 | 13.8643 | 4.5454 | \-8.3333 | 2.4308 |     |
| 75% | 0.0442 | 0.0019 | 14.7634 | 17.7746 | 8.3333 | 12.1581 |     |
| max | 0.9995 | 0.0718 | 17.5302 | 48.6395 | 41.6667 | 40.0652 |     |
|     | **Upgrade to Hold** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0378 | 0.0013 | 13.4413 | 0.4693 | \-6.8345 | 0.2373 |     |
| std | 0.1690 | 0.0092 | 1.9515 | 19.1051 | 15.3594 | 14.1343 |     |
| min | \-0.9514 | \-0.0436 | 3.6889 | \-50.0000 | \-50.0000 | \-45.1794 |     |
| 25% | \-0.1312 | \-0.0007 | 12.4871 | \-12.8866 | \-16.6667 | \-9.8030 |     |
| 50% | \-0.0253 | 0.0000 | 13.7146 | 0.3649 | \-8.3333 | 0.1527 |     |
| 75% | 0.0642 | 0.0009 | 14.6577 | 16.1969 | 0.0000 | 9.8186 |     |
| max | 0.5178 | 0.0483 | 17.4670 | 48.6395 | 33.3333 | 37.0413 |     |
|     | **Upgrade to Underweight** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.1072 | 0.0035 | 13.2337 | \-3.4856 | \-10.3261 | \-3.7898 |     |
| std | 0.1987 | 0.0127 | 1.8819 | 19.7201 | 18.3573 | 16.3550 |     |
| min | \-0.8004 | \-0.0217 | 9.4230 | \-40.2439 | \-41.6667 | \-36.1492 |     |
| 25% | \-0.2187 | \-0.0011 | 11.7975 | \-19.3347 | \-22.9167 | \-14.8473 |     |
| 50% | \-0.0755 | \-0.0001 | 12.7619 | \-0.9259 | \-16.6667 | \-3.1020 |     |
| 75% | 0.0510 | 0.0010 | 14.6525 | 7.3996 | 0.0000 | 4.9475 |     |
| max | 0.1722 | 0.0487 | 18.1930 | 34.1584 | 33.3333 | 31.5202 |     |

|     | **Downgrade to Sell** |     |     |     |     |     |
| --- | --- |     |     |     |     |     | --- | --- | --- | --- | --- |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0394 | 0.0013 | 13.7852 | 4.5994 | \-3.2738 | 3.4912 |     |
| std | 0.1557 | 0.0131 | 1.8961 | 18.2655 | 15.6187 | 13.8712 |     |
| min | \-0.6191 | \-0.0780 | 7.7187 | \-43.7143 | \-50.0000 | \-43.4628 |     |
| 25% | \-0.1194 | \-0.0018 | 12.6127 | \-8.1638 | \-16.6667 | \-6.5814 |     |
| 50% | \-0.0354 | 0.0000 | 13.8963 | 4.9972 | 0.0000 | 4.5253 |     |
| 75% | 0.0488 | 0.0024 | 15.0194 | 18.1646 | 8.3333 | 13.3972 |     |
| max | 0.5155 | 0.0817 | 18.5206 | 46.3636 | 33.3333 | 38.6997 |     |
|     | **Downgrade to Underweight** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0590 | \-0.0009 | 13.7369 | 1.6459 | \-5.8446 | 0.0554 |     |
| std | 0.1562 | 0.0091 | 1.9620 | 19.9543 | 16.4214 | 15.0911 |     |
| min | \-0.9933 | \-0.0558 | 2.3026 | \-42.8572 | \-41.6667 | \-34.5600 |     |
| 25% | \-0.1182 | \-0.0022 | 12.8545 | \-13.8368 | \-16.6667 | \-10.2861 |     |
| 50% | \-0.0474 | \-0.0001 | 13.8672 | 1.7046 | \-8.3333 | \-1.1255 |     |
| 75% | 0.0331 | 0.0012 | 14.9277 | 15.1445 | 8.3333 | 8.5686 |     |
| max | 0.2813 | 0.0403 | 17.2168 | 48.0583 | 41.6667 | 41.6700 |     |
|     | **Downgrade to Hold** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0384 | 0.0006 | 13.8941 | 3.5013 | \-3.8646 | 1.6926 |     |
| std | 0.1447 | 0.0102 | 1.8168 | 17.4169 | 15.0389 | 13.4538 |     |
| min | \-0.9924 | \-0.0805 | 2.3026 | \-50.0000 | \-50.0000 | \-42.6041 |     |
| 25% | \-0.1217 | \-0.0020 | 12.8585 | \-8.7302 | \-16.6667 | \-7.3398 |     |
| 50% | \-0.0374 | 0.0000 | 14.0057 | 3.7937 | 0.0000 | 1.8180 |     |
| 75% | 0.0440 | 0.0022 | 15.1624 | 16.6667 | 8.3333 | 11.2525 |     |
| max | 0.5655 | 0.1110 | 18.4558 | 49.3242 | 41.6667 | 40.5707 |     |
|     | **Downgrade to Overweight** |     |     |     |     |     |
|     | BSI | ATR | LTV | RSI | PLI | Sent |     |
| mean | \-0.0321 | 0.0006 | 14.0351 | 3.2131 | \-3.5472 | 1.5051 |     |
| std | 0.1507 | 0.0072 | 1.8641 | 17.4220 | 13.9654 | 12.6297 |     |
| min | \-0.8809 | \-0.0581 | 2.3026 | \-46.6102 | \-50.0000 | \-32.1909 |     |
| 25% | \-0.1200 | \-0.0016 | 12.8762 | \-9.4595 | \-16.6667 | \-7.4979 |     |
| 50% | \-0.0339 | 0.0000 | 14.2693 | 4.1176 | 0.0000 | 1.7189 |     |
| 75% | 0.0571 | 0.0027 | 15.4043 | 15.8460 | 8.3333 | 10.4548 |     |
| max | 0.5596 | 0.0602 | 18.2883 | 45.8763 | 41.6667 | 37.5912 |     |

#### Investment Setting: The Current View of Investors When Advice is Changed

Before analyzing stock market changes, it helps to first understand the attitudes of investors towards each firm when the analyst recommendations are changed. Analyzing descriptive statistics for upgrades and downgrades gives us initial views of the thoughts driving these opinions at the time they were updated. Table 9 gives these summary details, expressing the mood around each kind of recommendation update.

Looking carefully at these numbers, we discover some distinct and unusual ways these businesses operate. The mood of investors changes a lot depending on the nature and the direction of the analysts' recommendation.

When analysts present their new rating opinions, the index that measures market sentiment (Sent) generally has a surprising and difficult-to-interpret pattern. Even though upgrades are expected to receive positive sentiment and downgrades to get the negative, the facts are not as simple. Most types of revisions tend to include a small negative average for the Investors' Buy-Sell Imbalance (BSI) and the Psychological Line Index (PLI). This implies that usually, at the time of the revision, there is less purchase pressure and these days coincide with recent price lows or flatness, no matter what the revision is about.

"Downgrade to Sell" events are especially fascinating because of its paradox. Unexpectedly, these revisions contain the most average positive feedback (mean Sent = 3.49) among every other category. If stocks go up on the same day a negative call is made and the RSI is positive (mean: 4.60), there is a strong chance that the market has become overly negative and that a rally is hoped for, leading to a short-covering or a relief rally. Upgrades with strong recommendations, for example "Upgrade to Overweight" and "Upgrade to Buy", tend to meet expectations by displaying positive attitudes mainly due to the rise in the momentum rate (RSI), overcoming the weakness in the BSI and PLI scores. Such as, dropping from a favorable rating to a more neutral or still optimistic one such as "Downgrade to Hold" (mean Sent = 1.69) or "Downgrade to Overweight" (mean Sent = 1.51), generally provide a positive response the same day. Changes in stories resulting in pronouncements that are more vague or neutral or even negative, contribute to lower or more subdued sentiment. As an illustration, shifting from Sell/Underweight to Hold only affects investor mindset a little bit (mean Sent = 0.24), but a move from higher levels to Underweight shows about the same level of investor sentiment (mean Sent = 0.06). Events labeled "Upgrade to Underweight" are the most negative (Sent mean -3.80), as the target rating itself seems bearish and both BSI and PLI are at their most negative. This may suggest that ratings' impact on sentiment can be stronger than the simple message of an upgrade or downgrade.

In different types of revisions, the Relative Strength Index (RSI) tends to line up with the overall composite mood, showing that price momentum is a key part of the day's sentiment. The trading volume which is represented by LTV, does not vary much, indicating regular trading during revisions. In essence, the immediate market sentiment on the day of an analyst revision is a multifaceted reaction, where direct buying pressure might be tepid, but broader momentum and the perceived finality or severity of the target rating play crucial roles in shaping the overall sentiment. The "Downgrade to Sell" anomaly underscores the market's capacity for contrarian responses when expectations have been thoroughly managed or exceeded.

#### Price reactions measurement: Cumulative abnormal returns (CAR)

Our first step is to measure a variable for price impact. For each company _i_ that experiences a recommendation change, and for each day _t_ around that event, we construct CAR as follows:

- **Aligning the events:** We first started the process by aligning the events - when the analysts update their ratings - with the trading date of the traget companies. We set the interval from 25 days before the revision to 25 dasy after it. We then anchored the revision date at T0 to set the benchmark.
- **Calculating cumulative returns:** We start by calculating the cumulative raw return for both the individual stock and the overall market over the studied window.

CR<sub>i</sub> (t = (3)

CR<sub>mkt</sub> = (4)

_where is the stock's return at time t, and ​ is the market return on that same day. are in the time interval of (-25; 25)._

- **Determining Cumulative Abnormal Returns (CaR):** We then subtracted the cumulative market return from the stock's cumulative return:

CaR<sub>i,t</sub> = (5)

- **Averaging Across Events (CAR):** Finally, to see the typical impact for a _category_ of recommendation change (e.g., all "Upgrades to Buy"), we average these individual CaRs across all _n_ firms that experienced the same type of event:

CAR<sub>i,t</sub> = (6)

#### Cumulative Abnormal Sentiment (CAS)

- **Defining "Sentiment Surprise" (Abnormal Sentiment - AS):** Just as we looked for abnormal returns, we need a measure of "abnormal sentiment" or "sentiment surprise". This involves comparing the firm's actual idiosyncratic sentiment (AS<sub>i,t</sub>) around the event to what we might have expected. Let's define the daily abnormal sentiment (AS<sub>i,t</sub>) for firm _i_ on day _t_ as:

AS<sub>i,t</sub> = (7)

- **Averaging Across Events (Average Abnormal Sentiment - AAS):** Similar to returns, we average these firm-level sentiment surprises across all _n_ companies undergoing the same type of recommendation change to get the Average Abnormal Sentiment (AAS) for each day _t_ in the event window:

_AAS<sub>i,t</sub>_ = (8)

- **Accumulating the Sentiment Impact (Cumulative Abnormal Sentiment - CAS):** To capture the total sentiment shift over a period \[t₁, t₂\], we sum these daily AAS values:

CAS = (9)

#### Interpreting the Signals

In practice, we centered our event window on the announcement day (which we call day 0). We then examined different sub-periods:

- **Pre-event drift:** (from day -25 to -6, and -5 to -2) to see if there is any information leakage or anticipation or front-running.
- **Immediate reaction:** (day -1 to +1) to capture the swift market response.
- **Post-event adjustments:** (day +2 to +5, and further out to +6 to +25) to observe any continued momentum or reversals.

By comparing the size and statistical significance of these CAR and CAS measures across our different upgrade and downgrade categories, we aim to trace both the speed and the staying power of the market's responses and investors' sentiment to analysts' revised opinions. This detailed examination should provide valuable insights into the influence of sell-side analysts in Vietnamese stock market.

# EMPIRICAL RESULTS AND ANALYSIS

## Introduction to Empirical Findings

This chapter constitutes the empirical core of the thesis, presenting the detailed results of the event-study analysis designed to measure the market's dual reaction to analyst recommendation revisions in Vietnam. Following the structured methodology outlined in the preceding chapter, we systematically dissect the impact of these revisions on two distinct but related dimensions: stock price movements, as captured by Cumulative Abnormal Returns (CAR), and shifts in investor psychology, as measured by our composite Cumulative Abnormal Sentiment (CAS) index.

The structure of this chapter is designed to build a clear and logical narrative from the ground up, in accordance with established standards for presenting empirical research. We begin by examining the price impact of recommendation changes, first analyzing the market's response to various categories of upgrades and then turning to the more complex and counterintuitive reactions to downgrades. This section (4.2) will address the fundamental question of whether analyst revisions contain value-relevant information that moves stock prices in predictable ways.

Subsequently, we pivot our analysis to the psychological dimension in Section 4.3. Here, we apply the identical event-study framework to our novel CAS index to investigate how investor sentiment evolves before, during, and after the same set of recommendation changes. This parallel analysis will reveal whether investor mood aligns with or deviates from the expected response to positive and negative analyst signals.

## The Price Impact of Analyst Recommendations: An Analysis of Cumulative Abnormal Returns (CAR)

This section delves into the first core empirical question of the thesis: How do stock prices in the Vietnamese market react to changes in analyst recommendations? Utilizing the classic event-study methodology, we examine the CAR around eight distinct categories of recommendation revisions - four types of upgrades and four types of downgrades. The goal is to determine the extent to which these revisions convey new, price-moving information to the market and whether these reactions conform to or deviate from the patterns documented in established financial literature.

Table : Summary of upgrades' impact on CAR

| **Estimates** | **Upgrade to Buy** | **Upgrade to Overweight** | **Upgrade to Hold** | **Upgrade to Underweight** |
| --- | --- | --- | --- | --- |
| (-25, -6) | 0.99%\*\*\* | 1.09%\*\*\* | 0.28% | \-0.64% |
| (6.01) | (2.69) | (0.47) | (-0.54) |
| (-5, -2) | 0.22%\*\*\* | 0.37%\*\* | 0.05% | 1.10% |
| (2.94) | (2.40) | (0.16) | (1.46) |
| (-1, 1) | 0.25%\*\*\* | 0.40%\*\*\* | \-0.13% | 0.25% |
| (5.03) | (3.48) | (-0.79) | (0.67) |
| (2, 5) | 0.41%\*\*\* | 0.27% | 0.09% | 0.65% |
| (5.49) | (1.63) | (0.31) | (0.87) |
| (6, 25) | 0.85%\*\*\* | 0.42% | 1.58%\*\* | 1.28% |
| (5.45) | (1.24) | (2.15) | (1.06) |
| **n** | **2,707** | **582** | **278** | **46** |

### The Market Reaction to Analyst Upgrades

(Table 10 and Figure 1)

We begin by analyzing the market's response to positive recommendation revisions, or upgrades. These events are theoretically expected to signal favorable new information about a firm's prospects, leading to positive abnormal returns. The analysis below breaks down the reaction based on the final rating assigned after the upgrade.

**Upgrades to "Buy" and "Overweight": The Market's Affirmation of Positive News**

The most potent and unambiguous signals - upgrades to "Buy" and "Overweight" - elicit a market reaction that largely aligns with theoretical expectations, demonstrating a clear and sustained positive price impact.

As illustrated in the provided data table and visualized in Figure 1, a significant pre-announcement run-up is evident for both categories. For stocks upgraded to "Buy," the CAR in the long pre-event window (-25, -6) is a highly significant 0.99% (t=6.01). Similarly, stocks upgraded to "Overweight" exhibit a 1.09% positive CAR (t=2.69) in the same period. This upward trend accelerates in the immediate week before the announcement (-5, -2 window), with "Buy" upgrades gaining an additional 0.22% (t=2.94) and "Overweight" upgrades gaining 0.37% (t=2.40). This consistent and statistically significant positive drift leading up to the formal announcement suggests several potential dynamics are at play:

- **Analysts as Trend Confirmers:** This pattern strongly supports the view advanced by scholars like Altınkılıç and Hansen (2009), suggesting that analysts often issue upgrades for stocks that are already exhibiting strong positive momentum. In this interpretation, the upgrade does not provide entirely new information but rather confirms and legitimizes an existing positive trend, acting as a ratification of what the market is already beginning to recognize.
- **Information Leakage and Anticipatory Trading:** The pre-event run-up could also be indicative of information leakage, where news of an impending upgrade seeps into the market before the official announcement. This could fuel rumor-based trading and the "follow-the-crowd" or herding behavior that has been well-documented in the Vietnamese market by researchers such as Vo and Phan (2017).
- **Fundamental Improvement Recognition:** A third possibility is that both analysts and market participants are independently recognizing underlying fundamental improvements in a company. The pre-event price rise reflects the gradual incorporation of this positive information by the market, with the analyst's formal upgrade serving as a key crystallization point in this process.

During the critical event window itself (-1, +1), the market's positive reaction solidifies. An upgrade to "Buy" generates a CAR of 0.25% (t=5.03), while an upgrade to "Overweight" produces an even stronger 0.40% (t=3.48). Both results are highly significant, confirming a strong coincident relationship between the announcement and immediate positive price pressure. This aligns with findings from markets like Korea, where Kim, Ryu, and Yang (2019) observed that investors react strongly to positive recommendation changes.

Perhaps most tellingly, a significant post-recommendation drift is observable, particularly for the highest-conviction "Buy" upgrades. This phenomenon, first extensively documented by Womack (1996), suggests that the market does not fully and instantaneously impound the information contained in the recommendation. For "Upgrade to Buy," the positive CAR persists and grows, reaching 0.41% (t=5.49) in the short post-event window (2, 5) and a substantial 0.85% (t=5.45) in the longer (6, 25) window. This sustained upward drift challenges the semi-strong form of the Efficient Market Hypothesis, indicating that investors may either underreact to the initial news or that the recommendation triggers sustained buying pressure from retail and institutional investors who act on the information over a period of days or weeks.

For upgrades to "Overweight," this post-announcement drift is far less pronounced and statistically insignificant, with a CAR of 0.27% (t=1.63) in the (2, 5) window and 0.42% (t=1.24) in the (6, 25) window. This suggests that while the market reacts positively to the initial announcement, the impact is less enduring compared to a full "Buy" upgrade. Investors may perceive an "Overweight" rating as carrying less conviction, leading to a more rapid price adjustment with limited follow-through.

**Upgrades to "Hold" and "Underweight": Muted Reactions and Delayed Signals**

In contrast to the enthusiastic reception of "Buy" and "Overweight" upgrades, revisions that merely temper prior pessimism trigger a much more muted and complex market response.

For stocks upgraded to "Hold" (typically from a more negative "Sell" or "Underweight" rating), there is no statistically significant price movement in either the pre-event windows or the immediate event window (-1, +1), which records a negligible CAR of -0.13% (t=-0.79). This lack of immediate reaction supports the argument by Stickel (1995) that market impact is highly dependent on the perceived strength and conviction of the analyst's signal. An upgrade to "Hold" is an inherently weak signal, signifying a reduction in negativity rather than an endorsement of positive prospects, and the market appears to treat it with commensurate indifference.

However, a fascinating delayed reaction emerges. After an initial lull in the (2, 5) window, the "Upgrade to Hold" category delivers a significant positive CAR of 1.58% (t=2.15) in the longer (6, 25) post-event window. This delayed positive drift suggests a more complex interpretation by the market. An upgrade to "Hold" may not be an immediate catalyst, but it could signal a "bottoming out" of the stock's performance or the removal of significant negative sentiment. This may lead to a slow, gradual price recovery as investors who had been deterred by prior negativity cautiously re-evaluate the stock's prospects over time. It suggests that while the initial news is not exciting, its implication - that the worst may be over - is slowly priced in over the subsequent month.

For the rare "Upgrade to Underweight" category, the results are statistically noisy and inconclusive, primarily due to the very small sample size of only 46 observations. The observed CARs across all windows are not statistically significant. This limited data makes it impossible to draw any reliable conclusions about the market's reaction to this specific type of revision, highlighting the need for a larger dataset to robustly analyze such infrequent events.

Table : Summary of downgrades' impact on CAR

| **Estimates** | **Downgrade to Overweight** | **Downgrade to Hold** | **Downgrade to Underweight** | **Downgrade to Sell** |
| --- | --- | --- | --- | --- |
| **(-25, -6)** | 0.98%\*\*\* | 1.44%\*\*\* | 0.86% | 2.05%\*\*\* |
| (4.31) | (6.80) | (1.21) | (4.13) |
| **(-5, -2)** | 0.25%\*\* | 0.27%\*\*\* | 0.33% | 0.77%\*\*\* |
| (2.21) | (2.98) | (0.95) | (3.34) |
| **(-1, 1)** | 0.24%\*\*\* | 0.15%\*\* | \-0.13% | 0.32%\*\* |
| (2.93) | (2.36) | \-(0.59) | (2.13) |
| **(2, 5)** | 0.08% | \-0.04% | \-0.19% | 0.13% |
| (0.79) | \-(0.49) | \-(0.63) | (0.61) |
| **(6, 25)** | 0.62%\*\*\* | 0.36%\* | \-0.42% | 0.80%\* |
| (2.85) | (1.94) | \-(0.76) | (1.75) |
| **n** | **1,083** | **1,876** | **221** | **392** |

### The Market Reaction to Analyst Downgrades: The "Downgrade Puzzle"

(Table 11 and Figure 1)

The analysis of downgrades yields the most striking and theoretically challenging results of this study. The findings paint a picture that is fundamentally at odds with the textbook view that lower ratings should trigger sharp, negative price reactions. In nearly every downgrade category, we observe positive cumulative abnormal returns before, during, and in many cases, after the negative announcement. This phenomenon, which we term the "downgrade puzzle," is the central anomaly uncovered in our price analysis.

**Downgrades to "Overweight": A Paradoxically Positive Signal**

A downgrade from "Buy" to "Overweight" is the mildest form of negative revision. Given that "Overweight" is still a favorable rating, the market's persistently positive response may not be entirely surprising, but its strength is notable. Prices exhibit a strong positive run-up well before the announcement, climbing 0.98% (t=4.31) in the (-25, -6) window. This rally continues right up to the event, with an additional 0.25% (t=2.21) gain in the (-5, -2) window. Remarkably, even during the event window (-1, +1), the stock gains another 0.24% (t=2.93). The positive momentum is so strong that it persists into the longer post-event window (6, 25), adding a further 0.62% (t=2.85).

This unabated positive trajectory strongly suggests that analysts are issuing this type of downgrade primarily as a valuation call after a prolonged and significant rally has brought the stock price close to what they perceive as its fair value. Investors appear to interpret this signal not as a warning of fundamental trouble, but rather as a confirmation of the stock's strength, coupled with advice that further upside may be limited. The downgrade tempers enthusiasm but fails to extinguish the underlying bullish momentum.

**Downgrades to "Hold," "Underweight," and "Sell": The Core of the Anomaly**

The core of the puzzle lies in the market's reaction to more severe downgrades. A "Hold" rating normally signals neutrality, yet stocks downgraded to this category are, on average, enjoying a powerful rally before the announcement: CAR is 1.44% (t=6.80) in the (-25, -6) window and 0.27% (t=2.98) in the (-5, -2) window. Astonishingly, even the event window itself registers a statistically significant positive return of 0.15% (t=2.36). While there is no clear drift in the immediate (2, 5) post-event period, the positive trend re-emerges in the longer (6, 25) window with a gain of 0.36% (t=1.94).

The pattern for downgrades to "Underweight" is less clear due to a smaller sample size (n=221) and wider error bands, resulting in statistically insignificant CARs around the event. However, the absence of a significant negative reaction is, in itself, a noteworthy deviation from theoretical expectations.

The most profound puzzle emerges from downgrades to "Sell" - the strongest possible negative signal an analyst can issue. Defying all conventional wisdom, these stocks exhibit a powerful pre-event rally, gaining 2.05% (t=4.13) in the long pre-event window and another 0.77% (t=3.34) in the immediate pre-event week. During the event window (-1, +1), when a sharp price drop would be expected, these stocks instead post a significant positive CAR of 0.32% (t=2.13). The positive drift continues even into the long post-event period (6, 25), with an additional gain of 0.80% (t=1.75).

This consistent pattern of positive returns surrounding the most negative analyst ratings demands a robust explanation. We propose three primaries, potentially overlapping hypotheses:

- **Bad News is Fully Priced In:** Analysts may be issuing severe downgrades only after a stock has already suffered significant price declines in the more distant past (beyond our -25 day window) or after negative fundamental news is widely known. By the time the formal downgrade is announced, the worst of the selling pressure may be over. The public announcement could then act as a contrarian signal, sparking relief buying from investors who believe the stock is now "oversold" or that the downgrade marks a capitulation point.
- **Contrarian Trading and Limits to Arbitrage:** The institutional structure of the Vietnamese market is critical here. The absence of a viable short-selling mechanism for most investors means there is no straightforward way to profit from negative opinions. This creates a significant asymmetry. While bearish investors can sell their existing shares, they cannot create new selling pressure. This vacuum may be filled by contrarian retail investors who, seeing a "Sell" rating, decide to buy on the belief that the stock is now a bargain or that the "expert" is wrong. This contrarian buying pressure, unopposed by short-sellers, could be sufficient to overwhelm the selling from existing shareholders and push the price higher.
- **Analyst Disagreement and Credibility:** Investors may simply disagree with the analyst's pessimistic assessment. If a sufficient number of traders remain bullish on the stock's prospects, their continued buying can easily offset the selling pressure initiated by the downgrade, especially if the downgrading analyst is not perceived as highly credible.

### Synthesis of CAR Findings and Potential Explanations

In summary, the analysis of Cumulative Abnormal Returns reveals a market with a highly asymmetric response to analyst recommendations. Vietnamese market appears to process unambiguously positive news ("Upgrade to Buy") in a manner that is broadly consistent with financial theory, exhibiting a strong and persistent positive price reaction. However, its handling of all forms of negative news is deeply anomalous. The "downgrade puzzle" - the phenomenon of resilient or even positive price movements following downgrades - is a robust and pervasive finding across our dataset.

This suggests that the informational content of a downgrade is either discounted, misinterpreted, or overwhelmed by other market forces. The consistent positive pre-announcement CARs across nearly all downgrade categories strongly indicate that analysts in Vietnam often act as momentum-checkers, issuing downgrades in reaction to past positive performance rather than as predictors of future underperformance. The muted or positive event-window reactions, especially for severe downgrades, point towards the powerful influence of constraints (limits to shorting) and the potential for strong contrarian behavior from a retail-dominated investor base. These findings challenge the notion of a universally efficient market and highlight the critical importance of understanding local market structure and investor psychology.

## The Psychological Impact of Analyst Recommendations: An Analysis of Cumulative Abnormal Sentiment (CAS)

Having established the often-anomalous price impact of analyst recommendations, we now turn to the second core empirical question: How do these same revisions influence investor psychology? This section analyzes the Cumulative Abnormal Sentiment (CAS) surrounding the eight recommendation categories. CAS measures the deviation of our composite sentiment index from its expected value, with positive values indicating unusually optimistic sentiment and negative values indicating unusual pessimism. This analysis will reveal whether the psychological mood of the market aligns with the price movements documented in the previous section.

Table : Summary of upgrades' impact on CAS

| **Estimates** | **Upgrade to Buy** | **Upgrade to Overweight** | **Upgrade to Hold** | **Upgrade to Underweight** |
| --- | --- | --- | --- | --- |
| (-25, -6) | 1.65 | \-14.14 | \-15.60 | \-34.56 |
| (0.44) | (-1.61) | (-1.34) | (-1.03) |
| (-5, -2) | 2.37\*\* | \-0.64 | \-7.9\*\* | \-22.18\*\* |
| (2.39) | (-0.29) | (-2.44) | (-2.30) |
| (-1, 1) | 1.27\*\*\* | 0.88 | \-2.00 | \-9.65\*\* |
| (2.61) | (0.80) | (-1.26) | (-1.98) |
| (2, 5) | 1.49 | 0.63 | \-3.58 | \-18.11\* |
| (1.47) | (0.27) | (-1.08) | (-1.68) |
| (6, 25) | 13.84\*\*\* | \-3.53 | \-9.71 | 2.32 |
| (3.71) | (-0.42) | (-0.73) | (0.08) |
| **n** | **2,707** | **582** | **278** | **46** |

### The Sentiment Reaction to Analyst Upgrades

(Table 12 & Figure 2)

The sentiment response to upgrades reveals a fascinating and complex picture, where only the strongest positive signals are capable of generating a clear and sustained improvement in investor mood.

**"Upgrade to Buy": The Sole Catalyst for Positive Sentiment**

The "Upgrade to Buy" category stands alone as the only type of recommendation revision that consistently generates a significantly positive sentiment response. The data shows that investor optimism begins to build even before the formal announcement, with a statistically significant CAS of 2.37 (t=2.39) in the immediate pre-event window (-5, -2). This anticipatory rise in sentiment mirrors the pre-event price run-up, suggesting that investors are either reacting to leaked information or independently growing more optimistic about the firm's prospects.

During the event window (-1, +1), sentiment surges further, with a highly significant CAS of 1.27 (t=2.61). This indicates a strong and immediate positive psychological reaction to the analyst's official endorsement. The most striking finding, however, is the prolonged and powerful elevation of sentiment in the post-announcement period. In the (6, 25) window, the CAS reaches a substantial and highly significant 13.84 (t=3.71). This sustained wave of optimism suggests that a "Buy" upgrade significantly reinforces investor confidence, likely triggering continued interest and positive discussion that perpetuates a bullish mood long after the initial news.

**Weaker Upgrades: A Story of Skepticism and Negative Sentiment**

In stark contrast, the sentiment dynamics for all other upgrade categories are surprisingly and profoundly negative. For upgrades to "Overweight," sentiment is already negative, though not significantly so, in the long pre-event window (CAS = -14.14). Critically, the upgrade announcement itself fails to lift this mood; the CAS around the event window is negligible. This implies that investors view this weaker positive signal with skepticism, and it lacks the power to shift a previously cautious or negative mindset.

The results for upgrades to "Hold" are even more pronounced. Here, investors exhibit a statistically significant negative sentiment _before_ the announcement (CAS = -7.9 in the -5, -2 window). The upgrade to "Hold" does nothing to reverse this pessimism; sentiment remains negative throughout the event and post-event periods. This suggests that investors interpret a move from "Sell" to "Hold" not as a positive reassessment, but merely as a confirmation that the company's problems, while perhaps less severe, are far from resolved. The analyst's action is seen as too little, too late.

The most dramatic negative sentiment reaction is reserved for the "Upgrade to Underweight" category. Paradoxically, this technically positive revision is met with a severe and statistically significant deterioration in sentiment. CAS is an astonishing -22.18 (t=-2.30) just before the announcement, and it worsens further during the event window to -9.65 (t=-1.98). This counterintuitive reaction strongly suggests that investors view such an upgrade with extreme cynicism. They may perceive it as a belated and wholly inadequate response to profoundly deteriorating fundamentals, seeing it as a signal of persistent risk rather than a sign of stabilization. The analyst's credibility is likely so damaged by this point that their "upgrade" is treated as irrelevant or even as a confirmation of how bad the situation truly is.

Table : Summary of downgrades' impact on CAS

| **Estimates** | **Downgrade to Sell** | **Downgrade to Underweight** | **Downgrade to Hold** | **Downgrade to Overweight** |
| --- | --- | --- | --- | --- |
| **(-25, -6)** | \-5.74 | \-23.72\* | 0.70 | 3.74 |
| (-0.57) | (-1.84) | (0.16) | (0.62) |
| **(-5, -2)** | \-2.45 | \-3.04 | \-0.95 | 2.60 |
| (-0.96) | (-0.82) | (-0.77) | (1.61) |
| **(-1, 1)** | \-0.69 | \-0.75 | \-0.28 | 2.12\*\*\* |
| (-0.52) | (-0.40) | (-0.45) | (2.82) |
| **(2, 5)** | \-5.24\* | \-5.60 | \-1.97 | 1.61 |
| (-1.84) | (-1.36) | (-1.60) | (1.04) |
| **(6, 25)** | \-3.76 | \-16.00 | \-6.41 | 26.31\*\*\* |
| (-0.35) | (-1.20) | (-1.41) | (4.45) |
| **n** | **392** | **221** | **1,876** | **1,083** |

### The Sentiment Reaction to Analyst Downgrades

(Table 13 and Figure 2)

The sentiment response to downgrades aligns more closely with theoretical expectations than the price response did, generally showing a shift towards pessimism. However, one category provides a major paradoxical exception.

**"Downgrade to Sell" and "Underweight": Confirming and Deepening Pessimism**

As expected, downgrades to the most negative ratings are associated with a clear pattern of deteriorating investor sentiment. For downgrades to "Underweight," a significant pre-existing pessimism is evident, with a CAS of -23.72 (t=-1.84) in the long pre-event window. This indicates that analysts are often downgrading stocks for which investor sentiment is already deeply negative. For both "Sell" and "Underweight" downgrades, the sentiment remains negative across all subsequent windows. The "Sell" downgrade, in particular, triggers a statistically significant negative CAS of -5.24 (t=-1.84) in the immediate post-announcement period (2, 5), confirming that this signal effectively solidifies and amplifies a bearish mood among investors.

**"Downgrade to Hold": A Signal of Neutrality and Indifference**

A downgrade to "Hold" is met with general indifference from a sentiment perspective. The CAS values across all event windows hover near zero and are never statistically significant. This suggests that investors perceive this type of revision as containing little new informational content. It neither stokes fear nor inspires excitement, functioning as a sentiment-neutral event that fails to materially shift investor psychology. This may be because it is seen as a weak signal of valuation normalization after a price run-up, leading to a deferral of decisions and a reduction in the trading activity that drives our sentiment index.

**"Downgrade to Overweight": A Paradoxical Surge in Optimism**

Arguably the most perplexing and theoretically intriguing sentiment result emerges from the "Downgrade to Overweight" category. Despite being a technical downgrade from a "Buy" rating, this revision triggers a powerful and significant surge in positive investor sentiment. Around the announcement window (-1, +1), CAS increases significantly to 2.12 (t=2.82), and in the long post-event period (6, 25), it spikes dramatically to an exceptionally strong and significant 26.31 (t=4.45).

This counterintuitive sentiment boom mirrors the positive price reaction for this category and demands careful interpretation. It strongly suggests that investors do not perceive this as a negative event. Instead, they appear to interpret it as:

- **A Quality Confirmation Signal:** The downgrade is seen as an acknowledgment that the stock, while still a high-quality "Overweight" holding, has simply matured in its price rally. This continued, albeit moderated, endorsement from the analyst boosts confidence.
- **A Positive Framing Effect:** The narrative within the analyst's report may be overwhelmingly positive, focusing on strong fundamentals and merely adjusting the rating for valuation reasons. Investors may be reacting to this positive framing rather than the negative headline.

Figure 2: Visualization of CAS for each category

# FURTHER DISCUSSION

## Pre-announcement period: anticipation and existing trends

Before analyst recommendations are officially changed, interesting patterns emerge in both stock returns and investor sentiment. For stocks about to be upgraded to "Buy", both abnormal returns (CAR) and abnormal sentiment (CAS) are significantly positive in the days leading up to the announcement. This suggests that either information about the upcoming upgrade is leaking, or both analysts and investors are concurrently recognizing positive developments. In contrast, for stocks that will be upgraded to "Overweight", prices are already rising (positive CAR), but investor sentiment (CAS) is often negative or neutral. This indicates that the early price increase is not driven by widespread positive sentiment among investors. A similar pattern of negative pre-announcement sentiment is observed for stocks upgraded to "Hold" and "Underweight", where CAS is significantly negative even though these are technically "upgrades" from worse ratings. This suggests that analysts might be upgrading stocks that still carry negative investor sentiment.

Regarding downgrades, stocks eventually downgraded to "Overweight" (from Buy) show positive, though not always significant, abnormal sentiment and consistently positive abnormal returns before the announcement. This implies that even before the formal, milder downgrade, the stocks are performing well, and sentiment is generally favorable. For stocks that will be downgraded to "Hold" or "Sell", abnormal returns are surprisingly positive in the pre-announcement period. However, investor sentiment (CAS) for these future downgrades is more mixed: neutral for "Hold" and leaning negative (though often not significantly so) for "Sell." A notable exception is the "Downgrade to Underweight" category, where investor sentiment is already significantly negative well before the downgrade, indicating deep pre-existing pessimism, while CAR is relatively flat. This pre-announcement phase suggests that analysts often react to existing price trends (especially for downgrades where CAR is positive) and that investor sentiment can sometimes be a leading indicator of analyst actions (as seen with negative CAS before some upgrades or "Downgrade to Underweight").

## Event window: immediate impact of recommendation changes

During the immediate period surrounding the announcement of a recommendation change (typically -1 to +1 day), the market's reaction in terms of price and sentiment can vary significantly. For "Upgrade to Buy" recommendations, both CAR and CAS are strongly positive and significant, showing a clear, favorable immediate response in both price and mood. Similarly, an "Upgrade to Overweight" also results in a significantly positive CAR, but the positive impact on CAS is less pronounced and not statistically significant, indicating a price reaction stronger than the immediate sentiment shift. For upgrades to "Hold" or "Underweight", the immediate impact is quite different: CAR is generally insignificant, and CAS remains negative (significantly so for "Upgrade to Underweight"). This demonstrates that these less optimistic upgrades fail to generate positive price momentum or improve investor sentiment at the time of announcement.

When analysts downgrade stocks, the event window reactions are particularly noteworthy. A "Downgrade to Overweight" paradoxically leads to significantly positive CAR and CAS. This suggests the market and investors view this mild downgrade from "Buy" as a continued endorsement rather than a negative signal. For "Downgrade to Hold", CAR is also positive and significant, but CAS is neutral to slightly negative and insignificant, indicating that prices rise despite no accompanying boost in investor enthusiasm. For "Downgrade to Underweight" and "Downgrade to Sell", the CAR around the event is generally not significantly negative (and even positive for "Sell"). Abnormal sentiment (CAS) during this period is also typically negative but often lacks statistical significance. This muted or even contrarian price reaction to negative downgrades, coupled with a somewhat negative but not overwhelming sentiment response, highlights a disconnect between the analyst's signal and the immediate market behavior.

## Post-announcement period: lingering effects and drifts

In the days and weeks following the recommendation change, the persistence of price and sentiment effects is examined. For "Upgrade to Buy", both CAR and CAS remain significantly positive, especially in the longer (+6 to +25 day) window. This indicates a sustained positive impact on both price momentum and investor optimism. However, for "Upgrade to Overweight", the initial positive CAR does not typically persist significantly, and CAS also remains largely insignificant post-announcement, suggesting a more short-lived impact. For "Upgrade to Hold", there is a notable delayed positive CAR in the (+6 to +25 day) window, despite CAS remaining negative and insignificant. This implies that while sentiment doesn't improve, some buying interest eventually emerges. "Upgrade to Underweight" sees continued negative CAS (borderline significant in the +2 to +5 day window) and insignificant CAR, reinforcing the lack of positive impact.

Following downgrades, the patterns are also diverse. After a "Downgrade to Overweight", the remarkable positive CAS effect continues and strengthens significantly in the (+6 to +25 day) window, and CAR also shows a positive, significant drift. This reinforces the idea that this type of downgrade is perceived positively over time. For "Downgrade to Hold", CAR shows a slight positive drift later on, while CAS tends to become more negative, though often insignificantly. This further widens the gap between positive price trends and a lack of positive sentiment. For "Downgrade to Underweight", CAS remains negative but insignificant, and CAR is also insignificant. The "Downgrade to Sell" category shows a borderline significantly negative CAS in the immediate (2 to 5 day) post-announcement period, suggesting a delayed negative sentiment reaction. However, CAR can still show a puzzling positive drift even further out (+6 to +25 days), highlighting the persistence of anomalous price behavior despite the severe downgrade and somewhat negative sentiment.

## Conclusion: A complex interplay of returns and sentiment

The analysis reveals a complex relationship between abnormal stock returns (CAR) and abnormal investor sentiment (CAS) following analyst recommendation changes. Clear alignment, where both price and sentiment move positively and significantly, is most evident for "Upgrade to Buy" recommendations and, counterintuitively, for "Downgrade to Overweight" recommendations. These instances suggest that investor mood and market prices are moving in tandem.

However, significant divergences are more common. Upgrades to less enthusiastic levels like "Overweight", "Hold", or "Underweight" often fail to generate positive abnormal sentiment, with CAS frequently remaining neutral or negative, even if CAR shows some positive movement (as with "Upgrade to Overweight" initially, or "Upgrade to Hold" later). This suggests that the formal act of an "upgrade" does not always translate into improved investor optimism, and price movements may be driven by a subset of investors or other factors.

The most striking dissimilarities occur with downgrades, particularly "Downgrade to Hold" and "Downgrade to Sell." These categories often exhibit positive abnormal returns before, during, and even after the downgrade, despite abnormal sentiment being neutral or tending towards negative. This indicates that, in the studied market, negative recommendations frequently do not lead to the expected price declines, and this positive price action occurs even without strong positive investor sentiment. Factors such as the absolute level of the recommendation (e.g., "Overweight" still being a favorable state), analysts reacting to prior price momentum, or market-specific conditions (like short-sale limitations) likely contribute to these observed divergences between market returns and investor sentiment. Overall, while sentiment can sometimes align with price movements, it is not a consistent predictor or driver of returns for all types of recommendation changes, especially in the case of downgrades within this specific dataset.

# SUGGESTION FOR FUTURE STUDY AND CONCLUSION

## Suggestion for future study

The findings of this thesis, particularly the identification of the "downgrade puzzle" and the frequent divergence between stock returns and investor sentiment, open up several compelling avenues for future scholarly inquiry. While this study has provided a comprehensive and contemporary analysis of the Vietnamese market, it has also uncovered anomalies and complexities that warrant deeper investigation. The following sections outline five primary directions for future research that could build upon this work, each aimed at further unraveling the unique dynamics of analyst recommendations and investor behavior in an emerging market context.

### Deconstructing the "Downgrade Puzzle": A Deep Dive into Counterintuitive Price Reactions

One of the most compelling and counterintuitive findings of this thesis is the "downgrade puzzle," where negative recommendation changes, particularly downgrades to "Hold" or "Sell" frequently fail to trigger the expected negative stock returns and, in many instances, are followed by positive price drifts. This phenomenon challenges the foundational principles of market efficiency and suggests that the informational content of a negative rating is processed differently in Vietnam compared to more mature markets. Future research should prioritize dissecting this puzzle from multiple theoretical and empirical angles.

- **Contrarian Investor Behavior:** A primary hypothesis to explore is that the puzzle is driven by the behavior of Vietnam's dominant retail investor base. Future studies could investigate whether a significant segment of these investors acts as contrarians, deliberately trading against analyst consensus. This could be motivated by a distrust of institutional advice, a belief that analysts are perpetually behind the curve, or a strategy to acquire stocks they perceive as undervalued "bargains" after a wave of pessimistic sentiment. A potential research design would involve analyzing high-frequency trading data, if accessible, to determine if buy order volume from retail-sized accounts systematically increases in the immediate aftermath of a downgrade announcement. Alternatively, survey-based studies could directly query Vietnamese investors about their perceptions of analyst credibility and their typical reactions to negative recommendations.
- **The "Bottoming-Out" Signal Hypothesis:** Another plausible explanation is that a public downgrade acts as a lagging indicator, signaling that a stock's price has already hit its nadir. By the time an analyst formalizes a negative rating, informed institutional investors may have already exited their positions, causing the primary price decline to occur before the announcement. The public downgrade then serves as a "clearing event" that removes uncertainty, signaling to recovery-focused or value investors that the worst is over and a rebound is imminent. To test this, future research could employ a more granular event-study timeline, analyzing cumulative abnormal returns in the weeks and days leading up to the downgrade. If a significant negative CAR is observed pre-event, followed by a flat or positive CAR post-event, it would lend strong support to this "bottoming-out" hypothesis.
- **Impact of Institutional Constraints:** The structural characteristics of the Vietnamese market, most notably the practical impossibility of short-selling for most investors, must be rigorously examined as a contributing factor. Short-selling is a key mechanism that allows pessimistic views to be directly translated into downward price pressure. In its absence, the market response to negative news is inherently asymmetric. Investors who agree with a downgrade can sell their existing shares, but those who don't own the stock have no simple way to profit from their bearish conviction. This structural friction could be sufficient to mute or even reverse the expected price impact of a downgrade. A comparative study analyzing downgrade effects in emerging markets with varying levels of short-sale restrictions could provide powerful insights into the importance of this institutional factor.
- **The "Profit-Taking" Signal Interpretation:** It is crucial to investigate the context in which downgrades occur. It is possible that analysts are not issuing downgrades because a company's fundamentals have deteriorated, but rather because its stock price has enjoyed a strong run-up and is now perceived as fully valued. In such a scenario, a downgrade from "Buy" to "Hold" might be interpreted by the market not as a bearish signal, but as rational advice to "take profits" on a successful investment. This interpretation would not necessarily lead to a price collapse, as underlying momentum could persist. A future study could systematically test this by correlating downgrades with the stock's performance over the preceding 3-to-6-month period. A regression model could determine if downgrades following periods of high abnormal returns are significantly less likely to result in negative future price movements.

### Investigating the Divergence Between Sentiment (CAS) and Returns (CAR)

This research consistently documented a significant and puzzling divergence between Cumulative Abnormal Sentiment (CAS) and Cumulative Abnormal Returns (CAR). For instance, upgrades to "Overweight" triggered strong positive price reactions (CAR), but a comparatively weak or delayed positive shift in sentiment (CAS). Conversely, certain downgrades generated strong negative sentiment but failed to produce a corresponding price drop. This disconnect suggests that investor psychology and market prices are not moving in lockstep, and future research should focus on understanding the nature and drivers of this gap.

- **Lead-Lag Relationship Analysis:** A critical unanswered question is the temporal relationship between sentiment and returns. Does sentiment lead prices, or do prices lead sentiment? It is possible that the CAS, derived from trading activity, is a consequence of price changes rather than a cause; investors may only become optimistic (as measured by trading volume and buy-sell imbalances) after they observe a price rally initiated by a few large, informed traders. A formal investigation using advanced time-series econometrics, such as Vector Autoregression (VAR) models or Granger causality tests, could establish the lead-lag dynamics between our CAS and CAR measures for different types of recommendation changes.
- **The Potency of Sentiment:** The puzzle of why strong negative sentiment does not always translate into price declines warrants further study. This could imply that the sentiment captured by our market-based proxies, while real, is not potent enough to move prices against countervailing forces, such as strong underlying buying interest or the aforementioned inability to short-sell. Alternatively, it may be that investors are compartmentalizing their reactions; they may "feel" negative about a stock, as reflected in sentiment proxies, but they are not compelled to sell based on other information or beliefs. Future research could explore this by building more complex models that include interaction terms to see if negative sentiment only impacts prices under specific conditions, such as high market volatility or during economic downturns.
- **Qualitative Analysis of Analyst Reports:** The headline rating is only one piece of the puzzle. The divergence between CAR and CAS might be explained by the detailed language, tone, and justifications provided within the full analyst reports. A downgrade accompanied by surprisingly optimistic narrative language about a company's long-term prospects could explain why sentiment turns negative while the price remains resilient. A powerful avenue for future research would be to employ Natural Language Processing (NLP) and content analysis techniques to score the textual content of analyst reports. By creating a "textual sentiment" score for each report, researchers could test whether this qualitative measure is a better predictor of price movements (CAR) or psychological shifts (CAS) than the simple categorical rating change, offering a much richer understanding of how information is truly transmitted.

### Analyzing Analyst-Specific and Recommendation-Specific Characteristics

This study treated all recommendation changes within a category as broadly similar. However, the identity of the analyst and the specific nature of their recommendation likely moderate the market's reaction. Future work could drill down into these characteristics to see if they can help explain the observed anomalies.

- **Analyst Reputation and Accuracy:** It would be highly valuable to determine if the "downgrade puzzle" and the CAR-CAS divergence are consistent across all analysts or are concentrated among those with lower reputations or weaker track records. It is plausible that recommendations from top-tier, consistently accurate analysts or prestigious brokerage houses generate more "rational" and aligned market responses, where downgrades lead to price drops and sentiment follows suit. A future study could segment the data based on analyst characteristics - such as brokerage size, analyst experience, or a calculated measure of historical forecast accuracy - and re-run the event study for each segment. This would clarify whether the observed market inefficiencies are a general phenomenon or are confined to lower-quality information signals.
- **Interaction with Price Target Revisions:** Analyst reports often contain both a rating change and a revised price target. These two signals can sometimes be conflicting. For example, what happens when an analyst downgrades a stock from "Buy" to "Hold" but simultaneously increases their 12-month price target? This mixed signal could convey underlying confidence despite the formal downgrade. A dedicated study could create interaction variables to explicitly model these events. By comparing the market reaction to a "pure" downgrade versus a downgrade accompanied by a price target increase, researchers could isolate the marginal impact of each piece of information and better explain puzzling price resilience.
- **The Impact of "Bold" Recommendations:** Recommendations that are particularly "bold" - meaning they deviate significantly from the prevailing consensus rating for a stock - are likely to contain more new information. Future research could quantify the "boldness" of each recommendation (e.g., by measuring its distance from the mean analyst rating) and test whether these bold calls trigger larger or more unusual reactions. One might hypothesize that bold downgrades are more likely to break through investor inertia and cause a price drop, while bold upgrades might generate a stronger alignment between CAR and CAS due to their high information content.

### Examining the Role of Investor Heterogeneity and Information Flows

The aggregate market reactions measured in this thesis mask the complex interactions occurring at the micro-level between different types of investors and competing information sources. Future research should aim to disaggregate these effects.

- **Retail vs. Institutional Investor Reactions:** A fundamental question in behavioral finance is whether different investor classes react differently to the same information. If suitable data can be accessed (e.g., through partnerships with brokerage firms), it would be incredibly informative to separate trading data into retail and institutional accounts. This would allow a direct test of the hypothesis that the "downgrade puzzle" is driven by contrarian retail buying, while institutions react more conventionally by selling. Such an analysis could reveal two parallel but opposing market reactions that are currently obscured within the aggregate CAR.
- **Interaction with Corporate and Economic News:** Analyst recommendations do not exist in a vacuum. Their impact is likely moderated by the broader information environment. A future study could enhance the event-study methodology by controlling for other significant news events occurring around the recommendation date, such as official company earnings announcements, M&A news, or major macroeconomic releases. This would help isolate the pure impact of the analyst's opinion from confounding information.
- **The Influence of Social and Local Media:** It is crucial to understand how analyst reports interact with sentiment expressed on popular local financial news platforms and social media. Using the news sources that Vietnamese investors are known to follow, such as Vietstock, Cafef, and VNEconomy, a future project could create a separate, daily sentiment index based on NLP analysis of articles and user comments. This "media sentiment" could then be compared to our market-based CAS and the price-based CAR. This would help answer critical questions: Does the market sentiment (CAS) simply reflect the mood of the financial media? How does the interplay between official analyst ratings and informal online chatter affect stock prices? This line of inquiry is particularly relevant in a market with high social media penetration and a large retail investor base.

### Enhancing and Expanding the Measurement of Investor Sentiment

While the Principal Component Analysis-based sentiment index (CAS) used in this thesis is robust and grounded in established literature, there is always an opportunity to refine and validate sentiment measures.

- **Triangulation with Alternative Sentiment Proxies:** To strengthen the validity of our findings, future research could construct and compare our CAS with alternative sentiment measures tailored for the Vietnamese context. These could include:
  - **Direct Investor Surveys:** Conducting regular surveys to directly gauge the optimism and pessimism of Vietnamese investors.
  - **Textual Analysis of News:** Expanding on the idea above, creating a comprehensive daily sentiment index from a wide basket of financial news sources.
  - **Search-Based Sentiment:** Utilizing Google Trends data for finance-related keywords in Vietnamese to capture retail investor attention and sentiment.  
        By comparing the results from these different methods, researchers could build a more holistic and nuanced picture of investor mood and confirm whether the CAR-CAS divergence is a robust phenomenon or an artifact of a specific measurement technique.
- **Long-Term Dynamics of CAR and CAS:** This study focused on short-term event windows. A significant contribution would be to track the evolution of CAR and CAS over much longer horizons (e.g., 6, 12, or 24 months) following a recommendation change. This would address whether the initial disconnect between sentiment and price eventually corrects itself. Does investor sentiment ultimately converge with the stock's fundamental performance? Or do these gaps persist, indicating long-term market inefficiencies? Understanding these longer-term dynamics would offer profound insights into the lasting impact of analyst advice and the ultimate rationality of the market.

## Conclusion

### Recapitulation of the Research Journey

This thesis embarked on an in-depth investigation into the multifaceted impact of analyst recommendation revisions within the dynamic and distinct context of the Vietnamese stock market. The study was born from a fundamental dichotomy: the well-established theoretical importance of financial analysts as information intermediaries in efficient markets, versus the practical realities of an emerging market characterized by unique institutional structures, behavioral biases, and a relative scarcity of contemporary academic scrutiny. Grounded in the extensive literature on analyst influence and investor sentiment, yet motivated by the sparse and often dated research specific to Vietnam, this study was structured around three core objectives: to diagnose systematic biases in analyst ratings, to measure the dual impact of recommendation changes on both stock returns and investor sentiment, and to critically compare these two streams of market reaction.

To navigate this complex terrain, this research adopted a robust and multi-pronged methodological approach. By leveraging a large, contemporary dataset of over 7,000 recommendation changes from 2014 to 2024, the study moved beyond the limitations of prior work. Crucially, it introduced a novel analytical dimension by constructing a bespoke, firm-level investor sentiment index using Principal Component Analysis (PCA) on a suite of market-based proxies. This allowed for a parallel event-study framework, simultaneously tracking Cumulative Abnormal Returns (CAR) to measure price impact and Cumulative Abnormal Sentiment (CAS) to measure psychological impact. This dual-pronged strategy was designed to provide a granular and current understanding of the intricate interplay between expert guidance, market prices, and investor psychology. The findings that emerged from this comprehensive analysis have provided clear answers to each research objective, culminating in a portrait of a market that operates with its own unique, often counterintuitive, and fascinating logic.

### **Synthesis of Principal Findings**

The empirical results of this thesis have yielded several key findings that, taken together, challenge conventional assumptions and illuminate the specific character of the Vietnamese market.

First, in response to the objective of analyzing potential biases, this study empirically confirms the existence of a profound and persistent optimism bias among analysts covering Vietnamese stocks. The descriptive data unequivocally shows that an overwhelming majority of all ratings issued are positive. "Buy" and "Overweight" recommendations collectively constitute over 62% of the entire sample, while overtly negative ratings like "Sell" and "Underweight" are exceptionally rare, making up a mere 7.3%. This optimistic skew is not just a static feature but also influences the dynamics of recommendation changes. Analysts exhibit notable caution when issuing downgrades, frequently tempering them to a neutral "Hold" or a still-favorable "Overweight" rating, rather than an outright "Sell." This finding aligns with trends observed in other emerging markets and underscores a critical feature of the information environment that Vietnamese investors must navigate - one where positive reinforcement is the norm and truly negative signals are a significant deviation.

Second, this thesis sought to determine how analyst recommendation revisions influence stock returns (CAR) and investor sentiment (CAS). The results demonstrate that this influence is highly conditional, asymmetric, and often anomalous. The market does respond rationally to clear, unambiguously positive news: "Upgrade to Buy" recommendations successfully trigger a statistically significant and sustained positive response in both stock prices and investor mood. However, beyond this single case of textbook behavior, the market's reaction deviates sharply from established theories. Most notably, the study uncovered a significant "downgrade puzzle": severe downgrades to "Hold" or "Sell" largely fail to induce the expected negative price pressure. Instead, stocks often display puzzling price resilience and, in some cases, even a positive post-event drift. In a further paradoxical twist, the mildest form of negative revision, the "Downgrade to Overweight," is interpreted by the market as a positive signal, leading to significant and positive drifts in both returns and sentiment. This suggests investors may perceive it as a profit-taking signal on a fundamentally strong company rather than a bearish warning.

Third, in addressing the objective to compare the responses of stock returns and investor sentiment, this research uncovers its central empirical finding: a frequent and significant divergence between price and psychology. Clear alignment, where CAR and CAS move in tandem, proved to be the exception rather than the rule. This harmony was primarily observed in the case of strong "Buy" upgrades and the counterintuitively positive "Overweight" downgrades. More commonly, stock prices and investor sentiment told different stories. Less enthusiastic upgrades, for instance, often failed to lift investor mood measurably even as prices edged higher. Most strikingly, the surprising price increases following severe downgrades occurred despite neutral or even deteriorating sentiment. This consistent disconnect challenges the simplistic assumption that price movements are a direct reflection of collective investor psychology. It strongly indicates that, in the Vietnamese market, analyst signals are filtered through a unique local lens, shaped by factors that can cause prices and sentiment to lead separate lives.

## Implications of the Research

The findings of this thesis carry significant implications for various stakeholders, from individual investors to academic researchers.

- **For Investors and Practitioners:** The results serve as a critical and actionable warning that trading strategies ported from developed markets are not directly transferable to Vietnam. A downgrade is not a straightforward sell signal; indeed, it may paradoxically signal a price bottom. Investors must cultivate a more nuanced "second-level" thinking, understanding that the headline recommendation may be less important than the underlying context and the unique structural dynamics of the market.
- **For Analysts and Brokerage Houses:** The muted price impact of negative ratings calls into question their efficacy as a market-disciplining force. If downgrades fail to correct potential overvaluation, it raises questions about the value proposition of sell-side research in this market, particularly its role in promoting market efficiency and price discovery.
- **For Academics and Regulators:** This study reinforces the fundamental principle that market behavior is not universal but is deeply embedded in its institutional and cultural context. The "downgrade puzzle" and the CAR-CAS divergence are likely symptoms of the unique interplay between documented herding behavior, a retail-dominated investor base, and institutional frictions like the absence of a robust short-selling mechanism. For regulators, these findings highlight potential market inefficiencies and the powerful influence of behavioral biases, suggesting that investor education and enhancing market transparency remain critical priorities.

# REFERENCE

Altınkılıç, O. and Hansen, R.S., 2009. On the information role of stock recommendation revisions. _Journal of Accounting and Economics_, _48_(1), pp.17-36.

Asquith, P., Mikhail, M.B. and Au, A.S., 2005. Information content of equity analyst reports. _Journal of financial economics_, _75_(2), pp.245-282.

Baker, M. and Stein, J.C., 2004. Market liquidity as a sentiment indicator. _Journal of financial Markets_, _7_(3), pp.271-299.

Baker, M. and Wurgler, J., 2006. Investor sentiment and the cross‐section of stock returns. _The journal of Finance_, _61_(4), pp.1645-1680.

Baker, M. and Wurgler, J., 2007. Investor sentiment in the stock market. _Journal of economic perspectives_, _21_(2), pp.129-151.

Baker, M., Wurgler, J. and Yuan, Y., 2012. Global, local, and contagious investor sentiment. _Journal of financial economics_, _104_(2), pp.272-287.

Bandopadhyaya, A. and Jones, A.L., 2008. Measures of investor sentiment: A comparative analysis put-call ratio vs. volatility index. _Journal of Business & Economics Research (JBER)_, _6_(8).

Barber, B., Lehavy, R., McNichols, M. and Trueman, B., 2001. Can investors profit from the prophets? Security analyst recommendations and stock returns. _The Journal of finance_, _56_(2), pp.531-563.

Barber, B.M., Lehavy, R. and Trueman, B., 2010. Ratings changes, ratings levels, and the predictive value of analysts' recommendations. _Financial Management_, _39_(2), pp.533-553.

Barber, B.M., Odean, T. and Zhu, N., 2009. Systematic noise. _Journal of Financial Markets_, _12_(4), pp.547-569.

Boubaker, S., Farag, H. and Nguyen, D.K., 2015. Short-term overreaction to specific events: Evidence from an emerging market. _Research in international business and finance_, _35_, pp.153-165.

Bradley, D., Clarke, J., Lee, S. and Ornthanalai, C., 2014. Are analysts' recommendations informative? Intraday evidence on the impact of time stamp delays. _The Journal of Finance_, _69_(2), pp.645-673.

Brown, G.W., 1999. Volatility, sentiment, and noise traders. _Financial Analysts Journal_, _55_(2), pp.82-90.

Bui, N.D., Nguyen, L.T.B., Nguyen, N.T.T. and Titman, G.F., 2018. Herding in frontier stock markets: Evidence from the Vietnamese stock market. _Accounting & Finance_, _58_, pp.59-81.

Carhart, M.M., 1997. On persistence in mutual fund performance. _The Journal of finance_, _52_(1), pp.57-82.

Chang, E.C., Luo, Y. and Ren, J., 2014. Short-selling, margin-trading, and price efficiency: Evidence from the Chinese market. _Journal of Banking & Finance_, _48_, pp.411-424.

Chen, H., Chong, T.T.L. and Duan, X., 2010. A principal-component approach to measuring investor sentiment. _Quantitative Finance_, _10_(4), pp.339-347.

Choi, H.S., Ryu, D. and Yang, H., 2018. International transmission of risk factor movements: The case of developed markets. _Investment Analysts Journal_, _47_(2), pp.111-126.

Chong, T.T.L. and Ng, W.K., 2008. Technical analysis and the London stock exchange: testing the MACD and RSI rules using the FT30. _Applied Economics Letters_, _15_(14), pp.1111-1114.

Chung, C.Y., Cho, S.J., Ryu, D. and Ryu, D., 2019. Institutional blockholders and corporate social responsibility. _Asian Business & Management_, _18_, pp.143-186.

Chung, C.Y., Lee, Y. and Ryu, D., 2017. Do domestic institutional trades exacerbate information asymmetry? Evidence from the Korean stock market. _Asia-Pacific Financial Markets_, _24_, pp.309-322.

Drake, M.S., Roulstone, D.T. and Thornock, J.R., 2012. Investor information demand: Evidence from Google searches around earnings announcements. _Journal of Accounting research_, _50_(4), pp.1001-1040.

Da, Z., Engelberg, J. and Gao, P., 2015. The sum of all FEARS investor sentiment and asset prices. _The Review of Financial Studies_, _28_(1), pp.1-32.

Fang, L.H. and Yasuda, A., 2014. Are stars' opinions worth more? The relation between analyst reputation and recommendation values. _Journal of Financial Services Research_, _46_, pp.235-269.

Frankel, R., Kothari, S.P. and Weber, J., 2006. Determinants of the informativeness of analyst research. _Journal of Accounting and Economics_, _41_(1-2), pp.29-54.

Howe, J.S., Unlu, E. and Yan, X., 2009. The predictive content of aggregate analyst recommendations. _Journal of Accounting Research_, _47_(3), pp.799-821.

Hribar, P. and McInnis, J., 2012. Investor sentiment and analysts' earnings forecast errors. _Management science_, _58_(2), pp.293-307.

Ivković, Z. and Jegadeesh, N., 2004. The timing and value of forecast and recommendation revisions. _Journal of Financial Economics_, _73_(3), pp.433-463.

Jegadeesh, N., Kim, J., Krische, S.D. and Lee, C.M., 2004. Analyzing the analysts: When do recommendations add value?. _The journal of finance_, _59_(3), pp.1083-1124.

Jegadeesh, N. and Kim, W., 2006. Value of analyst recommendations: International evidence. _Journal of Financial Markets_, _9_(3), pp.274-309.

Juergens, J.L. and Lindsey, L., 2009. Getting out early: An analysis of market making activity at the recommending analyst's firm. _The Journal of Finance_, _64_(5), pp.2327-2359.

Jolliffe, I.T. and Cadima, J., 2016. Principal component analysis: a review and recent developments. _Philosophical transactions of the royal society A: Mathematical, Physical and Engineering Sciences_, _374_(2065), p.20150202.

Kim, D. and Na, H., 2018. Investor sentiment, anomalies, and macroeconomic conditions. _Asia‐Pacific Journal of Financial Studies_, _47_(6), pp.751-804.

Kim, K., Ryu, D. and Yang, H., 2018. Investor sentiment indices and the cross-section of stock returns of individual firms. _Korean Management Review_, _47_(5), pp.1231-1260.

Kim, J.S., Ryu, D. and Seo, S.W., 2014. Investor sentiment and return predictability of disagreement. _Journal of Banking & Finance_, _42_, pp.166-178.

Kim, K., Ryu, D. and Yang, H., 2019. Investor sentiment, stock returns, and analyst recommendation changes: The KOSPI stock market. _Investment Analysts Journal_, _48_(2), pp.89-101.

Kumar, A. and Lee, C.M., 2006. Retail investor sentiment and return comovements. _The Journal of Finance_, _61_(5), pp.2451-2486.

Lan, N.N.P., TÂM LÝ NHÀ ĐẦU TƯ, THÔNG TIN KẾ TOÁN VÀ GIÁ CỔ PHIẾU TRÊN THỊ TRƯỜNG CHỨNG KHOÁN VIỆT NAM.

Loh, R.K. and Stulz, R.M., 2011. When are analyst recommendation changes influential?. _The review of financial studies_, _24_(2), pp.593-627.

MacKinlay, A.C., 1997. Event studies in economics and finance. _Journal of economic literature_, _35_(1), pp.13-39.

Michaely, R. and Womack, K.L., 1999. Conflict of interest and the credibility of underwriter analyst recommendations. _The review of financial studies_, _12_(4), pp.653-686.

Morgan, P.J. and Trinh, L.Q., 2019. Determinants and impacts of financial literacy in Cambodia and Viet Nam. _Journal of Risk and Financial Management_, _12_(1), p.19.

Moshirian, F., Ng, D. and Wu, E., 2009. The value of stock analysts' recommendations: Evidence from emerging markets. _International Review of Financial Analysis_, _18_(1-2), pp.74-83.

Nguyen, C., Hoang, L., Shim, J. and Truong, P., 2020. Internet search intensity, liquidity and returns in emerging markets. _Research in International Business and Finance_, _52_, p.101166.

Nguyen, D.D. and Pham, M.C., 2018. Search-based sentiment and stock market reactions: An empirical evidence in Vietnam. _The Journal of Asian Finance, Economics and Business_, _5_(4), pp.45-56.

Nguyen, H.H., Ngo, V.M., Pham, L.M. and Van Nguyen, P., 2025. Investor sentiment and market returns: A multi-horizon analysis. _Research in International Business and Finance_, _74_, p.102701.

Nguyen, T.A. and Vuong, M.N., 2025. Does corporate governance add value to target price forecast in developing markets: the context of Vietnam. _Cogent Business & Management_, _12_(1), p.2496735.

Phuong, L.C.M. and Nhung, V.C., 2021. Investor sentiment measurement based on technical analysis indicators affecting stock returns: Empirical evidence on VN100. _Investment Management & Financial Innovations_, _18_(4), p.297.

Phuong, L.C.M., 2021. Investor sentiment by relative strength index and stock return: Empirical evidence on Vietnam's stock market. _Accounting_, _7_(2), pp.451-456.

Quang, L.T., Linh, N.D., Van Nguyen, D. and Khoa, D.D., 2023. Behavioral factors influencing individual investors' decision making in Vietnam market. _Journal of Eastern European and Central Asian Research (JEECAR)_, _10_(2), pp.264-280.

Ryu, D., Ryu, D. and Yang, H., 2020. Investor sentiment, market competition, and financial crisis: Evidence from the Korean stock market. _Emerging Markets Finance and Trade_, _56_(8), pp.1804-1816.

Sorescu, S. and Subrahmanyam, A., 2006. The cross section of analyst recommendations. _Journal of Financial and Quantitative Analysis_, _41_(1), pp.139-168.

Stickel, S.E., 1995. The anatomy of the performance of buy and sell recommendations. _Financial analysts journal_, _51_(5), pp.25-39.

Thanh, C.N., Huy, T.P. and Nhat, A.N., 2024. Investor sentiments and Fama-French five-factor in Vietnam market. _International Journal of Revenue Management_, _14_(2), pp.203-220.

Thai, H.M., Thu, T.H.T., Ngoc, S.P. and Thi, A.M., 2023, May. Corporate Governance and the Accuracy of Analysts' Earnings Forecast in Vietnam. In _International Conference on Emerging Challenges: Strategic Adaptation in The World of Uncertainties (ICECH 2022)_ (pp. 442-466). Atlantis Press.

Van Huy Bui, V.M.H., Nguyen, D.T.M.T., Bich Loc Tram, G.Q.P. and Nguyen, H., Market's Reaction to Analytical Information From Brokerage Institutions: Empirical Evidence From Stock Market in Vietnam.

Vo, X.V. and Phan, D.B.A., 2017. Further evidence on the herd behavior in Vietnam stock market. _Journal of Behavioral and Experimental Finance_, _13_, pp.33-41.

Vo, X.V. and Phan, D.B.A., 2019. Herd behavior and idiosyncratic volatility in a frontier market. _Pacific-Basin Finance Journal_, _53_, pp.321-330.

Womack, K.L., 1996. Do brokerage analysts' recommendations have investment value?. _The journal of finance_, _51_(1), pp.137-167.

Yang, H., Ryu, D. and Ryu, D., 2017. Investor sentiment, asset returns and firm characteristics: Evidence from the Korean stock market. _Investment Analysts Journal_, _46_(2), pp.132-147.