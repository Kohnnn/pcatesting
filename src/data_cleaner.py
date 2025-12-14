"""
Comprehensive Data Cleaning and Consolidation Script for SentimentAlpha Vietnam.

Handles:
- Ticker symbol standardization and validation
- Missing/incorrect price and market data detection and handling
- Data quality flagging and reporting
- Clean consolidated dataset output for signal detection
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import logging
import re
import json

logger = logging.getLogger(__name__)

# Vietnam stock exchange ticker patterns
HOSE_PATTERN = re.compile(r'^[A-Z]{3}$')  # 3-letter tickers for HOSE
HNX_PATTERN = re.compile(r'^[A-Z]{3,4}$')  # 3-4 letter tickers for HNX
UPCOM_PATTERN = re.compile(r'^[A-Z0-9]{3,6}$')  # More flexible for UPCOM

# Known ticker corrections mapping
TICKER_CORRECTIONS = {
    # Common misspellings and variations
    'VNM ': 'VNM',
    ' VNM': 'VNM',
    'VNM.': 'VNM',
    'HPG ': 'HPG',
    'FPT ': 'FPT',
    'VIC ': 'VIC',
    'VHM ': 'VHM',
    'MSN ': 'MSN',
    'TCB ': 'TCB',
    'VCB ': 'VCB',
    'BID ': 'BID',
    'CTG ': 'CTG',
    'MBB ': 'MBB',
    'ACB ': 'ACB',
    'VPB ': 'VPB',
    'STB ': 'STB',
    'HDB ': 'HDB',
    'TPB ': 'TPB',
    'SSI ': 'SSI',
    'VND ': 'VND',
    'HCM ': 'HCM',
}

# Valid Vietnam stock tickers (partial list - top 100 by market cap)
VALID_TICKERS = {
    'AAA', 'AAM', 'AAT', 'ABR', 'ABS', 'ABT', 'ACB', 'ACC', 'ACG', 'ACL',
    'ADG', 'ADP', 'ADS', 'AGG', 'AGR', 'ANV', 'APG', 'APH', 'ASG', 'ASM',
    'ASP', 'AST', 'ATP', 'BAF', 'BBC', 'BCE', 'BCG', 'BCM', 'BFC', 'BHN',
    'BIC', 'BID', 'BKG', 'BMC', 'BMI', 'BMP', 'BRC', 'BSI', 'BSR', 'BTP',
    'BTT', 'BVH', 'BWE', 'C32', 'C47', 'CCC', 'CCI', 'CCL', 'CDC', 'CHP',
    'CIG', 'CII', 'CKG', 'CLC', 'CLL', 'CLW', 'CMG', 'CMV', 'CMX', 'CNG',
    'COM', 'CRC', 'CRE', 'CRV', 'CSM', 'CSV', 'CTD', 'CTF', 'CTG', 'CTI',
    'CTR', 'CTS', 'CVT', 'D2D', 'DAH', 'DAT', 'DBC', 'DBD', 'DBT', 'DC4',
    'DCL', 'DCM', 'DGC', 'DGW', 'DHA', 'DHC', 'DHG', 'DHM', 'DIG', 'DLG',
    'DMC', 'DPG', 'DPM', 'DPR', 'DQC', 'DRC', 'DRH', 'DRL', 'DSC', 'DSE',
    'FPT', 'GAS', 'GEX', 'GMD', 'GVR', 'HAG', 'HBC', 'HCM', 'HDB', 'HDC',
    'HDG', 'HHS', 'HNG', 'HPG', 'HQC', 'HSG', 'HT1', 'HVN', 'IJC', 'IMP',
    'KBC', 'KDC', 'KDH', 'KSB', 'LCG', 'LGC', 'LPB', 'MBB', 'MCG', 'MIG',
    'MSB', 'MSN', 'MWG', 'NAF', 'NKG', 'NLG', 'NTL', 'NVL', 'OCB', 'OGC',
    'PAN', 'PC1', 'PDR', 'PHR', 'PLC', 'PLX', 'PNJ', 'POW', 'PPC', 'PTB',
    'PVD', 'PVS', 'PVT', 'QCG', 'REE', 'SAB', 'SBT', 'SCS', 'SHB', 'SHS',
    'SIP', 'SJS', 'SSB', 'SSI', 'STB', 'SZC', 'TCB', 'TCH', 'TDM', 'THG',
    'TLG', 'TNG', 'TPB', 'VCB', 'VCG', 'VCI', 'VGC', 'VHC', 'VHM', 'VIB',
    'VIC', 'VIX', 'VJC', 'VND', 'VNM', 'VOS', 'VPB', 'VPI', 'VRE', 'VSC',
    'VSH', 'VTP', 'YEG',
}


class DataQualityReport:
    """Container for data quality metrics and issues."""
    
    def __init__(self):
        self.total_records = 0
        self.valid_records = 0
        self.invalid_tickers: List[str] = []
        self.corrected_tickers: Dict[str, str] = {}
        self.missing_prices: int = 0
        self.missing_volumes: int = 0
        self.flagged_records: List[Dict] = []
        self.outliers_detected: int = 0
        self.date_issues: int = 0
        self.duplicate_records: int = 0
        
    def to_dict(self) -> Dict:
        return {
            'total_records': self.total_records,
            'valid_records': self.valid_records,
            'invalid_tickers': self.invalid_tickers[:50],  # Limit for readability
            'corrected_tickers': dict(list(self.corrected_tickers.items())[:50]),
            'missing_prices': self.missing_prices,
            'missing_volumes': self.missing_volumes,
            'flagged_records_count': len(self.flagged_records),
            'outliers_detected': self.outliers_detected,
            'date_issues': self.date_issues,
            'duplicate_records': self.duplicate_records,
            'data_quality_score': self._calculate_quality_score()
        }
    
    def _calculate_quality_score(self) -> float:
        """Calculate overall data quality score (0-100)."""
        if self.total_records == 0:
            return 0.0
        
        issues = (
            len(self.invalid_tickers) +
            self.missing_prices +
            self.missing_volumes +
            self.outliers_detected +
            self.date_issues +
            self.duplicate_records
        )
        
        score = max(0, 100 - (issues / self.total_records * 100))
        return round(score, 2)


class DataCleaner:
    """
    Comprehensive data cleaning and validation for Vietnam stock market data.
    """
    
    def __init__(self, data_dir: str = "xlsx"):
        self.data_dir = Path(data_dir)
        self.report = DataQualityReport()
        
    def standardize_ticker(self, ticker: str) -> Tuple[str, bool, Optional[str]]:
        """
        Standardize ticker symbol.
        
        Returns:
            Tuple of (standardized_ticker, is_valid, correction_note)
        """
        if pd.isna(ticker) or ticker is None:
            return '', False, 'Missing ticker'
        
        # Convert to string and clean
        ticker_str = str(ticker).strip().upper()
        
        # Apply known corrections
        if ticker_str in TICKER_CORRECTIONS:
            corrected = TICKER_CORRECTIONS[ticker_str]
            return corrected, True, f'Corrected from {ticker_str}'
        
        # Remove common suffixes/prefixes
        ticker_str = re.sub(r'[.\s]+$', '', ticker_str)
        ticker_str = re.sub(r'^[.\s]+', '', ticker_str)
        
        # Validate format
        if not ticker_str:
            return '', False, 'Empty ticker after cleaning'
        
        # Check against known valid tickers
        if ticker_str in VALID_TICKERS:
            return ticker_str, True, None
        
        # Check pattern validity
        if HOSE_PATTERN.match(ticker_str) or HNX_PATTERN.match(ticker_str):
            # Valid pattern but not in our known list - flag for review
            return ticker_str, True, 'Valid pattern, not in known list'
        
        return ticker_str, False, f'Invalid ticker format: {ticker_str}'
    
    def validate_price(self, price: float, ticker: str = '') -> Tuple[float, bool, Optional[str]]:
        """
        Validate and clean price data.
        
        Returns:
            Tuple of (cleaned_price, is_valid, flag_reason)
        """
        if pd.isna(price) or price is None:
            return np.nan, False, 'Missing price'
        
        try:
            price_val = float(price)
        except (ValueError, TypeError):
            return np.nan, False, f'Invalid price format: {price}'
        
        # Vietnam stock prices are typically in VND (1,000 - 500,000 range)
        if price_val <= 0:
            return np.nan, False, 'Non-positive price'
        
        if price_val < 100:
            # Might be in thousands, flag for review
            return price_val, True, 'Unusually low price - verify units'
        
        if price_val > 1000000:
            # Unusually high, might be data error
            return price_val, True, 'Unusually high price - verify'
        
        return price_val, True, None
    
    def validate_volume(self, volume: float) -> Tuple[float, bool, Optional[str]]:
        """
        Validate and clean volume data.
        
        Returns:
            Tuple of (cleaned_volume, is_valid, flag_reason)
        """
        if pd.isna(volume) or volume is None:
            return np.nan, False, 'Missing volume'
        
        try:
            vol_val = float(volume)
        except (ValueError, TypeError):
            return np.nan, False, f'Invalid volume format: {volume}'
        
        if vol_val < 0:
            return np.nan, False, 'Negative volume'
        
        if vol_val == 0:
            return 0.0, True, 'Zero volume - no trading'
        
        return vol_val, True, None
    
    def detect_outliers(self, df: pd.DataFrame, column: str, n_std: float = 3.0) -> pd.Series:
        """
        Detect outliers using z-score method.
        
        Returns:
            Boolean series indicating outliers
        """
        if column not in df.columns:
            return pd.Series([False] * len(df))
        
        values = df[column].dropna()
        if len(values) < 10:
            return pd.Series([False] * len(df))
        
        mean = values.mean()
        std = values.std()
        
        if std == 0:
            return pd.Series([False] * len(df))
        
        z_scores = np.abs((df[column] - mean) / std)
        return z_scores > n_std

    def fill_missing_prices(
        self,
        df: pd.DataFrame,
        price_col: str = 'close',
        method: str = 'ffill'
    ) -> pd.DataFrame:
        """
        Fill missing price data using specified method.
        
        Args:
            df: DataFrame with price data
            price_col: Column name for prices
            method: 'ffill' (forward fill), 'bfill' (backward fill), 
                   'interpolate', or 'mean'
        
        Returns:
            DataFrame with filled prices
        """
        df = df.copy()
        
        if price_col not in df.columns:
            return df
        
        if method == 'ffill':
            df[price_col] = df.groupby('ticker')[price_col].ffill()
        elif method == 'bfill':
            df[price_col] = df.groupby('ticker')[price_col].bfill()
        elif method == 'interpolate':
            df[price_col] = df.groupby('ticker')[price_col].transform(
                lambda x: x.interpolate(method='linear')
            )
        elif method == 'mean':
            df[price_col] = df.groupby('ticker')[price_col].transform(
                lambda x: x.fillna(x.mean())
            )
        
        return df
    
    def clean_market_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, DataQualityReport]:
        """
        Clean and validate market data DataFrame.
        
        Args:
            df: Raw market data DataFrame
            
        Returns:
            Tuple of (cleaned DataFrame, quality report)
        """
        report = DataQualityReport()
        report.total_records = len(df)
        
        df = df.copy()
        
        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Clean ticker symbols
        if 'ticker' in df.columns:
            cleaned_tickers = []
            for ticker in df['ticker']:
                std_ticker, is_valid, note = self.standardize_ticker(ticker)
                cleaned_tickers.append(std_ticker)
                
                if not is_valid:
                    report.invalid_tickers.append(str(ticker))
                elif note and 'Corrected' in note:
                    report.corrected_tickers[str(ticker)] = std_ticker
            
            df['ticker'] = cleaned_tickers
            df['ticker_valid'] = df['ticker'].apply(lambda x: x in VALID_TICKERS or bool(HOSE_PATTERN.match(str(x))))
        
        # Clean date column
        date_cols = ['date', 'Date', 'trading_date']
        for col in date_cols:
            if col in df.columns:
                try:
                    df['date'] = pd.to_datetime(df[col], errors='coerce')
                    report.date_issues = df['date'].isna().sum()
                    break
                except Exception as e:
                    logger.warning(f"Error parsing date column {col}: {e}")
        
        # Clean price columns
        price_cols = ['close', 'close_adjusted', 'price', 'Close Adjusted (D)']
        for col in price_cols:
            if col in df.columns:
                df['close'] = df[col].apply(lambda x: self.validate_price(x)[0])
                report.missing_prices = df['close'].isna().sum()
                break
        
        # Clean volume columns
        volume_cols = ['volume', 'total_volume', 'trading_volume', 'Total trading volume (D)']
        for col in volume_cols:
            if col in df.columns:
                df['volume'] = df[col].apply(lambda x: self.validate_volume(x)[0])
                report.missing_volumes = df['volume'].isna().sum()
                break
        
        # Clean buy/sell volumes
        if 'buy_volume' in df.columns:
            df['buy_volume'] = df['buy_volume'].apply(lambda x: self.validate_volume(x)[0])
        if 'sell_volume' in df.columns:
            df['sell_volume'] = df['sell_volume'].apply(lambda x: self.validate_volume(x)[0])
        
        # Detect outliers
        if 'close' in df.columns:
            outliers = self.detect_outliers(df, 'close')
            df['price_outlier'] = outliers
            report.outliers_detected = outliers.sum()
        
        # Remove duplicates
        if 'ticker' in df.columns and 'date' in df.columns:
            before_dedup = len(df)
            df = df.drop_duplicates(subset=['ticker', 'date'], keep='last')
            report.duplicate_records = before_dedup - len(df)
        
        # Fill missing prices
        if 'close' in df.columns and 'ticker' in df.columns:
            df = self.fill_missing_prices(df, 'close', method='ffill')
        
        # Add data quality flag
        df['data_quality_flag'] = 'OK'
        
        if 'ticker_valid' in df.columns:
            df.loc[~df['ticker_valid'], 'data_quality_flag'] = 'INVALID_TICKER'
        if 'close' in df.columns:
            df.loc[df['close'].isna(), 'data_quality_flag'] = 'MISSING_PRICE'
        if 'price_outlier' in df.columns:
            df.loc[df['price_outlier'], 'data_quality_flag'] = 'PRICE_OUTLIER'
        
        report.valid_records = len(df[df['data_quality_flag'] == 'OK'])
        
        return df, report
    
    def clean_recommendations(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, DataQualityReport]:
        """
        Clean and validate analyst recommendations DataFrame.
        
        Args:
            df: Raw recommendations DataFrame
            
        Returns:
            Tuple of (cleaned DataFrame, quality report)
        """
        report = DataQualityReport()
        report.total_records = len(df)
        
        df = df.copy()
        
        # Standardize column names
        col_mapping = {
            'Ticker': 'ticker',
            'Comp name': 'company_name',
            'Analyst': 'analyst',
            'Recommendation': 'recommendation',
            'Target price': 'target_price',
            'Issue date': 'issue_date',
            'Date collected': 'date_collected'
        }
        df = df.rename(columns=col_mapping)
        
        # Clean ticker symbols
        if 'ticker' in df.columns:
            cleaned_tickers = []
            for ticker in df['ticker']:
                std_ticker, is_valid, note = self.standardize_ticker(ticker)
                cleaned_tickers.append(std_ticker)
                
                if not is_valid:
                    report.invalid_tickers.append(str(ticker))
                elif note and 'Corrected' in note:
                    report.corrected_tickers[str(ticker)] = std_ticker
            
            df['ticker'] = cleaned_tickers
        
        # Standardize recommendation ratings
        rating_mapping = {
            'strong buy': 5, 'buy': 5, 'add': 5, 'accumulate': 5,
            'outperform': 4, 'overweight': 4, 'overwt/in-line': 4,
            'hold': 3, 'market perform': 3, 'neutral': 3, 'equalwt/in-line': 3,
            'underperform': 2, 'underweight': 2,
            'reduce': 1, 'sell': 1, 'strong sell': 1
        }
        
        if 'recommendation' in df.columns:
            df['recommendation_clean'] = df['recommendation'].str.lower().str.strip()
            df['rating_numeric'] = df['recommendation_clean'].map(rating_mapping)
            
            # Flag unmapped recommendations
            unmapped = df[df['rating_numeric'].isna() & df['recommendation'].notna()]
            for _, row in unmapped.iterrows():
                report.flagged_records.append({
                    'ticker': row.get('ticker', ''),
                    'issue': f"Unknown recommendation: {row.get('recommendation', '')}"
                })
        
        # Clean dates
        for col in ['issue_date', 'date_collected']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Clean target price
        if 'target_price' in df.columns:
            df['target_price'] = pd.to_numeric(df['target_price'], errors='coerce')
            report.missing_prices = df['target_price'].isna().sum()
        
        # Remove rows with missing critical data
        critical_cols = ['ticker', 'recommendation']
        for col in critical_cols:
            if col in df.columns:
                df = df[df[col].notna() & (df[col] != '')]
        
        # Remove duplicates
        if all(col in df.columns for col in ['ticker', 'analyst', 'issue_date']):
            before_dedup = len(df)
            df = df.drop_duplicates(subset=['ticker', 'analyst', 'issue_date'], keep='last')
            report.duplicate_records = before_dedup - len(df)
        
        report.valid_records = len(df)
        
        return df, report
    
    def load_and_clean_all(self) -> Dict[str, Tuple[pd.DataFrame, DataQualityReport]]:
        """
        Load and clean all data files from the xlsx directory.
        
        Returns:
            Dictionary mapping data type to (cleaned DataFrame, report)
        """
        results = {}
        
        # Load and merge market data files
        logger.info("Loading market data files...")
        market_dfs = []
        
        for file_type in ['close', 'buy', 'sell', 'tra', 'sha']:
            for i in range(1, 10):
                file_path = self.data_dir / f"{file_type}{i}.csv"
                if file_path.exists():
                    try:
                        logger.info(f"Loading {file_path}...")
                        df = self._load_csv_with_header_detection(file_path)
                        df['source_file'] = f"{file_type}{i}"
                        market_dfs.append(df)
                        logger.info(f"  Loaded {len(df)} rows from {file_type}{i}.csv")
                    except Exception as e:
                        logger.error(f"Error loading {file_path}: {e}")
        
        if market_dfs:
            logger.info(f"Merging {len(market_dfs)} market data files...")
            # Merge all market data
            merged_market = self._merge_market_files(market_dfs)
            logger.info(f"Merged data has {len(merged_market)} records")
            
            if len(merged_market) > 0:
                cleaned_market, market_report = self.clean_market_data(merged_market)
                results['market_data'] = (cleaned_market, market_report)
        
        # Load recommendations
        rec_path = self.data_dir / "rec.csv"
        if rec_path.exists():
            try:
                logger.info("Loading recommendations...")
                rec_df = self._load_recommendations(rec_path)
                cleaned_rec, rec_report = self.clean_recommendations(rec_df)
                results['recommendations'] = (cleaned_rec, rec_report)
                logger.info(f"  Loaded {len(cleaned_rec)} recommendations")
            except Exception as e:
                logger.error(f"Error loading recommendations: {e}")
        
        # Load VNIndex
        vnindex_path = self.data_dir / "vnindex.csv"
        if vnindex_path.exists():
            try:
                logger.info("Loading VNIndex...")
                vnindex_df = self._load_csv_with_header_detection(vnindex_path)
                # Basic cleaning for VNIndex
                vnindex_df.columns = vnindex_df.columns.str.lower().str.strip()
                results['vnindex'] = (vnindex_df, DataQualityReport())
            except Exception as e:
                logger.error(f"Error loading VNIndex: {e}")
        
        # Load risk-free rate
        rfr_path = self.data_dir / "rfr.csv"
        if rfr_path.exists():
            try:
                logger.info("Loading risk-free rate...")
                rfr_df = self._load_csv_with_header_detection(rfr_path)
                rfr_df.columns = rfr_df.columns.str.lower().str.strip()
                results['risk_free_rate'] = (rfr_df, DataQualityReport())
            except Exception as e:
                logger.error(f"Error loading risk-free rate: {e}")
        
        return results
    
    def _load_recommendations(self, file_path: Path) -> pd.DataFrame:
        """
        Load recommendations CSV with special handling for its format.
        """
        # Read first few rows to find header
        preview = pd.read_csv(file_path, nrows=10, header=None, encoding='utf-8')
        
        header_row = 0
        for i, row in preview.iterrows():
            row_str = ' '.join(str(x) for x in row.values if pd.notna(x))
            if 'Ticker' in row_str and 'Recommendation' in row_str:
                header_row = i
                break
        
        # Load with correct header
        df = pd.read_csv(file_path, header=header_row, encoding='utf-8')
        
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Remove rows where all values are NaN (empty rows)
        df = df.dropna(how='all')
        
        # Remove rows where critical columns are missing
        if 'Ticker' in df.columns:
            df = df[df['Ticker'].notna()]
        
        return df
    
    def _load_csv_with_header_detection(self, file_path: Path) -> pd.DataFrame:
        """
        Load CSV file with automatic header row detection.
        
        The xlsx files have metadata rows before the actual data.
        Data is in wide format: tickers as columns, dates as rows.
        The ticker symbols are in a row above the header row.
        """
        # Read first few rows to detect header structure
        preview = pd.read_csv(file_path, nrows=15, header=None, encoding='utf-8')
        
        # Find the row with ticker symbols (row before the data header)
        ticker_row = None
        header_row = None
        
        for i, row in preview.iterrows():
            row_str = ' '.join(str(x) for x in row.values if pd.notna(x))
            # Look for row containing 'No' and 'Date' - this is the header row
            if 'No' in row_str and 'Date' in row_str:
                header_row = i
                ticker_row = i - 1  # Tickers are in the row above
                break
        
        if header_row is None:
            # Fallback: look for any row with Date
            for i, row in preview.iterrows():
                row_str = ' '.join(str(x) for x in row.values if pd.notna(x))
                if 'Date' in row_str:
                    header_row = i
                    ticker_row = i - 1 if i > 0 else None
                    break
        
        if header_row is None:
            header_row = 0
        
        # Get ticker symbols from the ticker row
        tickers = []
        if ticker_row is not None and ticker_row >= 0:
            ticker_data = preview.iloc[ticker_row]
            for t in ticker_data.values:
                if pd.notna(t) and str(t).strip():
                    ticker_str = str(t).strip().upper()
                    # Check if it looks like a ticker (3-4 uppercase letters)
                    if len(ticker_str) >= 2 and len(ticker_str) <= 6 and ticker_str.isalpha():
                        tickers.append(ticker_str)
                    else:
                        tickers.append(None)
                else:
                    tickers.append(None)
        
        # Load the data, skipping metadata rows
        df = pd.read_csv(file_path, skiprows=header_row, encoding='utf-8')
        
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Rename columns to ticker symbols if we have them
        if tickers and len(tickers) >= len(df.columns):
            new_columns = []
            ticker_idx = 0
            for i, col in enumerate(df.columns):
                col_lower = str(col).lower()
                if 'no' in col_lower or col_lower == 'no':
                    new_columns.append('No')
                elif 'date' in col_lower:
                    new_columns.append('Date')
                else:
                    # Find next valid ticker
                    while ticker_idx < len(tickers) and tickers[ticker_idx] is None:
                        ticker_idx += 1
                    if ticker_idx < len(tickers) and tickers[ticker_idx]:
                        new_columns.append(tickers[ticker_idx])
                        ticker_idx += 1
                    else:
                        new_columns.append(col)
            
            if len(new_columns) == len(df.columns):
                df.columns = new_columns
        
        # Remove empty columns
        df = df.dropna(axis=1, how='all')
        
        return df
    
    def _merge_market_files(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Merge multiple market data files into a single DataFrame.
        Converts wide format (tickers as columns) to long format (ticker, date, value).
        """
        if not dfs:
            return pd.DataFrame()
        
        all_records = []
        
        for df in dfs:
            source_file = df.get('source_file', ['unknown'])[0] if 'source_file' in df.columns else 'unknown'
            
            # Determine data type from source file name
            data_type = 'unknown'
            if 'buy' in str(source_file).lower():
                data_type = 'buy_volume'
            elif 'sell' in str(source_file).lower():
                data_type = 'sell_volume'
            elif 'close' in str(source_file).lower():
                data_type = 'close'
            elif 'tra' in str(source_file).lower():
                data_type = 'trading_volume'
            elif 'sha' in str(source_file).lower():
                data_type = 'shares_outstanding'
            
            # Find date column
            date_col = None
            for col in df.columns:
                if 'date' in str(col).lower():
                    date_col = col
                    break
            
            if date_col is None:
                continue
            
            # Get ticker columns (all columns except No, Date, source_file)
            exclude_cols = {'no', 'date', 'source_file'}
            ticker_cols = [col for col in df.columns 
                          if str(col).lower() not in exclude_cols 
                          and not str(col).startswith('Unnamed')]
            
            # Convert wide to long format
            for _, row in df.iterrows():
                date_val = row.get(date_col)
                if pd.isna(date_val):
                    continue
                    
                for ticker in ticker_cols:
                    value = row.get(ticker)
                    if pd.notna(value):
                        all_records.append({
                            'date': date_val,
                            'ticker': str(ticker).strip().upper(),
                            'value': value,
                            'data_type': data_type,
                            'source_file': source_file
                        })
        
        if not all_records:
            return pd.DataFrame()
        
        # Create long-format DataFrame
        long_df = pd.DataFrame(all_records)
        
        # Pivot to get one row per ticker-date with columns for each data type
        try:
            pivoted = long_df.pivot_table(
                index=['ticker', 'date'],
                columns='data_type',
                values='value',
                aggfunc='first'
            ).reset_index()
            
            # Flatten column names
            pivoted.columns = [col if isinstance(col, str) else col for col in pivoted.columns]
            
            return pivoted
        except Exception as e:
            logger.warning(f"Error pivoting data: {e}, returning long format")
            return long_df
    
    def export_clean_data(
        self,
        output_dir: str = "data/clean",
        format: str = "csv"
    ) -> Dict[str, str]:
        """
        Export cleaned data to files.
        
        Args:
            output_dir: Directory for output files
            format: Output format ('csv', 'parquet', 'json')
            
        Returns:
            Dictionary mapping data type to output file path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = self.load_and_clean_all()
        output_files = {}
        
        for data_type, (df, report) in results.items():
            if format == 'csv':
                file_path = output_path / f"{data_type}_clean.csv"
                df.to_csv(file_path, index=False)
            elif format == 'parquet':
                file_path = output_path / f"{data_type}_clean.parquet"
                df.to_parquet(file_path, index=False)
            elif format == 'json':
                file_path = output_path / f"{data_type}_clean.json"
                df.to_json(file_path, orient='records', date_format='iso')
            
            output_files[data_type] = str(file_path)
            
            # Save quality report
            report_path = output_path / f"{data_type}_quality_report.json"
            with open(report_path, 'w') as f:
                json.dump(report.to_dict(), f, indent=2)
            
            logger.info(f"Exported {data_type}: {len(df)} records, quality score: {report.to_dict()['data_quality_score']}")
        
        return output_files


def main():
    """Main entry point for data cleaning."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    cleaner = DataCleaner(data_dir="xlsx")
    
    print("=" * 60)
    print("SentimentAlpha Vietnam - Data Cleaning & Consolidation")
    print("=" * 60)
    
    # Load and clean all data
    results = cleaner.load_and_clean_all()
    
    # Print summary
    for data_type, (df, report) in results.items():
        print(f"\n{data_type.upper()}")
        print("-" * 40)
        report_dict = report.to_dict()
        print(f"  Total Records: {report_dict['total_records']}")
        print(f"  Valid Records: {report_dict['valid_records']}")
        print(f"  Data Quality Score: {report_dict['data_quality_score']}%")
        print(f"  Invalid Tickers: {len(report_dict['invalid_tickers'])}")
        print(f"  Missing Prices: {report_dict['missing_prices']}")
        print(f"  Outliers: {report_dict['outliers_detected']}")
        print(f"  Duplicates Removed: {report_dict['duplicate_records']}")
    
    # Export clean data
    print("\n" + "=" * 60)
    print("Exporting cleaned data...")
    output_files = cleaner.export_clean_data(output_dir="data/clean", format="csv")
    
    for data_type, file_path in output_files.items():
        print(f"  {data_type}: {file_path}")
    
    print("\nData cleaning complete!")


if __name__ == "__main__":
    main()
