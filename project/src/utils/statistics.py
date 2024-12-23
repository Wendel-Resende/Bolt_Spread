"""Statistical analysis utilities for spread trading"""
import pandas as pd
import numpy as np

def calculate_spread_statistics(spread_series: pd.Series) -> dict:
    """
    Calculate key statistical metrics for spread analysis
    
    Args:
        spread_series: Pandas Series containing spread values
        
    Returns:
        Dictionary containing statistical metrics
    """
    return {
        'mean': spread_series.mean(),
        'std': spread_series.std(),
        'z_score': (spread_series - spread_series.mean()) / spread_series.std(),
        'percentile_95': spread_series.quantile(0.95),
        'percentile_5': spread_series.quantile(0.05),
        'skew': spread_series.skew(),
        'kurtosis': spread_series.kurtosis()
    }

def calculate_rolling_statistics(spread_series: pd.Series, window: int = 20) -> pd.DataFrame:
    """
    Calculate rolling statistical metrics
    
    Args:
        spread_series: Pandas Series containing spread values
        window: Rolling window size
        
    Returns:
        DataFrame with rolling statistics
    """
    df = pd.DataFrame()
    df['rolling_mean'] = spread_series.rolling(window=window).mean()
    df['rolling_std'] = spread_series.rolling(window=window).std()
    df['upper_band'] = df['rolling_mean'] + (2 * df['rolling_std'])
    df['lower_band'] = df['rolling_mean'] - (2 * df['rolling_std'])
    return df