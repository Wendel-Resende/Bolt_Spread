"""Main application file for spread trading analysis"""
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from data.stock_fetcher import get_stock_data
from analysis.spread_analyzer import (
    calculate_spread,
    analyze_spread_opportunities,
    get_pair_metrics
)
from visualization.charts import plot_spread_chart, plot_returns_distribution

def analyze_specific_pair(stock_a: str, stock_b: str, 
                         start_date: datetime,
                         end_date: datetime,
                         spread_min: float,
                         custo_operacional: float):
    """Analyze a specific stock pair"""
    try:
        # Fetch data
        data_a = get_stock_data(stock_a, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        data_b = get_stock_data(stock_b, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        # Calculate spread and opportunities
        spread = calculate_spread(data_a, data_b)
        oportunidades = analyze_spread_opportunities(spread, spread_min, custo_operacional)
        
        # Get metrics
        metrics = get_pair_metrics(data_a, data_b, spread, oportunidades)
        
        # Create visualizations
        spread_chart = plot_spread_chart(spread, spread_min, f'Spread {stock_a}/{stock_b}')
        returns_chart = plot_returns_distribution(
            oportunidades['Retorno_Liquido'] if len(oportunidades) > 0 else pd.Series(),
            'Distribuição dos Retornos Líquidos'
        )
        
        return metrics, spread_chart, returns_chart, oportunidades
        
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
            metrics, spread_chart, returns_chart, oportunidades = result
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Spread Médio", f"R$ {metrics['Spread_Medio']:.2f}")
            col2.metric("Total de Oportunidades", metrics['Total_Oportunidades'])
            col3.metric("Retorno Total Potencial", f"R$ {metrics['Retorno_Total']:.2f}")
            col4.metric("Retorno Médio por Operação", f"R$ {metrics['Retorno_Medio']:.2f}")
            
            # Display charts
            st.plotly_chart(spread_chart, use_container_width=True)
            if len(oportunidades) > 0:
                st.plotly_chart(returns_chart, use_container_width=True)
                st.dataframe(oportunidades)

if __name__ == "__main__":
    main()