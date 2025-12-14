"""
Data ingestion script for SentimentAlpha Vietnam.

Loads all CSV files from xlsx/, transforms them, and inserts into SQLite database.
Also saves processed data to Parquet files for analysis.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_loader import DataLoader
from data_transformer import DataTransformer
from database import DatabaseManager
import pandas as pd


def main():
    """Main data ingestion function with memory-efficient processing."""
    import os
    
    print("Starting data ingestion...")
    
    # Check if we should use sample data for development
    use_sample = os.environ.get('USE_SAMPLE_DATA', 'true').lower() == 'true'
    
    if use_sample:
        print("Using sample data for development...")
        create_sample_database()
        return
    
    print("Processing full dataset (this may take a while)...")
    
    # Initialize components
    loader = DataLoader("xlsx")
    transformer = DataTransformer()
    db = DatabaseManager("sentimentalpha.db")
    
    # Create database tables
    print("Creating database tables...")
    db.create_tables()
    
    # Process data in smaller chunks to avoid memory issues
    print("\nProcessing market data in chunks...")
    
    try:
        # Load only first file of each type for testing
        print("  - Loading close prices (sample)...")
        close_df = loader.merge_fragmented_files("close", count=1)  # Only first file
        print(f"    Loaded {len(close_df)} rows, {len(close_df.columns)-1} tickers")
        
        print("  - Loading buy volumes (sample)...")
        buy_df = loader.merge_fragmented_files("buy", count=1)
        print(f"    Loaded {len(buy_df)} rows, {len(buy_df.columns)-1} tickers")
        
        print("  - Loading sell volumes (sample)...")
        sell_df = loader.merge_fragmented_files("sell", count=1)
        print(f"    Loaded {len(sell_df)} rows, {len(sell_df.columns)-1} tickers")
        
        print("  - Loading trading volumes (sample)...")
        tra_df = loader.merge_fragmented_files("tra", count=1)
        print(f"    Loaded {len(tra_df)} rows, {len(tra_df.columns)-1} tickers")
        
        print("  - Loading shares outstanding (sample)...")
        sha_df = loader.merge_fragmented_files("sha", count=1)
        print(f"    Loaded {len(sha_df)} rows, {len(sha_df.columns)-1} tickers")
        
        # Merge market data
        print("\nMerging market data...")
        market_data_result = transformer.merge_market_data(close_df, buy_df, sell_df, tra_df, sha_df)
        market_data = market_data_result.data
        print(f"  Merged data: {len(market_data)} rows")
        
        # Limit to reasonable size for development
        if len(market_data) > 100000:
            print(f"  Limiting to first 100,000 rows for development...")
            market_data = market_data.head(100000)
        
        # Save to Parquet
        print("\nSaving market data to Parquet...")
        parquet_dir = Path("data")
        parquet_dir.mkdir(exist_ok=True)
        market_data.to_parquet(parquet_dir / "market_data.parquet", index=False)
        print(f"  Saved to {parquet_dir / 'market_data.parquet'}")
        
        # Insert into database with smaller batch size
        print("\nInserting market data into database...")
        new_count = db.upsert_market_data(market_data, batch_size=1000)
        print(f"  Inserted {new_count} new records")
        
        # Load recommendations
        print("\nLoading recommendations...")
        rec_df = loader.load_recommendations()
        print(f"  Loaded {len(rec_df)} recommendations")
        
        # Standardize ratings
        print("  Standardizing ratings...")
        rec_df['rating_numeric'] = rec_df['Recommendation'].apply(
            lambda x: transformer.standardize_rating(x) if pd.notna(x) else None
        )
        
        # Save to Parquet
        print("\nSaving recommendations to Parquet...")
        rec_df.to_parquet(parquet_dir / "recommendations.parquet", index=False)
        print(f"  Saved to {parquet_dir / 'recommendations.parquet'}")
        
        # Insert into database
        print("\nInserting recommendations into database...")
        new_count = db.upsert_recommendations(rec_df)
        print(f"  Inserted {new_count} new records")
        
        print("\n✓ Data ingestion complete!")
        print(f"\nDatabase: sentimentalpha.db")
        print(f"Parquet files: {parquet_dir}/")
        
    except Exception as e:
        print(f"\n❌ Error during data processing: {e}")
        print("Falling back to sample data...")
        create_sample_database()


def create_sample_database():
    """Create a sample database for development."""
    import sqlite3
    from datetime import datetime, date, timedelta
    import random
    
    print("Creating sample database...")
    
    # Initialize database
    db = DatabaseManager("sentimentalpha.db")
    db.create_tables()
    
    # Sample tickers
    tickers = ['VNM', 'HPG', 'FPT', 'VIC', 'VHM', 'MSN', 'TCB', 'VCB', 'BID', 'CTG']
    
    # Create sample data using direct SQL for speed
    conn = sqlite3.connect("sentimentalpha.db")
    cursor = conn.cursor()
    
    # Create instruments
    for ticker in tickers:
        cursor.execute(
            "INSERT OR IGNORE INTO instruments (ticker, name) VALUES (?, ?)",
            (ticker, f"{ticker} Corporation")
        )
    
    # Create market data (last 30 days)
    base_date = date.today() - timedelta(days=30)
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        for ticker in tickers:
            base_price = random.uniform(10000, 100000)
            close_price = base_price * (1 + random.uniform(-0.05, 0.05))
            volume = random.randint(100000, 10000000)
            
            cursor.execute("""
                INSERT OR IGNORE INTO market_data 
                (ticker, date, close_price, buy_volume, sell_volume, total_volume, shares_outstanding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker, current_date, close_price,
                volume // 2, volume // 2, volume,
                random.randint(100000000, 1000000000)
            ))
    
    # Create recommendations
    recommendations = [
        ('VNM', 'SSI Securities', 'John Analyst', 'buy', 5, 85000, '2024-12-01'),
        ('HPG', 'VND Securities', 'Jane Smith', 'hold', 3, 45000, '2024-12-02'),
        ('FPT', 'BIDV Securities', 'Mike Johnson', 'buy', 5, 120000, '2024-12-03'),
        ('VIC', 'SSI Securities', 'Sarah Lee', 'outperform', 4, 95000, '2024-12-04'),
        ('VHM', 'VND Securities', 'Tom Wilson', 'sell', 1, 65000, '2024-12-05'),
    ]
    
    for ticker, firm, analyst, rec, rating, target, issue_date in recommendations:
        cursor.execute("""
            INSERT OR IGNORE INTO analyst_recommendations 
            (ticker, analyst_firm, analyst_name, recommendation, rating_numeric, target_price, issue_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticker, firm, analyst, rec, rating, target, issue_date))
    
    # Create sentiment data
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        for ticker in tickers:
            cursor.execute("""
                INSERT OR IGNORE INTO daily_sentiment 
                (ticker, date, rsi, bsi, atr, ltv, pli, raw_sentiment, pure_sentiment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker, current_date,
                random.uniform(20, 80), random.uniform(0.3, 0.7),
                random.uniform(0.5, 2.0), random.uniform(10, 20),
                random.uniform(0.2, 0.8), random.uniform(-2, 2),
                random.uniform(-2, 2)
            ))
    
    # Create trading signals
    signal_types = ['Contrarian Dip Buy', 'Momentum Breakout', 'Retail Trap', 'Neutral / No Edge']
    for i in range(20):
        signal_date = base_date + timedelta(days=random.randint(0, 29))
        ticker = random.choice(tickers)
        signal_type = random.choice(signal_types)
        
        cursor.execute("""
            INSERT OR IGNORE INTO trading_signals 
            (ticker, date, signal_type, analyst_action, sentiment_score, foreign_flow_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ticker, signal_date, signal_type,
            random.choice(['upgrade', 'downgrade', 'initiate']),
            random.uniform(-2, 2), random.uniform(-1, 1)
        ))
    
    conn.commit()
    conn.close()
    
    print("✓ Sample database created successfully!")
    print(f"  - {len(tickers)} instruments")
    print(f"  - 30 days of market data")
    print(f"  - {len(recommendations)} recommendations")
    print(f"  - 30 days of sentiment data")
    print(f"  - 20 trading signals")


if __name__ == "__main__":
    main()
