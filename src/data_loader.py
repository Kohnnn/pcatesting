"""
DataLoader class for loading and parsing CSV files from xlsx/ directory.
"""
import pandas as pd
from pathlib import Path
from typing import Optional


class DataLoader:
    """Loads and parses CSV files from xlsx/ directory."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize DataLoader with data directory path.
        
        Args:
            data_dir: Path to directory containing CSV files (defaults to DATA_SOURCE_DIR env var or 'xlsx')
        """
        import os
        if data_dir is None:
            data_dir = os.getenv("DATA_SOURCE_DIR", "xlsx")
        self.data_dir = Path(data_dir)
    
    def load_wide_csv(self, filepath: str, skip_rows: int = 7, chunksize: Optional[int] = None) -> pd.DataFrame:
        """
        Load wide-format CSV with ticker columns.
        
        The CSV files have:
        - Header metadata rows (rows 0-6)
        - Ticker symbols as column headers in row 7
        - Column descriptions in row 8
        - Data starting from row 9 with format: No, Date, then values for each ticker
        
        Args:
            filepath: Path to CSV file (relative to data_dir or absolute)
            skip_rows: Number of header rows to skip before ticker row (default 7)
            chunksize: If specified, read file in chunks to reduce memory usage
            
        Returns:
            DataFrame with Date column and ticker columns
        """
        # Construct full path - handle both string and Path objects
        filepath_obj = Path(filepath)
        if not filepath_obj.is_absolute():
            # Only prepend data_dir if filepath doesn't already start with it
            if not str(filepath).startswith(str(self.data_dir)):
                filepath_obj = self.data_dir / filepath
        
        # Read CSV with ticker symbols as header (row 7)
        # Skip rows 0-6 (metadata) and row 8 (descriptions)
        # Fix DtypeWarning by specifying low_memory=False for mixed types
        if chunksize:
            # Read in chunks to reduce memory usage
            chunks = []
            for chunk in pd.read_csv(
                str(filepath_obj),
                skiprows=list(range(skip_rows)) + [skip_rows + 1],
                header=0,
                low_memory=False,
                chunksize=chunksize
            ):
                chunks.append(chunk)
            df = pd.concat(chunks, ignore_index=True)
            # Explicitly delete chunks to free memory
            del chunks
        else:
            df = pd.read_csv(
                str(filepath_obj),
                skiprows=list(range(skip_rows)) + [skip_rows + 1],  # Skip 0-6 and 8
                header=0,  # Use row 7 as header
                low_memory=False
            )
        
        # Drop the first column (No/Unnamed: 0) if it exists
        if 'No' in df.columns:
            df = df.drop(columns=['No'])
        elif 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        # Rename 'Unnamed: 1' to 'Date' if it exists
        if 'Unnamed: 1' in df.columns:
            df = df.rename(columns={'Unnamed: 1': 'Date'})
        
        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    
    def merge_fragmented_files(self, prefix: str, count: int = 9) -> pd.DataFrame:
        """
        Merge fragmented CSV files (buy1-9, sell1-9, etc.) into single DataFrame.
        
        Files are split because they contain many ticker columns. This method
        concatenates them horizontally (column-wise).
        
        Args:
            prefix: File prefix (e.g., 'buy', 'sell', 'close', 'tra', 'sha')
            count: Number of fragments (default 9)
            
        Returns:
            Merged DataFrame with all ticker columns
        """
        dfs = []
        
        for i in range(1, count + 1):
            filename = f"{prefix}{i}.csv"
            try:
                df = self.load_wide_csv(filename)
                
                # For the first file, keep the Date column
                # For subsequent files, drop the Date column to avoid duplicates
                if i > 1 and 'Date' in df.columns:
                    df = df.drop(columns=['Date'])
                
                dfs.append(df)
            except FileNotFoundError:
                # If a file doesn't exist, skip it
                print(f"Warning: {filename} not found, skipping")
                continue
        
        if not dfs:
            raise ValueError(f"No files found for prefix '{prefix}'")
        
        # Concatenate horizontally (along columns)
        merged_df = pd.concat(dfs, axis=1)
        
        return merged_df
    
    def load_recommendations(self) -> pd.DataFrame:
        """
        Load and parse rec.csv with analyst recommendations.
        
        Returns:
            DataFrame with columns: Ticker, Comp name, Analyst, Recommendation, 
                                   Target price, Issue date
        """
        filepath = self.data_dir / "rec.csv"
        
        # Skip first 2 rows (header metadata)
        # Fix DtypeWarning by specifying low_memory=False for mixed types in columns 2,3,4,6
        df = pd.read_csv(filepath, skiprows=2, low_memory=False)
        
        # Drop the first unnamed column
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        # Drop 'Date collected' column if present
        if 'Date collected' in df.columns:
            df = df.drop(columns=['Date collected'])
        
        # Convert Issue date to datetime
        if 'Issue date' in df.columns:
            df['Issue date'] = pd.to_datetime(df['Issue date'], errors='coerce')
        
        # Drop rows where all critical fields are null
        df = df.dropna(subset=['Ticker', 'Recommendation'], how='all')
        
        # Drop rows where Recommendation is null (these are placeholder rows)
        df = df.dropna(subset=['Recommendation'])
        
        return df
    
    def load_vnindex(self) -> pd.DataFrame:
        """
        Load VNIndex benchmark data.
        
        Returns:
            DataFrame with columns: Date, Close Index, Buy Volume, Sell Volume, Trading Volume
        """
        # Fix: Use correct path without duplication
        filepath = self.data_dir / "vnindex.csv"
        
        # VNIndex has same structure as other wide CSVs
        df = self.load_wide_csv(filepath)
        
        # Rename columns for clarity - handle various possible column names
        column_mapping = {
            'Close Index': 'close_index',
            'Close Index (D)\nUnit: Point': 'close_index',
            'Buy Volume': 'buy_volume',
            'Total Buy Trade Volume (D)\nUnit: Shares': 'buy_volume',
            'Sell Volume': 'sell_volume',
            'Total Sell Trade Volume (D)\nUnit: Shares': 'sell_volume',
            'Trading Volume': 'total_volume',
            'Total Trading Volume (D)\nUnit: Shares': 'total_volume'
        }
        
        # Only rename columns that exist
        existing_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
        if existing_cols:
            df = df.rename(columns=existing_cols)
        
        return df
    
    def load_risk_free_rate(self) -> pd.DataFrame:
        """
        Load risk-free rate data.
        
        Returns:
            DataFrame with columns: Date, rate
        """
        # Fix: Use correct path without duplication
        filepath = self.data_dir / "rfr.csv"
        
        df = self.load_wide_csv(filepath)
        
        # The file should have Date and rate columns
        # Rename if needed
        if len(df.columns) == 2:
            df.columns = ['Date', 'rate']
        
        return df
