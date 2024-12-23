"""Risk management utilities for spread trading"""
import pandas as pd
import numpy as np
from typing import Dict, Union

def calculate_risk_metrics(spread_series: pd.Series, 
                         position_size: float,
                         confidence_level: float = 0.95) -> Dict[str, float]:
    """
    Calculate key risk metrics for position management
    
    Args:
        spread_series: Pandas Series containing spread values
        position_size: Size of the trading position
        confidence_level: Confidence level for VaR calculation
        
    Returns:
        Dictionary containing risk metrics
    """
    daily_returns = spread_series.pct_change().dropna()
    
    # Calculate Value at Risk (VaR)
    var = np.percentile(daily_returns, (1 - confidence_level) * 100)
    var_position = position_size * var
    
    # Calculate Maximum Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    rolling_max = cumulative_returns.expanding().max()
    drawdowns = cumulative_returns / rolling_max - 1
    max_drawdown = drawdowns.min()
    
    return {
        'daily_volatility': daily_returns.std(),
        'annualized_volatility': daily_returns.std() * np.sqrt(252),
        'value_at_risk': var_position,
        'max_drawdown': max_drawdown,
        'position_risk': position_size * daily_returns.std()
    }

def calculate_stop_levels(current_spread: float,
                         volatility: float,
                         risk_multiple: float = 2.0) -> Dict[str, float]:
    """
    Calculate stop loss and take profit levels
    
    Args:
        current_spread: Current spread value
        volatility: Spread volatility
        risk_multiple: Multiple of volatility for stop levels
        
    Returns:
        Dictionary containing stop levels
    """
    return {
        'stop_loss': current_spread - (volatility * risk_multiple),
        'take_profit': current_spread + (volatility * risk_multiple)
    }