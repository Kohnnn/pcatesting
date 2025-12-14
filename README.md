# SentimentAlpha Vietnam

Trading signals platform for Vietnamese stock market based on analyst recommendations and sentiment analysis. Built on academic research investigating the "Downgrade Puzzle" - a market anomaly where analyst downgrades paradoxically lead to positive price movements in emerging markets.

## Quick Start

```bash
manage.bat
# Select option 1 to start both servers
```

Then open http://localhost:3000

## Project Status

**Current Phase**: Production-ready MVP with comprehensive testing framework

**Key Achievements**:
- ✅ Complete data pipeline with validation, transformation, and audit trail
- ✅ Four signal types based on academic research (Contrarian Dip Buy, Momentum Breakout, Retail Trap, Neutral)
- ✅ Composite sentiment index using PCA on 5 technical indicators (BSI, ATR, LTV, RSI, PLI)
- ✅ Event study analysis with CAR/CAS calculations
- ✅ Full-stack application with dark mode, responsive design, and comprehensive error handling
- ✅ Property-based testing with Hypothesis (70%+ coverage)
- ✅ Data Management interface with pipeline control and quality monitoring

**Recent Updates**:
- Fixed dark mode toggle and theme persistence
- Added comprehensive error handling across all pages
- Implemented data quality dashboard with validation metrics
- Built pipeline orchestration with resource monitoring
- Created export functionality for all data tables

See [progress.md](progress.md) for detailed development roadmap.

## Documentation

- **[brief.md](brief.md)** - Project overview, concept, and goals
- **[tech.md](tech.md)** - Technical documentation and architecture
- **[progress.md](progress.md)** - Development status and roadmap
- **[danielthesis.md](danielthesis.md)** - Academic research foundation

## Requirements

- Python 3.8+
- Node.js 16+
- Windows OS (for batch scripts)

## First Time Setup

```bash
manage.bat
# Select option 2 for full setup
```

This will:
1. Install Python dependencies
2. Install Node.js dependencies
3. Initialize the database
4. Seed initial data

### I'm currently hoasting it on:
https://pcatesting.share.zrok.io/

## Core Features

### Signal Generation
- **Contrarian Dip Buy**: Downgrade + high sentiment + positive foreign flow
- **Momentum Breakout**: Upgrade + rising sentiment + RSI < 70
- **Retail Trap**: Downgrade + high BSI + negative foreign flow
- **Neutral / No Edge**: All other combinations

### Sentiment Analysis
- Five technical indicators: BSI, ATR, LTV, RSI, PLI
- PCA-based composite sentiment index
- Pure sentiment (market-adjusted, firm-specific)
- Historical sentiment tracking per ticker

### Data Pipeline
- Automatic Excel file detection and type identification
- Schema validation for all input file types
- Incremental updates to avoid reprocessing
- Data quality checks and validation
- Audit trail for all pipeline operations
- Resource monitoring during execution

### User Interface
- 📊 Dashboard with recent signals and detailed analysis
- 🔍 Signals page with filtering by signal type
- 💼 Portfolio watchlist management
- 🗄️ Data Management interface with pipeline control
- ⚙️ Settings page for threshold configuration
- 📖 About page with comprehensive thesis documentation
- 🌓 Dark/light theme support
- 📱 Responsive design for mobile and desktop

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov=backend

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/property/
```

## Architecture

**Backend**: FastAPI + Python + SQLite
- RESTful API with comprehensive error handling
- Data pipeline orchestration
- Signal generation engine
- Event study analyzer

**Frontend**: Next.js + React + TypeScript + Tailwind CSS
- Server-side rendering for performance
- Real-time data updates
- Interactive charts with Recharts
- Theme persistence with localStorage

**Data Processing**: Pandas + NumPy + Scikit-learn
- Excel file processing
- PCA-based sentiment index
- Statistical calculations (CAR, CAS, t-statistics)

## Next Steps

**High Priority**:
- Backtesting framework for signal performance evaluation
- Signal performance tracking (win rate, average return)
- PostgreSQL migration for production deployment
- User authentication and authorization
- Real-time data updates via API

**Medium Priority**:
- Portfolio performance tracking with risk metrics
- Advanced charting with technical indicators
- PDF report generation
- API response caching with Redis
- Mobile app (React Native)

See [progress.md](progress.md) for complete roadmap.

Huge thank to Dandan [danielthesis.md](danielthesis.md) for the cool thesis.
