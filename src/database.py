"""
Database models and manager for SentimentAlpha Vietnam.
"""
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, BigInteger, 
    Date, DateTime, Text, ForeignKey, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import date, datetime
from typing import Optional
import pandas as pd

Base = declarative_base()


class Instrument(Base):
    """Instrument/Stock table."""
    __tablename__ = "instruments"
    
    ticker = Column(String, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    market_data = relationship("MarketData", back_populates="instrument")
    recommendations = relationship("AnalystRecommendation", back_populates="instrument")
    sentiment = relationship("DailySentiment", back_populates="instrument")
    signals = relationship("TradingSignal", back_populates="instrument")
    watchlist = relationship("Watchlist", back_populates="instrument")


class MarketData(Base):
    """Market data table."""
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey("instruments.ticker"))
    date = Column(Date)
    close_price = Column(Float)
    buy_volume = Column(BigInteger)
    sell_volume = Column(BigInteger)
    total_volume = Column(BigInteger)
    shares_outstanding = Column(BigInteger)
    
    __table_args__ = (UniqueConstraint('ticker', 'date', name='_ticker_date_uc'),)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="market_data")


class VNIndex(Base):
    """VNIndex benchmark data table."""
    __tablename__ = "vnindex"
    
    date = Column(Date, primary_key=True)
    close_index = Column(Float)
    buy_volume = Column(BigInteger)
    sell_volume = Column(BigInteger)
    total_volume = Column(BigInteger)


class RiskFreeRate(Base):
    """Risk-free rate table."""
    __tablename__ = "risk_free_rate"
    
    date = Column(Date, primary_key=True)
    rate = Column(Float)


class AnalystRecommendation(Base):
    """Analyst recommendations table."""
    __tablename__ = "analyst_recommendations"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey("instruments.ticker"))
    analyst_firm = Column(String)
    analyst_name = Column(String)
    recommendation = Column(String)
    rating_numeric = Column(Integer)
    target_price = Column(Float)
    issue_date = Column(Date)
    
    __table_args__ = (
        UniqueConstraint('ticker', 'analyst_firm', 'issue_date', name='_ticker_analyst_date_uc'),
    )
    
    # Relationships
    instrument = relationship("Instrument", back_populates="recommendations")
    signals = relationship("TradingSignal", back_populates="recommendation")


class DailySentiment(Base):
    """Daily sentiment table."""
    __tablename__ = "daily_sentiment"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey("instruments.ticker"))
    date = Column(Date)
    rsi = Column(Float)
    bsi = Column(Float)
    atr = Column(Float)
    ltv = Column(Float)
    pli = Column(Float)
    raw_sentiment = Column(Float)
    pure_sentiment = Column(Float)
    
    __table_args__ = (UniqueConstraint('ticker', 'date', name='_ticker_date_sentiment_uc'),)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="sentiment")


class TradingSignal(Base):
    """Trading signals table."""
    __tablename__ = "trading_signals"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey("instruments.ticker"))
    date = Column(Date)
    signal_type = Column(String)
    sentiment_score = Column(Float)
    foreign_flow_score = Column(Float)
    analyst_action = Column(String)
    recommendation_id = Column(Integer, ForeignKey("analyst_recommendations.id"))
    
    # Relationships
    instrument = relationship("Instrument", back_populates="signals")
    recommendation = relationship("AnalystRecommendation", back_populates="signals")


class Settings(Base):
    """Settings table."""
    __tablename__ = "settings"
    
    key = Column(String, primary_key=True)
    value = Column(Text)
    category = Column(String)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Watchlist(Base):
    """Watchlist table."""
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey("instruments.ticker"))
    added_at = Column(DateTime, default=func.now())
    
    # Relationships
    instrument = relationship("Instrument", back_populates="watchlist")


class PipelineRun(Base):
    """Tracks pipeline execution history."""
    __tablename__ = "pipeline_runs"
    
    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    status = Column(String)  # 'running', 'success', 'partial', 'failed'
    files_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    error_details = Column(Text)  # JSON array of error messages


class DataQualityMetric(Base):
    """Stores data quality metrics per table."""
    __tablename__ = "data_quality_metrics"
    
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    metric_date = Column(Date)
    total_records = Column(Integer)
    null_count = Column(Integer)
    completeness_pct = Column(Float)
    anomaly_count = Column(Integer)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DatabaseManager:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize DatabaseManager.
        
        Args:
            db_path: Path to SQLite database file (defaults to DATABASE_PATH env var or 'sentimentalpha.db')
        """
        import os
        if db_path is None:
            db_path = os.getenv("DATABASE_PATH", "sentimentalpha.db")
        
        # Create engine with connection pooling limits to prevent leaks
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            pool_size=5,  # Maximum number of connections to keep open
            max_overflow=5,  # Maximum number of connections to create beyond pool_size
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            connect_args={
                "check_same_thread": False,
                "timeout": 30  # 30 second timeout for lock acquisition
            }
        )
        self.Session = sessionmaker(bind=self.engine)
    
    def dispose(self) -> None:
        """
        Dispose of the connection pool and close all connections.
        Call this when done with the DatabaseManager to prevent leaks.
        """
        if hasattr(self, 'engine'):
            self.engine.dispose()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup."""
        self.dispose()
        return False
    
    def create_tables(self) -> None:
        """Create all database tables."""
        Base.metadata.create_all(self.engine)
    
    def upsert_market_data(self, df: pd.DataFrame, batch_size: int = 10000) -> int:
        """
        Insert or update market data using bulk operations for better performance.
        
        Args:
            df: DataFrame with columns: date, ticker, close_price, buy_volume,
                sell_volume, total_volume, shares_outstanding
            batch_size: Number of records to process in each batch
                
        Returns:
            Count of new records inserted
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # Clean the dataframe first
        df_clean = df.dropna(subset=['ticker', 'date']).copy()
        
        # Helper functions
        def safe_float(val):
            return None if pd.isna(val) else float(val)
        
        def safe_int(val):
            return None if pd.isna(val) else int(val)
        
        # Convert data types
        df_clean['close_price'] = df_clean.get('close_price', pd.Series()).apply(safe_float)
        df_clean['buy_volume'] = df_clean.get('buy_volume', pd.Series()).apply(safe_int)
        df_clean['sell_volume'] = df_clean.get('sell_volume', pd.Series()).apply(safe_int)
        df_clean['total_volume'] = df_clean.get('total_volume', pd.Series()).apply(safe_int)
        df_clean['shares_outstanding'] = df_clean.get('shares_outstanding', pd.Series()).apply(safe_int)
        
        session = self.Session()
        new_count = 0
        
        try:
            # First, ensure all instruments exist
            unique_tickers = df_clean['ticker'].unique()
            logger.info(f"Ensuring {len(unique_tickers)} instruments exist...")
            
            existing_tickers = set(
                ticker[0] for ticker in session.query(Instrument.ticker).all()
            )
            
            new_instruments = [
                Instrument(ticker=ticker) 
                for ticker in unique_tickers 
                if ticker not in existing_tickers
            ]
            
            if new_instruments:
                session.bulk_save_objects(new_instruments)
                session.commit()
                logger.info(f"Created {len(new_instruments)} new instruments")
            
            # Process market data in batches
            total_rows = len(df_clean)
            logger.info(f"Processing {total_rows} market data records in batches of {batch_size}...")
            
            for i in range(0, total_rows, batch_size):
                batch_df = df_clean.iloc[i:i+batch_size]
                logger.info(f"Processing batch {i//batch_size + 1}/{(total_rows-1)//batch_size + 1} ({len(batch_df)} records)")
                
                # Use pandas to_sql with if_exists='replace' for much faster insertion
                # But first check for existing records to avoid duplicates
                batch_records = []
                
                for _, row in batch_df.iterrows():
                    # Check if record exists (this is still slow but necessary for upsert)
                    existing = session.query(MarketData).filter_by(
                        ticker=row['ticker'],
                        date=row['date']
                    ).first()
                    
                    if not existing:
                        batch_records.append(MarketData(
                            ticker=row['ticker'],
                            date=row['date'],
                            close_price=row['close_price'],
                            buy_volume=row['buy_volume'],
                            sell_volume=row['sell_volume'],
                            total_volume=row['total_volume'],
                            shares_outstanding=row['shares_outstanding']
                        ))
                        new_count += 1
                
                # Bulk insert new records
                if batch_records:
                    session.bulk_save_objects(batch_records)
                    session.commit()
                    logger.info(f"Inserted {len(batch_records)} new records in this batch")
            
            logger.info(f"Total new records inserted: {new_count}")
            return new_count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error during market data upsert: {e}")
            raise e
        finally:
            session.close()
    
    def upsert_recommendations(self, df: pd.DataFrame) -> int:
        """
        Insert or update recommendations.
        
        Args:
            df: DataFrame with columns: Ticker, Comp name, Analyst, Recommendation,
                rating_numeric, Target price, Issue date
                
        Returns:
            Count of new records inserted
        """
        session = self.Session()
        new_count = 0
        
        try:
            for _, row in df.iterrows():
                # Skip rows with null ticker or issue_date
                if pd.isna(row.get('Ticker')) or pd.isna(row.get('Issue date')):
                    continue
                
                # Ensure instrument exists
                instrument = session.query(Instrument).filter_by(ticker=row['Ticker']).first()
                if not instrument:
                    instrument = Instrument(
                        ticker=row['Ticker'],
                        name=row.get('Comp name') if not pd.isna(row.get('Comp name')) else None
                    )
                    session.add(instrument)
                    session.flush()
                
                # Get analyst firm (handle NaN)
                analyst_firm = row.get('Analyst', '')
                if pd.isna(analyst_firm):
                    analyst_firm = ''
                
                # Check if recommendation already exists
                existing = session.query(AnalystRecommendation).filter_by(
                    ticker=row['Ticker'],
                    analyst_firm=analyst_firm,
                    issue_date=row['Issue date']
                ).first()
                
                # Handle nullable numeric fields properly
                rating_numeric = row.get('rating_numeric')
                if pd.isna(rating_numeric):
                    rating_numeric = None
                else:
                    # Convert to int if not None
                    rating_numeric = int(rating_numeric)
                
                target_price = row.get('Target price')
                if pd.isna(target_price):
                    target_price = None
                else:
                    target_price = float(target_price)
                
                if existing:
                    # Update existing record
                    existing.analyst_name = row.get('Analyst') if not pd.isna(row.get('Analyst')) else None
                    existing.recommendation = row.get('Recommendation') if not pd.isna(row.get('Recommendation')) else None
                    existing.rating_numeric = rating_numeric
                    existing.target_price = target_price
                else:
                    # Insert new record
                    recommendation = AnalystRecommendation(
                        ticker=row['Ticker'],
                        analyst_firm=analyst_firm,
                        analyst_name=row.get('Analyst') if not pd.isna(row.get('Analyst')) else None,
                        recommendation=row.get('Recommendation') if not pd.isna(row.get('Recommendation')) else None,
                        rating_numeric=rating_numeric,
                        target_price=target_price,
                        issue_date=row['Issue date']
                    )
                    session.add(recommendation)
                    new_count += 1
            
            session.commit()
            return new_count
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_latest_date(self, table: str) -> Optional[date]:
        """
        Get most recent date in table for incremental updates.
        
        Args:
            table: Table name ('market_data', 'vnindex', 'risk_free_rate', etc.)
            
        Returns:
            Most recent date or None if table is empty
        """
        session = self.Session()
        
        try:
            if table == 'market_data':
                result = session.query(func.max(MarketData.date)).scalar()
            elif table == 'vnindex':
                result = session.query(func.max(VNIndex.date)).scalar()
            elif table == 'risk_free_rate':
                result = session.query(func.max(RiskFreeRate.date)).scalar()
            elif table == 'daily_sentiment':
                result = session.query(func.max(DailySentiment.date)).scalar()
            elif table == 'analyst_recommendations':
                result = session.query(func.max(AnalystRecommendation.issue_date)).scalar()
            else:
                raise ValueError(f"Unknown table: {table}")
            
            return result
        finally:
            session.close()
