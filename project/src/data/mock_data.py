"""Module for generating mock stock data for testing"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_prices(start_date: str, end_date: str, base_price: float = 100.0) -> pd.Series:
    """
    Generate mock stock price data
    
    Args:
        start_date: Start date for data generation
        end_date: End date for data generation
        base_price: Initial price for the stock
        
    Returns:
        Pandas Series with daily prices
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    dates = pd.date_range(start=start, end=end, freq='D')
    
    # Generate random walk
    returns = np.random.normal(loc=0.0001, scale=0.02, size=len(dates))
    price = base_price * (1 + returns).cumprod()
    
    return pd.Series(price, index=dates)