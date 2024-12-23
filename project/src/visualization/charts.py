"""Module for creating analysis charts"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_spread_chart(spread_series: pd.Series, spread_min: float, title: str):
    """Create spread analysis chart"""
    fig = px.line(
        spread_series,
        title=title
    )
    fig.add_hline(y=spread_min, line_dash="dash", line_color="red")
    return fig

def plot_returns_distribution(returns: pd.Series, title: str):
    """Create returns distribution chart"""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=30
    ))
    fig.update_layout(
        title=title,
        xaxis_title='Retorno (R$)',
        yaxis_title='Frequência'
    )
    return fig