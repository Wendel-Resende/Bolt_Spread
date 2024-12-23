"""Main application file for spread trading analysis"""
import streamlit as st
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from analysis.spread_analyzer import (
    calculate_spread,
    analyze_spread_opportunities,
    get_pair_metrics
)
from utils.statistics import calculate_spread_statistics, calculate_rolling_statistics
from utils.risk_management import calculate_risk_metrics, calculate_stop_levels

def get_stock_data(ticker: str, start_date: str, end_date: str) -> pd.Series:
    """Fetch stock data from Yahoo Finance"""
    if not ticker.endswith('.SA'):
        ticker = f"{ticker}.SA"
    try:
        stock = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        return stock['High']
    except Exception as e:
        st.error(f"Erro ao obter dados para {ticker}: {str(e)}")
        return None

def analyze_specific_pair(stock_a: str, stock_b: str, 
                         start_date: datetime,
                         end_date: datetime,
                         spread_min: float,
                         custo_operacional: float):
    """Analyze a specific stock pair"""
    try:
        # Fetch data
        data_a = get_stock_data(stock_a, start_date, end_date)
        data_b = get_stock_data(stock_b, start_date, end_date)
        
        if data_a is None or data_b is None:
            return None
        
        # Calculate spread and opportunities
        spread = calculate_spread(data_a, data_b)
        oportunidades = analyze_spread_opportunities(spread, spread_min, custo_operacional)
        
        # Get metrics
        metrics = get_pair_metrics(data_a, data_b, spread, oportunidades)
        
        # Calculate additional statistics
        stats = calculate_spread_statistics(spread)
        rolling_stats = calculate_rolling_statistics(spread)
        
        # Calculate risk metrics (assuming position size of 1000)
        risk_metrics = calculate_risk_metrics(spread, 1000.0)
        
        # Calculate stop levels
        current_spread = spread.iloc[-1]
        stop_levels = calculate_stop_levels(current_spread, stats['std'])
        
        return {
            'metrics': metrics,
            'statistics': stats,
            'rolling_stats': rolling_stats,
            'risk_metrics': risk_metrics,
            'stop_levels': stop_levels,
            'opportunities': oportunidades
        }
        
    except Exception as e:
        st.error(f"Erro na análise: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Análise de Spread", layout="wide")
    st.title("📊 Análise de Spread entre Ações")
    
    # Interface inputs
    col1, col2 = st.columns(2)
    stock_a = col1.text_input("Ação A", value="PETR3").upper()
    stock_b = col2.text_input("Ação B", value="PETR4").upper()
    
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input("Data Inicial", datetime.now() - timedelta(days=365))
    end_date = col2.date_input("Data Final", datetime.now())
    spread_min = col3.number_input("Spread Mínimo (R$)", min_value=0.1, value=1.0, step=0.1)
    
    custo_operacional = st.number_input(
        "Custo Operacional por Operação (R$)",
        min_value=0.0,
        value=5.0,
        step=0.5
    )
    
    if st.button("Analisar Par"):
        result = analyze_specific_pair(
            stock_a, stock_b,
            start_date, end_date,
            spread_min, custo_operacional
        )
        
        if result:
            # Display basic metrics
            metrics = result['metrics']
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Spread Médio", f"R$ {metrics['Spread_Medio']:.2f}")
            col2.metric("Total de Oportunidades", metrics['Total_Oportunidades'])
            col3.metric("Retorno Total Potencial", f"R$ {metrics['Retorno_Total']:.2f}")
            col4.metric("Retorno Médio por Operação", f"R$ {metrics['Retorno_Medio']:.2f}")
            
            # Display risk metrics
            st.subheader("Métricas de Risco")
            risk_metrics = result['risk_metrics']
            col1, col2, col3 = st.columns(3)
            col1.metric("VaR Diário", f"R$ {risk_metrics['value_at_risk']:.2f}")
            col2.metric("Volatilidade Anualizada", f"{risk_metrics['annualized_volatility']:.2%}")
            col3.metric("Drawdown Máximo", f"{risk_metrics['max_drawdown']:.2%}")
            
            # Display stop levels
            st.subheader("Níveis de Stop")
            stop_levels = result['stop_levels']
            col1, col2 = st.columns(2)
            col1.metric("Stop Loss", f"R$ {stop_levels['stop_loss']:.2f}")
            col2.metric("Take Profit", f"R$ {stop_levels['take_profit']:.2f}")
            
            # Display opportunities
            if not result['opportunities'].empty:
                st.subheader("Oportunidades Identificadas")
                st.dataframe(result['opportunities'])

if __name__ == "__main__":
    main()