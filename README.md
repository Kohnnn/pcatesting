# SentimentAlpha Vietnam 🇻🇳

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/next.js-14.0-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104%2B-009688)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Transform Vietnamese stock market analyst recommendations into actionable trading signals using academic research and sentiment analysis.

## Overview

SentimentAlpha Vietnam is a full-stack financial analytics platform implementing the "Downgrade Puzzle" research for the Vietnamese stock market. The system processes market data, constructs sentiment indices using PCA, performs event study analysis (CAR/CAS), and generates trading signals based on documented market anomalies.

## Features

- **Sentiment Index Construction** - Multi-factor analysis using RSI, BSI, ATR, LTV, and PLI
- **PCA-Based Aggregation** - Principal Component Analysis to extract pure sentiment signals
- **Event Study Analysis** - CAR (Cumulative Abnormal Returns) and CAS (Cumulative Abnormal Sentiment)
- **Signal Generation** - Four signal types: Contrarian Dip Buy, Momentum Breakout, Retail Trap, Neutral
- **Data Management** - Browse, filter, and export database tables with quality monitoring
- **Automated Pipeline** - Incremental data updates with validation

## Project Structure

```
sentimentalpha-vietnam/
├── backend/                 # FastAPI REST API
│   ├── routers/            # API route handlers
│   ├── services/           # Business logic services
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js 14 Dashboard
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── contexts/          # React contexts (Theme)
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API client
│   └── package.json       # Node dependencies
├── src/                    # Core analytics engine
│   ├── sentiment_engine.py
│   ├── alpha_generator.py
│   ├── event_study_analyzer.py
│   ├── data_loader.py
│   ├── data_transformer.py
│   └── pipeline_orchestrator.py
├── tests/                  # Test suites
│   ├── unit/
│   ├── integration/
│   └── property/          # Hypothesis property tests
├── xlsx/                   # Raw CSV data files
├── data/                   # Processed Parquet files
├── dev.bat                # Development script (Windows)
├── requirements.txt       # Root Python dependencies
└── seed_data.py          # Database initialization
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/sentimentalpha-vietnam.git
cd sentimentalpha-vietnam

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Initialize database and run data pipeline
python update_data.py
```

**Note:** Use `update_data.py` instead of `seed_data.py` for complete setup. This will:
- Load all market data
- Generate sentiment indices
- Create trading signals
- Populate all database tables

### Running the Application

**Windows (Recommended):**
```cmd
dev.bat
```
Select option `[2]` to start both servers.

**Manual Start:**
```bash
# Terminal 1 - Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Troubleshooting:**
If servers don't start or no data appears:
```bash
# Run diagnostics
python diagnose_startup.py

# Populate database if needed
python update_data.py
```

### Access Points

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| Data Management | http://localhost:3000/data-management |
| API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_PATH=sentimentalpha.db

# Data directories
DATA_SOURCE_DIR=xlsx
DATA_OUTPUT_DIR=data

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## API Reference

### Signals
```http
GET /signals                    # List all signals
GET /signals/{ticker}           # Get signals for ticker
```

### Sentiment
```http
GET /sentiment/{ticker}         # Get sentiment data
```

### Data Management
```http
GET /data-management/tables              # List tables
GET /data-management/tables/{name}       # Get table data
GET /data-management/instruments/{ticker} # Instrument details
GET /data-management/quality             # Quality metrics
```

### Pipeline
```http
POST /pipeline/run              # Run data pipeline
GET /pipeline/status/{run_id}   # Check status
GET /pipeline/history           # Pipeline history
```

### Export
```http
GET /export/{table_name}.csv    # Export as CSV
GET /export/{table_name}.json   # Export as JSON
GET /export/daily_signals.csv   # Daily signals report
```

### Settings & Watchlist
```http
GET/POST /settings              # User settings
GET/POST/DELETE /watchlist      # Watchlist management
```

## Data Pipeline

### Input Files (xlsx/)

| File Pattern | Description |
|--------------|-------------|
| close1-9.csv | Closing prices |
| buy1-9.csv | Buy volumes |
| sell1-9.csv | Sell volumes |
| tra1-9.csv | Total trading volumes |
| sha1-9.csv | Shares outstanding |
| rec.csv | Analyst recommendations |
| vnindex.csv | Market index |
| rfr.csv | Risk-free rate |

### Incremental Updates

```bash
python update_data.py
```

Or use `dev.bat` option `[7]`.

## Testing

```bash
# All tests
pytest tests/ -v

# By category
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/property/ -v

# With coverage
pytest tests/ -v --cov=src --cov=backend --cov-report=html
```

## Development Script (dev.bat)

The comprehensive development script provides:

1. **Full Setup** - Install all dependencies + initialize database
2. **Start Dev Servers** - Launch frontend and backend concurrently
3. **Database Operations** - Seed, backup, restore, reset
4. **Test Suite** - Run unit, integration, property tests
5. **Data Updates** - Incremental pipeline execution
6. **Debug Mode** - Verbose logging for troubleshooting
7. **Clean Artifacts** - Remove cache and build files

## Deployment

### Production Build

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)

```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
COPY src/ ./src/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Considerations

- Set `ENVIRONMENT=production`
- Use PostgreSQL for production database
- Configure CORS for your domain
- Set up reverse proxy (nginx)
- Enable HTTPS

## Architecture

```
CSV Files → Data Pipeline → SQLite/Parquet → Analytics Engine → FastAPI → Next.js Dashboard
```

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Pipeline | Python/Pandas | ETL from CSV |
| Analytics | NumPy/Scikit-learn | Sentiment & signals |
| Backend | FastAPI | REST API |
| Frontend | Next.js 14 + TypeScript | Dashboard |
| Database | SQLite | Persistence |
| Testing | Pytest + Hypothesis | Quality assurance |

## Academic Background

Based on research showing that severe analyst downgrades can lead to positive price drifts when:
1. Pure sentiment remains positive (contrarian indicator)
2. Foreign institutional investors are buying (NFB > 0)
3. Retail investors are selling (creating opportunity)

### Methodology
1. **Sentiment Construction** - PCA on 5 market indicators
2. **Purification** - Regression against market returns
3. **Event Study** - CAR/CAS analysis around recommendations
4. **Signal Classification** - Rule-based on research findings

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/sentimentalpha-vietnam/issues)
- **Email**: your.email@example.com

---

**Built for the Vietnamese stock market** 🇻🇳
