"""Module for fetching stock data"""
import pandas as pd
from typing import Optional
from .mock_data import generate_mock_prices

def get_stock_data(ticker: str, start_date: str, end_date: str) -> pd.Series:
    """
    Fetch stock data (currently using mock data while yfinance is unavailable)
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date for data
        end_date: End date for data
        
    Returns:
        Pandas Series with daily prices
    """
    try:
        # Usando dados simulados temporariamente
        base_price = 100.0 if 'PETR3' in ticker else 90.0
        return generate_mock_prices(start_date, end_date, base_price)
        
    except Exception as e:
        raise Exception(f"Erro ao gerar dados para {ticker}: {str(e)}")