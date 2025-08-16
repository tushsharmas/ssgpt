import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import numpy as np
import sqlite3
import json
import pyperclip
import os
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="Advanced Real-Time Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup for history feature
DB_PATH = "stock_history.db"

def init_database():
    """Initialize SQLite database for storing query history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            company_name TEXT,
            query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            period TEXT,
            current_price REAL,
            change_amount REAL,
            change_percent REAL,
            volume INTEGER,
            market_cap INTEGER,
            sector TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_history(ticker: str, stock_info: Dict[str, Any], period: str, 
                   current_price: float, change_amount: float, change_percent: float,
                   volume: int, summary: str):
    """Save query to history database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Keep only last 10 entries per ticker to avoid database bloat
        cursor.execute('''
            DELETE FROM query_history 
            WHERE ticker = ? AND id NOT IN (
                SELECT id FROM query_history 
                WHERE ticker = ? 
                ORDER BY query_time DESC 
                LIMIT 9
            )
        ''', (ticker, ticker))
        
        cursor.execute('''
            INSERT INTO query_history 
            (ticker, company_name, period, current_price, change_amount, 
             change_percent, volume, market_cap, sector, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticker,
            stock_info.get('longName', ticker),
            period,
            current_price,
            change_amount,
            change_percent,
            volume,
            stock_info.get('marketCap', 0),
            stock_info.get('sector', 'N/A'),
            summary
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error saving to history: {e}")

def get_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve query history from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM query_history 
            ORDER BY query_time DESC 
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        st.error(f"Error retrieving history: {e}")
        return []

def copy_to_clipboard(text: str, label: str = "text"):
    """Copy text to clipboard with user feedback"""
    try:
        pyperclip.copy(text)
        st.success(f"✅ {label} copied to clipboard!")
    except Exception as e:
        st.error(f"❌ Failed to copy to clipboard: {e}")
        # Fallback: show text in a text area for manual copying
        st.text_area(f"Copy this {label} manually:", value=text, height=100)

def create_copy_button(text: str, label: str, key: str):
    """Create a copy button with unique key"""
    if st.button(f"📋 Copy {label}", key=key, help=f"Copy {label} to clipboard"):
        copy_to_clipboard(text, label)

# Custom CSS for better UI
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive { color: #00C851; }
    .negative { color: #ff4444; }
    .neutral { color: #33b5e5; }
    .real-time-indicator {
        background-color: #4CAF50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        animation: pulse 2s infinite;
    }
    .history-item {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    .copy-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.8rem;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(ttl=300)  # Cache for 5 minutes
def get_stock_info(ticker):
    """Get comprehensive stock information"""
    try:
        stock = yf.Ticker(ticker)
        return stock
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

@st.cache_data(ttl=60)  # Cache for 1 minute for real-time feel
def get_real_time_data(ticker):
    """Get real-time stock data"""
    try:
        stock = yf.Ticker(ticker)
        # Get intraday data for real-time feel
        data = stock.history(period="1d", interval="1m")
        return data
    except Exception as e:
        st.error(f"Error fetching real-time data: {e}")
        return pd.DataFrame()

def calculate_technical_indicators(data):
    """Calculate comprehensive technical indicators"""
    if data.empty:
        return data
    
    # Simple Moving Averages
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    
    # Exponential Moving Averages
    data['EMA_12'] = data['Close'].ewm(span=12).mean()
    data['EMA_26'] = data['Close'].ewm(span=26).mean()
    data['EMA_50'] = data['Close'].ewm(span=50).mean()
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
    data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
    
    # Bollinger Bands
    data['BB_Middle'] = data['Close'].rolling(window=20).mean()
    bb_std = data['Close'].rolling(window=20).std()
    data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
    data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
    
    # Stochastic Oscillator
    low_14 = data['Low'].rolling(window=14).min()
    high_14 = data['High'].rolling(window=14).max()
    data['%K'] = 100 * ((data['Close'] - low_14) / (high_14 - low_14))
    data['%D'] = data['%K'].rolling(window=3).mean()
    
    # Average True Range (ATR)
    data['H-L'] = data['High'] - data['Low']
    data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
    data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=14).mean()
    
    return data

def create_advanced_candlestick_chart(data, title="Stock Price"):
    """Create advanced candlestick chart with volume"""
    if data.empty:
        return go.Figure()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(title, 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="OHLC",
            increasing_line_color='#00C851',
            decreasing_line_color='#ff4444'
        ),
        row=1, col=1
    )
    
    # Add moving averages if available
    if 'SMA_20' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['SMA_20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )
    
    if 'SMA_50' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
    
    # Volume chart
    colors = ['red' if close < open else 'green' 
              for close, open in zip(data['Close'], data['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=600,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig