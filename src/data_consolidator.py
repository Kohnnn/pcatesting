"""
Data Consolidation Module for SentimentAlpha Vietnam.

Provides robust data structure and merging strategy for CSV files:
- Handles all CSV files in the xlsx directory
- Supports incremental data updates (pushing new data without full reprocessing)
- Maintains data integrity across merges
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
import logging

from src.data_loader import DataLoader
from src.data_transformer import DataTransformer
from src.database import DatabaseManager

logger = logging.getLogger(__name__)


class DataConsolidator:
    """
    Consolidates and manages CSV data files with incremental update support.
    """
    
    def __init__(
        self,
        data_dir: Optional[str] = None,
        db_manager: Optional[DatabaseManager] = None
    ):
        """
        Initialize DataConsolidator.
        
        Args:
            data_dir: Directory containing CSV files
            db_manager: DatabaseManager instance for database operations
        """
        self.loader = DataLoader(data_dir)
        self.transformer = DataTransformer()
        self.db = db_manager or DatabaseManager()
        self.data_dir = Path(data_dir or "xlsx")
    
    def consolidate_market_data(
        self,
        incremental: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Consolidate all market data CSV files into a single DataFrame.
        
        Handles fragmented files (buy1-9, sell1-9, etc.) and merges them
        into a unified market data structure.
        
        Args:
            incremental: If True, only return data newer than latest in database
            
        Returns:
            Tuple of (consolidated DataFrame, statistics dict)
        """
        stats = {
            'files_processed': 0,
            'total_records': 0,
            'new_records': 0,
            'errors': 0
        }
        
        try:
            # Load and merge fragmented files
            logger.info("Loading market data files...")
            
            close_df = self.loader.merge_fragmented_files('close', count=9)
            stats['files_processed'] += 9
            
            buy_df = self.loader.merge_fragmented_files('buy', count=9)
            stats['files_processed'] += 9
            
            sell_df = self.loader.merge_fragmented_files('sell', count=9)
            stats['files_processed'] += 9
            
            tra_df = self.loader.merge_fragmented_files('tra', count=9)
            stats['files_processed'] += 9
            
            sha_df = self.loader.merge_fragmented_files('sha', count=9)
            stats['files_processed'] += 9
            
            # Transform and merge
            logger.info("Transforming and merging market data...")
            result = self.transformer.merge_market_data(
                close_df=close_df,
                buy_df=buy_df,
                sell_df=sell_df,
                tra_df=tra_df,
                sha_df=sha_df,
                validate=True
            )
            
            merged_df = result.data
            stats['total_records'] = len(merged_df)
            stats['errors'] = len(result.errors)
            
            # Filter for incremental update if requested
            if incremental:
                latest_date = self.db.get_latest_date('market_data')
                if latest_date:
                    merged_df = merged_df[merged_df['date'] > pd.Timestamp(latest_date)]
                    logger.info(f"Filtered to records after {latest_date}")
            
            stats['new_records'] = len(merged_df)
            
            return merged_df, stats
            
        except Exception as e:
            logger.error(f"Error consolidating market data: {str(e)}")
            stats['errors'] += 1
            raise
    
    def consolidate_recommendations(
        self,
        incremental: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Consolidate analyst recommendations with rating standardization.
        
        Args:
            incremental: If True, only return data newer than latest in database
            
        Returns:
            Tuple of (consolidated DataFrame, statistics dict)
        """
        stats = {
            'files_processed': 0,
            'total_records': 0,
            'new_records': 0,
            'errors': 0
        }
        
        try:
            # Load recommendations
            logger.info("Loading recommendations...")
            df = self.loader.load_recommendations()
            stats['files_processed'] = 1
            stats['total_records'] = len(df)
            
            # Standardize ratings
            logger.info("Standardizing ratings...")
            result = self.transformer.standardize_ratings_batch(
                df, rating_column='Recommendation'
            )
            
            df_with_ratings = result.data
            stats['errors'] = len(result.errors)
            
            # Filter for incremental update if requested
            if incremental:
                latest_date = self.db.get_latest_date('analyst_recommendations')
                if latest_date and 'issue date' in df_with_ratings.columns:
                    df_with_ratings = df_with_ratings[
                        df_with_ratings['issue date'] > pd.Timestamp(latest_date)
                    ]
                    logger.info(f"Filtered to records after {latest_date}")
            
            stats['new_records'] = len(df_with_ratings)
            
            return df_with_ratings, stats
            
        except Exception as e:
            logger.error(f"Error consolidating recommendations: {str(e)}")
            stats['errors'] += 1
            raise
    
    def consolidate_vnindex(
        self,
        incremental: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Consolidate VNIndex benchmark data.
        
        Args:
            incremental: If True, only return data newer than latest in database
            
        Returns:
            Tuple of (consolidated DataFrame, statistics dict)
        """
        stats = {
            'files_processed': 0,
            'total_records': 0,
            'new_records': 0,
            'errors': 0
        }
        
        try:
            # Load VNIndex
            logger.info("Loading VNIndex data...")
            df = self.loader.load_vnindex()
            stats['files_processed'] = 1
            stats['total_records'] = len(df)
            
            # Filter for incremental update if requested
            if incremental:
                latest_date = self.db.get_latest_date('vnindex')
                if latest_date and 'Date' in df.columns:
                    df = df[df['Date'] > pd.Timestamp(latest_date)]
                    logger.info(f"Filtered to records after {latest_date}")
            
            stats['new_records'] = len(df)
            
            return df, stats
            
        except Exception as e:
            logger.error(f"Error consolidating VNIndex: {str(e)}")
            stats['errors'] += 1
            raise
    
    def consolidate_risk_free_rate(
        self,
        incremental: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Consolidate risk-free rate data.
        
        Args:
            incremental: If True, only return data newer than latest in database
            
        Returns:
            Tuple of (consolidated DataFrame, statistics dict)
        """
        stats = {
            'files_processed': 0,
            'total_records': 0,
            'new_records': 0,
            'errors': 0
        }
        
        try:
            # Load risk-free rate
            logger.info("Loading risk-free rate data...")
            df = self.loader.load_risk_free_rate()
            stats['files_processed'] = 1
            stats['total_records'] = len(df)
            
            # Filter for incremental update if requested
            if incremental:
                latest_date = self.db.get_latest_date('risk_free_rate')
                if latest_date and 'Date' in df.columns:
                    df = df[df['Date'] > pd.Timestamp(latest_date)]
                    logger.info(f"Filtered to records after {latest_date}")
            
            stats['new_records'] = len(df)
            
            return df, stats
            
        except Exception as e:
            logger.error(f"Error consolidating risk-free rate: {str(e)}")
            stats['errors'] += 1
            raise
    
    def consolidate_all(
        self,
        incremental: bool = True
    ) -> Dict[str, Dict[str, int]]:
        """
        Consolidate all data sources and load to database.
        
        Args:
            incremental: If True, only process new data
            
        Returns:
            Dictionary with statistics for each data source
        """
        all_stats = {}
        
        # Market data
        try:
            market_df, market_stats = self.consolidate_market_data(incremental)
            if not market_df.empty:
                self.db.upsert_market_data(market_df)
            all_stats['market_data'] = market_stats
        except Exception as e:
            logger.error(f"Failed to consolidate market data: {str(e)}")
            all_stats['market_data'] = {'error': str(e)}
        
        # Recommendations
        try:
            rec_df, rec_stats = self.consolidate_recommendations(incremental)
            if not rec_df.empty:
                # Rename columns to match database expectations
                rec_df = rec_df.rename(columns={
                    'ticker': 'Ticker',
                    'comp name': 'Comp name',
                    'analyst': 'Analyst',
                    'recommendation': 'Recommendation',
                    'target price': 'Target price',
                    'issue date': 'Issue date'
                })
                self.db.upsert_recommendations(rec_df)
            all_stats['recommendations'] = rec_stats
        except Exception as e:
            logger.error(f"Failed to consolidate recommendations: {str(e)}")
            all_stats['recommendations'] = {'error': str(e)}
        
        # VNIndex
        try:
            vnindex_df, vnindex_stats = self.consolidate_vnindex(incremental)
            if not vnindex_df.empty:
                # Insert VNIndex data
                session = self.db.Session()
                try:
                    from src.database import VNIndex
                    for _, row in vnindex_df.iterrows():
                        vnindex = VNIndex(
                            date=row['Date'].date() if hasattr(row['Date'], 'date') else row['Date'],
                            close_index=row.get('close_index'),
                            buy_volume=row.get('buy_volume'),
                            sell_volume=row.get('sell_volume'),
                            total_volume=row.get('total_volume')
                        )
                        session.merge(vnindex)
                    session.commit()
                finally:
                    session.close()
            all_stats['vnindex'] = vnindex_stats
        except Exception as e:
            logger.error(f"Failed to consolidate VNIndex: {str(e)}")
            all_stats['vnindex'] = {'error': str(e)}
        
        # Risk-free rate
        try:
            rfr_df, rfr_stats = self.consolidate_risk_free_rate(incremental)
            if not rfr_df.empty:
                # Insert risk-free rate data
                session = self.db.Session()
                try:
                    from src.database import RiskFreeRate
                    for _, row in rfr_df.iterrows():
                        rfr = RiskFreeRate(
                            date=row['Date'].date() if hasattr(row['Date'], 'date') else row['Date'],
                            rate=row.get('rate')
                        )
                        session.merge(rfr)
                    session.commit()
                finally:
                    session.close()
            all_stats['risk_free_rate'] = rfr_stats
        except Exception as e:
            logger.error(f"Failed to consolidate risk-free rate: {str(e)}")
            all_stats['risk_free_rate'] = {'error': str(e)}
        
        return all_stats
