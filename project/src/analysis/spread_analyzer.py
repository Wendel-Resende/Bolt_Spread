"""Module for spread analysis calculations"""
import pandas as pd
import numpy as np
from typing import Dict, Optional

def calculate_spread(price_a: pd.Series, price_b: pd.Series) -> pd.Series:
    """Calculate the spread between two price series"""
    return (price_a - price_b).abs().round(2)

def analyze_spread_opportunities(spread: pd.Series, 
                               spread_min: float,
                               custo_operacional: float = 5.0) -> pd.DataFrame:
    """
    Analyze spread trading opportunities
    """
    oportunidades = spread[spread >= spread_min].copy()
    if len(oportunidades) == 0:
        return pd.DataFrame()
    
    return pd.DataFrame({
        'Data': oportunidades.index,
        'Spread': oportunidades,
        'Retorno_Bruto': oportunidades - (spread_min / 2),
        'Custo_Total': custo_operacional * 2,
        'Retorno_Liquido': (oportunidades - (spread_min / 2)) - (custo_operacional * 2)
    })

def get_pair_metrics(stock_a: pd.Series, 
                    stock_b: pd.Series, 
                    spread: pd.Series,
                    oportunidades: pd.DataFrame) -> Dict:
    """
    Calculate key metrics for a stock pair
    """
    return {
        'Spread_Medio': spread.mean(),
        'Spread_Maximo': spread.max(),
        'Total_Oportunidades': len(oportunidades),
        'Retorno_Medio': oportunidades['Retorno_Liquido'].mean() if len(oportunidades) > 0 else 0,
        'Retorno_Total': oportunidades['Retorno_Liquido'].sum() if len(oportunidades) > 0 else 0,
        'Correlacao': stock_a.corr(stock_b)
    }