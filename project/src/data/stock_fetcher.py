"""Module for fetching stock data"""
import yfinance as yf
import pandas as pd
from typing import Optional

def get_stock_data(ticker: str, start_date: str, end_date: str) -> pd.Series:
    """
    Fetch historical stock data from Yahoo Finance
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date for data
        end_date: End date for data
        
    Returns:
        Pandas Series with daily prices
    """
    try:
        if not ticker.endswith('.SA'):
            ticker = f"{ticker}.SA"
            
        stock = yf.download(
            ticker, 
            start=start_date, 
            end=end_date, 
            progress=False,
            show_errors=False
        )
        
        if stock.empty:
            raise Exception(f"Não foi possível obter dados para {ticker}")
            
        return stock['Close']
        
    except Exception as e:
        raise Exception(f"Erro ao buscar dados para {ticker}: {str(e)}")