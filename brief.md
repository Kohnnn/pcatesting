# SentimentAlpha Vietnam - Project Brief

## Application Description

SentimentAlpha Vietnam is a trading signal platform that analyzes Vietnamese stock market data by combining analyst recommendations with investor sentiment indicators. The application generates actionable trading signals based on academic research into market anomalies, specifically the "Downgrade Puzzle" phenomenon observed in emerging markets.

The platform provides traders and investors with:
- Real-time trading signals based on analyst actions and sentiment analysis
- Comprehensive sentiment tracking using five technical indicators (BSI, ATR, LTV, RSI, PLI)
- Event study analysis showing cumulative abnormal returns (CAR) and sentiment (CAS)
- Portfolio watchlist management
- Data pipeline for processing market data from Excel files

## Foundational Concept

The project is built upon academic research investigating the relationship between investor sentiment and analyst recommendations in the Vietnamese stock market. The core finding is the "Downgrade Puzzle" - a market anomaly where severe analyst downgrades paradoxically lead to positive price drifts, contrary to efficient market expectations.

**Key Research Principles**:
- **Sentiment Composite Index**: Five sentiment proxies (BSI, ATR, LTV, RSI, PLI) combined using Principal Component Analysis (PCA)
- **Pure Sentiment**: Sentiment residual after regressing against market returns to isolate firm-specific sentiment
- **Event Study Methodology**: Measuring CAR and CAS over event windows (-25 to +25 days) around analyst recommendation changes
- **Foreign vs Retail Divergence**: When foreign institutional investors diverge from retail sentiment, foreign flows tend to be more predictive

## What Is Being Built

A full-stack web application consisting of:

**Frontend (Next.js + React + TypeScript)**:
- Dashboard with recent signals and detailed analysis
- Signals page with filtering and export capabilities
- Portfolio watchlist for tracking favorite stocks
- Data Management interface for pipeline control and data quality monitoring
- Settings page for configuring signal thresholds
- About page with comprehensive thesis documentation
- Dark/light theme support

**Backend (FastAPI + Python)**:
- RESTful API for serving trading signals and market data
- Data pipeline for processing Excel files (recommendations, prices, sentiment proxies)
- Signal generation engine implementing academic research logic
- Event study analyzer for CAR/CAS calculations
- Database management with SQLite

**Data Processing Pipeline**:
- Automatic detection and processing of Excel files
- Schema validation and data quality checks
- Incremental updates to avoid reprocessing
- Audit trail for all pipeline operations

## Core Requirements

### Functional Requirements
1. **Signal Generation**: Generate four types of trading signals based on analyst actions and market conditions:
   - Contrarian Dip Buy (downgrade + high sentiment + positive foreign flow)
   - Momentum Breakout (upgrade + rising sentiment + RSI < 70)
   - Retail Trap (downgrade + high BSI + negative foreign flow)
   - Neutral / No Edge (all other combinations)

2. **Data Management**: Process and validate market data from multiple Excel sources:
   - Analyst recommendations with rating standardization
   - Daily price and volume data
   - Sentiment proxy calculations (BSI, ATR, LTV, RSI, PLI)
   - Foreign flow tracking (Net Foreign Buy)

3. **Event Study Analysis**: Calculate and display CAR and CAS around analyst recommendation changes

4. **Portfolio Management**: Allow users to create and manage watchlists of stocks

5. **Data Quality Monitoring**: Track data completeness, freshness, and validation errors

### Technical Requirements
1. **Performance**: Handle datasets with 100,000+ rows efficiently
2. **Reliability**: Robust error handling and data validation
3. **Maintainability**: Clean code architecture with comprehensive testing
4. **Usability**: Intuitive UI with helpful error messages and guidance
5. **Accessibility**: Full dark mode support and responsive design

### Core Goals
1. **Academic Rigor**: Implement research methodology faithfully and accurately
2. **Practical Utility**: Provide actionable signals that traders can use
3. **Data Integrity**: Ensure all calculations are correct and auditable
4. **User Experience**: Make complex financial analysis accessible and understandable
5. **Scalability**: Design for future expansion to other markets or signal types
