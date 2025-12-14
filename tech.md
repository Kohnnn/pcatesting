# SentimentAlpha Vietnam - Technical Documentation

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Heroicons
- **HTTP Client**: Axios
- **State Management**: React Hooks (useState, useEffect, useContext)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **ASGI Server**: Uvicorn
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas, NumPy
- **Validation**: Pydantic
- **Testing**: Pytest, Hypothesis (property-based testing)

### Development Tools
- **Package Management**: npm (frontend), pip (backend)
- **Code Quality**: ESLint (frontend), Black/Flake8 (backend)
- **Version Control**: Git
- **Testing**: Jest (frontend), Pytest (backend)

## System Architecture

### High-Level Architecture
```
┌─────────────────┐
│   Web Browser   │
│  (Next.js App)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Server │
│   (Port 8000)   │
└────────┬────────┘
         │
         ├─────────► SQLite Database
         │           (sentimentalpha.db)
         │
         └─────────► Excel Files
                     (xlsx/ directory)
```

### Frontend Architecture
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with theme provider
│   ├── page.tsx           # Dashboard (home page)
│   ├── signals/           # Signals list page
│   ├── portfolio/         # Watchlist page
│   ├── data-management/   # Data pipeline UI
│   ├── settings/          # Configuration page
│   └── about/             # Documentation page
├── components/            # Reusable React components
│   ├── charts/           # Chart components (Recharts)
│   ├── Sidebar.tsx       # Navigation sidebar
│   ├── ThemeToggle.tsx   # Dark mode toggle
│   └── ...
├── contexts/             # React contexts
│   └── ThemeContext.tsx  # Theme state management
├── hooks/                # Custom React hooks
│   ├── useSignals.ts     # Fetch signals data
│   ├── usePipeline.ts    # Pipeline operations
│   └── ...
├── services/             # API client
│   └── api.ts            # Axios-based API calls
└── types/                # TypeScript type definitions
    └── index.ts
```

### Backend Architecture
```
backend/
├── main.py               # FastAPI application entry point
├── database.py           # SQLAlchemy setup and session management
├── models.py             # SQLAlchemy ORM models
├── schemas.py            # Pydantic schemas for validation
├── routers/              # API route handlers
│   ├── signals.py        # Trading signals endpoints
│   ├── sentiment.py      # Sentiment data endpoints
│   ├── event_study.py    # Event study endpoints
│   ├── data_management.py # Data browsing endpoints
│   ├── pipeline.py       # Pipeline control endpoints
│   ├── settings.py       # Configuration endpoints
│   ├── watchlist.py      # Watchlist endpoints
│   └── export.py         # Data export endpoints
└── services/             # Business logic services
```

### Data Processing Architecture
```
src/
├── data_loader.py        # Excel file reading and parsing
├── file_detector.py      # Automatic file type detection
├── schema_validator.py   # Schema validation for Excel files
├── data_validator.py     # Data quality validation
├── data_transformer.py   # Data transformation and cleaning
├── data_cleaner.py       # Data cleaning utilities
├── data_consolidator.py  # Merge data from multiple sources
├── sentiment_engine.py   # Sentiment calculation (PCA)
├── alpha_generator.py    # Signal generation logic
├── event_study_analyzer.py # CAR/CAS calculations
├── pipeline_orchestrator.py # Pipeline coordination
├── database.py           # Database operations
└── resource_monitor.py   # Memory and performance monitoring
```

## Database Schema

### Core Tables

**instruments**
- ticker (PK): Stock ticker symbol
- name: Company name
- sector: Industry sector
- market_cap: Market capitalization
- listing_date: IPO date

**daily_prices**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- date: Trading date
- open, high, low, close: OHLC prices
- volume: Trading volume
- adjusted_close: Adjusted closing price

**analyst_recommendations**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- date: Recommendation date
- broker: Brokerage firm
- analyst: Analyst name
- rating: Standardized rating (1-5)
- rating_text: Original rating text
- target_price: Price target
- previous_rating: Previous rating for change detection

**daily_sentiment**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- date: Date
- bsi: Buy-Sell Imbalance (0-1)
- atr: Adjusted Turnover Ratio
- ltv: Log Trading Volume
- rsi: Relative Strength Index (0-100)
- pli: Psychological Line Index (0-1)
- sentiment_composite: PCA composite score
- sentiment_pure: Market-adjusted sentiment

**trading_signals**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- date: Signal date
- signal_type: Signal classification
- analyst_action: Upgrade/Downgrade/Initiate
- sentiment_score: Pure sentiment at signal time
- foreign_flow_score: Net Foreign Buy
- confidence: Signal confidence (0-1)
- notes: Additional context

**event_study_results**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- event_date: Recommendation change date
- event_window_start: Start of analysis window
- event_window_end: End of analysis window
- car: Cumulative Abnormal Return
- cas: Cumulative Abnormal Sentiment
- t_stat_car: T-statistic for CAR
- t_stat_cas: T-statistic for CAS

**pipeline_runs**
- id (PK): Auto-increment ID
- start_time: Pipeline start timestamp
- end_time: Pipeline end timestamp
- status: success/failed/running
- files_processed: Number of files processed
- records_inserted: Records added to database
- records_updated: Records modified
- errors: Error count
- error_details: JSON error log

**watchlist**
- id (PK): Auto-increment ID
- ticker (FK): References instruments
- added_at: Timestamp when added

**settings**
- key (PK): Setting name
- value: Setting value (JSON)
- updated_at: Last update timestamp

## API Endpoints

### Signals
- `GET /signals` - List all trading signals (with pagination)
- `GET /signals/{ticker}` - Get latest signal for a ticker

### Sentiment
- `GET /sentiment/{ticker}` - Get sentiment history for a ticker

### Event Study
- `GET /event-study/{ticker}/{date}` - Get event study results

### Data Management
- `GET /data-management/tables` - List all database tables
- `GET /data-management/tables/{table_name}` - Get table data with filtering
- `GET /data-management/instruments/{ticker}` - Get instrument details
- `GET /data-management/quality` - Get data quality metrics

### Pipeline
- `POST /pipeline/run` - Trigger pipeline execution
- `GET /pipeline/status/{run_id}` - Get pipeline run status
- `GET /pipeline/history` - Get pipeline execution history

### Settings
- `GET /settings` - Get signal thresholds
- `POST /settings` - Update signal thresholds

### Watchlist
- `GET /watchlist` - Get user's watchlist
- `POST /watchlist` - Add ticker to watchlist
- `DELETE /watchlist/{id}` - Remove from watchlist

### Export
- `GET /export/daily_signals.csv` - Export signals as CSV

## Data Pipeline Flow

1. **File Detection**: Scan `xlsx/` directory for new Excel files
2. **Schema Validation**: Verify file structure matches expected schema
3. **Data Loading**: Read Excel files into Pandas DataFrames
4. **Data Validation**: Check for missing values, outliers, duplicates
5. **Data Transformation**: Clean and standardize data
6. **Data Consolidation**: Merge data from multiple sources
7. **Sentiment Calculation**: Compute PCA composite sentiment
8. **Signal Generation**: Apply signal logic to generate trading signals
9. **Event Study Analysis**: Calculate CAR/CAS for recommendation changes
10. **Database Update**: Insert/update records in SQLite
11. **Audit Logging**: Record pipeline execution details

## Signal Generation Logic

### Contrarian Dip Buy
```python
if (analyst_action == "Downgrade" and 
    pure_sentiment > 1.0 and 
    net_foreign_buy > 0):
    return "Contrarian Dip Buy"
```

### Momentum Breakout
```python
if (analyst_action == "Upgrade" and 
    sentiment_slope > 0 and 
    rsi < 70):
    return "Momentum Breakout"
```

### Retail Trap
```python
if (analyst_action == "Downgrade" and 
    bsi > 0.5 and 
    net_foreign_buy < 0):
    return "Retail Trap"
```

### Neutral / No Edge
All other combinations that don't meet specific signal criteria.

## Theme System Implementation

The application supports dark and light modes using:

1. **ThemeContext**: React context for global theme state
2. **localStorage**: Persist user's theme preference
3. **Tailwind CSS**: Dark mode classes (`dark:bg-gray-900`)
4. **Inline Script**: Prevent flash of unstyled content (FOUC)

Theme initialization in `layout.tsx`:
```javascript
<script dangerouslySetInnerHTML={{
  __html: `
    try {
      const theme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.classList.add(theme);
    } catch (e) {}
  `
}} />
```

## Testing Strategy

### Backend Testing
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints end-to-end
- **Property-Based Tests**: Use Hypothesis for generative testing
- **Coverage Target**: 80%+ code coverage

### Frontend Testing
- **Component Tests**: Test React components in isolation
- **Integration Tests**: Test user flows
- **Linting**: ESLint for code quality

### Test Organization
```
tests/
├── unit/              # Unit tests
├── integration/       # Integration tests
└── property/          # Property-based tests
```

## Performance Considerations

1. **Database Indexing**: Indexes on ticker, date columns for fast queries
2. **Pagination**: API endpoints support limit/offset pagination
3. **Caching**: Frontend caches API responses
4. **Lazy Loading**: Charts and heavy components load on demand
5. **Resource Monitoring**: Track memory usage during pipeline execution

## Security Considerations

1. **CORS**: Configured to allow only localhost origins
2. **Input Validation**: Pydantic schemas validate all API inputs
3. **SQL Injection**: SQLAlchemy ORM prevents SQL injection
4. **XSS Protection**: React automatically escapes user input
5. **Error Handling**: Sensitive information not exposed in error messages

## Deployment

### Development
```bash
# Start both servers
manage.bat
# Select option 1
```

### Production Considerations
- Use PostgreSQL instead of SQLite for better concurrency
- Deploy backend with Gunicorn + Uvicorn workers
- Deploy frontend with Vercel or similar platform
- Use environment variables for configuration
- Implement proper logging and monitoring
- Set up automated backups
- Use HTTPS for all connections
