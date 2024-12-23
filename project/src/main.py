"""Main application file for spread trading analysis"""
import streamlit as st
from datetime import datetime, timedelta
import sys
import subprocess

# Instala yfinance se não estiver disponível
if 'yfinance' not in sys.modules:
    st.info("Instalando dependências necessárias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])

import yfinance as yf
import pandas as pd
from analysis.spread_analyzer import (
    calculate_spread,
    analyze_spread_opportunities,
    get_pair_metrics
)
from utils.statistics import calculate_spread_statistics, calculate_rolling_statistics
from utils.risk_management import calculate_risk_metrics, calculate_stop_levels

# ... resto do código permanece igual ...