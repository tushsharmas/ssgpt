import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import numpy as np
import requests
import plotly.io as pio
from tr import predict_stock
import matplotlib.pyplot as plt
import urllib.request


# ---------- STATIC IMPORTANT STOCKS ----------
IMPORTANT_STOCKS = [
    "AAPL - Apple Inc.",
    "MSFT - Microsoft Corporation",
    "GOOGL - Alphabet Inc. (Class A)",
    "GOOG - Alphabet Inc. (Class C)",
    "AMZN - Amazon.com Inc.",
    "META - Meta Platforms Inc.",
    "NVDA - NVIDIA Corporation",
    "TSLA - Tesla, Inc.",
    "BRK.B - Berkshire Hathaway Inc. (B)",
    "UNH - UnitedHealth Group Inc.",
    "JPM - JPMorgan Chase & Co.",
    "JNJ - Johnson & Johnson",
    "V - Visa Inc.",
    "MA - Mastercard Inc.",
    "PG - Procter & Gamble Co.",
    "XOM - Exxon Mobil Corporation",
    "LLY - Eli Lilly and Company",
    "HD - Home Depot Inc.",
    "AVGO - Broadcom Inc.",
    "COST - Costco Wholesale Corporation",
    "NFLX - Netflix, Inc.",
    "DIS - The Walt Disney Company",
    "WMT - Walmart Inc.",
    "BAC - Bank of America Corporation",
    "KO - The Coca-Cola Company",
    "ADBE - Adobe Inc.",
    "PEP - PepsiCo, Inc.",
    "CRM - Salesforce, Inc.",
    "INTC - Intel Corporation",
    "MCD - McDonald's Corporation",
]

@st.cache_data
def search_yahoo_stocks(query):
    try:
        if not query:
            return IMPORTANT_STOCKS
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=20&newsCount=0"
        headers = {"User-Agent": "Mozilla/5.0"}
        data = requests.get(url, headers=headers).json()
        results = [
            f"{q['symbol']} - {q.get('shortname') or q.get('longname','')}"
            for q in data.get("quotes", [])
            if q.get("symbol") and (q.get("shortname") or q.get("longname"))
        ]
        return results or IMPORTANT_STOCKS
    except Exception:
        return IMPORTANT_STOCKS

      

# Custom Plotly templates for light/dark modes
_light_plotly_template = go.layout.Template(
    layout=dict(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#0b1220"),
        legend=dict(font=dict(color="#0b1220")),
        xaxis=dict(title=dict(font=dict(color="#0b1220")), tickfont=dict(color="#0b1220")),
        yaxis=dict(title=dict(font=dict(color="#0b1220")), tickfont=dict(color="#0b1220"))
    )
)

_dark_plotly_template = go.layout.Template(
    layout=dict(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#e6eef8"),
        legend=dict(font=dict(color="#e6eef8")),
        xaxis=dict(title=dict(font=dict(color="#e6eef8")), tickfont=dict(color="#e6eef8")),
        yaxis=dict(title=dict(font=dict(color="#e6eef8")), tickfont=dict(color="#e6eef8"))
    )
)

pio.templates["custom_light"] = _light_plotly_template
pio.templates["custom_dark"] = _dark_plotly_template

# Light/dark mode CSS definitions
_light_css = """
    <style>
    /* Light theme - comprehensive styling */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        color: #0b1220 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] > div {
        background-color: #f7f9fb !important;
        color: #0b1220 !important;
    }

    /* All text elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown p, .stText, label, span, .stCaption,
    [data-testid="stSidebar"] * {
        color: #0b1220 !important;
    }

    /* Metric containers */
    .metric-container {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        color: #0b1220 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }

    /* Inputs and controls */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stRadio > label,
    .stCheckbox > label {
        background-color: #ffffff !important;
        color: #0b1220 !important;
        border: 1px solid #dcdcdc !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffffff !important;
        color: #0b1220 !important;
        border: 1px solid #dcdcdc !important;
    }
    .stButton > button:hover {
        background-color: #f1f5f9 !important;
    }

    /* Alerts and messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #0b1220 !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }

    /* Links */
    a { color: #0a66ff !important; }

    /* Plotly container background */
    .plotly-graph-div .main-svg { 
        background-color: #ffffff !important; 
    }
        /* Tab styling for light mode */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa !important;
        border-radius: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #0b1220 !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0a66ff !important;
        background-color: #ffffff !important;
        border-radius: 4px !important;
        border-bottom: 2px solid #0a66ff !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #0a66ff !important;
        background-color: #f1f5f9 !important;
    }
    input::placeholder {
        color: rgba(80, 80, 80, 0.8) !important;
        font-style: italic !important;
        opacity: 1 !important;
    }
    header, [data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: #ffffff !important;
}

    </style>
"""

_dark_css = """
    <style>
    /* Dark theme styling */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
        color: #e6eef8 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] > div {
        background-color: #262730 !important;
        color: #e6eef8 !important;
    }

    /* All text elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown p, .stText, label, span, .stCaption,
    [data-testid="stSidebar"] * {
        color: #e6eef8 !important;
    }

    /* Metric containers */
    .metric-container {
        background: linear-gradient(135deg, #1e2130, #262730) !important;
        border: 1px solid #404040 !important;
        color: #e6eef8 !important;
    }

    /* Inputs and controls */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stRadio > label,
    .stCheckbox > label {
        background-color: #262730 !important;
        color: #e6eef8 !important;
        border: 1px solid #404040 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #262730 !important;
        color: #e6eef8 !important;
        border: 1px solid #404040 !important;
    }
    .stButton > button:hover {
        background-color: #3a3b4a !important;
    }

    /* Alerts and messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #e6eef8 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    /* Links */
    a { color: #7fb4ff !important; }

    /* Plotly container background */
    .plotly-graph-div .main-svg { 
        background-color: #0e1117 !important; 
    }
    /* Tab styling for dark mode */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2130 !important;
        border-radius: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #e6eef8 !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #7fb4ff !important;
        background-color: #262730 !important;
        border-radius: 4px !important;
        border-bottom: 2px solid #7fb4ff !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #7fb4ff !important;
        background-color: #2d303e !important;
    }
    header, [data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: #0e1117 !important;
}

    </style>
"""

# ==========================
# Company Name/Ticker Search (Autocomplete Feature)
# ==========================

@st.cache_data(ttl=3600)
def fetch_ticker_suggestions(query, max_results=5):
    """
    Fetch matching tickers and company names using Yahoo Finance autocompletion API.
    Returns a list of tuples: (symbol, name, exchange)
    """
    if not query or len(query) < 2:
        return []  # Don't spam API for short queries

    url = (
        f"https://query2.finance.yahoo.com/v1/finance/search"
        f"?q={query}&quotesCount={max_results}&newsCount=0&lang=en"
    )
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code != 200:
            return []
        data = resp.json()
        suggestions = []
        for item in data.get("quotes", []):
            symbol = item.get("symbol")
            name = item.get("shortname") or item.get("longname") or ""
            exch = item.get("exchange", "")
            # Filter out cryptocurrencies and funds for relevance
            if item.get("quoteType") in ("EQUITY", "ETF"):
                suggestions.append((symbol, name, exch))
        return suggestions[:max_results]
    except Exception:
        return []





# ==========================
# Portfolio Tracker (Watchlist) Feature
# ==========================

def get_watchlist():
    if "watchlist" not in st.session_state:
        st.session_state["watchlist"] = []
    return st.session_state["watchlist"]

def add_to_watchlist(ticker):
    watchlist = get_watchlist()
    ticker = ticker.upper().strip()
    if ticker and ticker not in watchlist:
        watchlist.append(ticker)
        st.session_state["watchlist"] = watchlist

def remove_from_watchlist(ticker):
    watchlist = get_watchlist()
    ticker = ticker.upper().strip()
    if ticker in watchlist:
        watchlist.remove(ticker)
        st.session_state["watchlist"] = watchlist

def display_watchlist(selected_ticker_callback=None):
    st.sidebar.markdown("## 📋 My Watchlist")
    watchlist = get_watchlist()
    if not watchlist:
        st.sidebar.info("Your watchlist is empty. Add stocks to track them here!")
        return
    tickers_data = {}
    for ticker in watchlist:
        try:
            stock = yf.Ticker(ticker)
            price = stock.info.get("regularMarketPrice", None)
            prev = stock.info.get("regularMarketPreviousClose", None)
            daychg = None
            pctchg = None
            if price is not None and prev is not None and prev != 0:
                daychg = price - prev
                pctchg = (daychg / prev) * 100
            tickers_data[ticker] = {
                "price": price,
                "daychg": daychg,
                "pctchg": pctchg
            }
        except Exception:
            tickers_data[ticker] = {"price": None, "daychg": None, "pctchg": None}
    for ticker in watchlist:
        data = tickers_data[ticker]
        label = f"**{ticker}**"
        if data["price"] is not None:
            label += f" ${data['price']:.2f} "
            if data["daychg"] is not None:
                emoji = "🟢" if data["daychg"] >= 0 else "🔴"
                label += f"{emoji} {data['daychg']:+.2f} ({data['pctchg']:+.2f}%)"
        else:
            label += " -"
        cols = st.sidebar.columns([0.7, 0.15, 0.15])
        with cols[0]:
            if st.button(label, key=f"goto_{ticker}"):
                if selected_ticker_callback:
                    selected_ticker_callback(ticker)
                else:
                    st.session_state["selected_ticker"] = ticker
        with cols[1]:
            st.markdown("")
        with cols[2]:
            if st.button("❌", key=f"rm_{ticker}"):
                current_mode = st.session_state.get("dark_mode", False)
                current_tab = st.session_state.get("active_tab", 0)
                remove_from_watchlist(ticker)
                st.session_state["dark_mode"] = current_mode
                st.session_state["active_tab"] = current_tab
                st.rerun()
                
# ==========================
# Configure page
# ==========================
st.set_page_config(
    page_title="Advanced Real-Time Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
        template=pio.templates.default,
        height=600,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def create_technical_indicators_chart(data):
    """Create comprehensive technical indicators chart"""
    if data.empty or 'RSI' not in data.columns:
        return go.Figure()
    
    # Create subplots for multiple indicators
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('RSI', 'MACD', 'Stochastic Oscillator', 'Bollinger Bands'),
        row_heights=[0.2, 0.2, 0.2, 0.4]
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')),
        row=1, col=1
    )
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=1, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="gray", row=1, col=1)
    
    # MACD
    fig.add_trace(
        go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='blue')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal', line=dict(color='red')),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=data.index, y=data['MACD_Histogram'], name='Histogram', opacity=0.7),
        row=2, col=1
    )
    
    # Stochastic Oscillator
    if '%K' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['%K'], name='%K', line=dict(color='blue')),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['%D'], name='%D', line=dict(color='red')),
            row=3, col=1
        )
        fig.add_hline(y=80, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="green", row=3, col=1)
    
    # Bollinger Bands with Price
    fig.add_trace(
        go.Scatter(x=data.index, y=data['BB_Upper'], name='BB Upper', line=dict(color='red', dash='dash')),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['BB_Middle'], name='BB Middle', line=dict(color='orange')),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['BB_Lower'], name='BB Lower', line=dict(color='red', dash='dash')),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name='Close Price'),
        row=4, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Technical Indicators Dashboard",
        template=pio.templates.default,
        height=800,
        showlegend=True
    )
    
    # Update y-axis ranges
    fig.update_yaxes(range=[0, 100], row=1, col=1)  # RSI
    fig.update_yaxes(range=[0, 100], row=3, col=1)  # Stochastic
    
    return fig

def create_volume_analysis_chart(data):
    """Create advanced volume analysis chart"""
    if data.empty:
        return go.Figure()
    
    # Create a copy to avoid modifying the original data
    volume_data = data.copy()
    
    # Calculate volume indicators
    volume_data['Volume_SMA'] = volume_data['Volume'].rolling(window=20).mean()
    
    # Avoid division by zero
    volume_data['Volume_Ratio'] = np.where(
        volume_data['Volume_SMA'] > 0,
        volume_data['Volume'] / volume_data['Volume_SMA'],
        0
    )
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Volume vs Moving Average', 'Volume Ratio'),
        row_heights=[0.6, 0.4]
    )
    
    # Volume bars
    colors = ['red' if close < open else 'green' 
              for close, open in zip(volume_data['Close'], volume_data['Open'])]
    
    fig.add_trace(
        go.Bar(x=volume_data.index, y=volume_data['Volume'], name='Volume', marker_color=colors, opacity=0.7),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=volume_data.index, y=volume_data['Volume_SMA'], name='Volume SMA(20)', 
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Volume ratio
    fig.add_trace(
        go.Scatter(x=volume_data.index, y=volume_data['Volume_Ratio'], name='Volume Ratio', 
                  line=dict(color='purple')),
        row=2, col=1
    )
    fig.add_hline(y=1.5, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=1.0, line_dash="solid", line_color="gray", row=2, col=1)
    fig.add_hline(y=0.5, line_dash="dash", line_color="green", row=2, col=1)
    
    fig.update_layout(
        title="Volume Analysis",
        template=pio.templates.default,
        height=500
    )
    
    return fig

def display_real_time_metrics(stock_info, current_data):
    """Display real-time metrics in an attractive format"""
    if current_data.empty:
        return
    
    current_price = current_data['Close'].iloc[-1]
    prev_close = stock_info.info.get('regularMarketPreviousClose', current_price)
    change = current_price - prev_close
    change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
    
    # Real-time indicator
    st.markdown('<span class="real-time-indicator">🔴 LIVE</span>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        color_class = "positive" if change >= 0 else "negative"
        st.markdown(f"""
        <div class="metric-container">
            <h3>Current Price</h3>
            <h2 class="{color_class}">${current_price:.2f}</h2>
            <p class="{color_class}">
                {'▲' if change >= 0 else '▼'} ${abs(change):.2f} ({change_pct:+.2f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        day_high = current_data['High'].max()
        day_low = current_data['Low'].min()
        st.markdown(f"""
        <div class="metric-container">
            <h3>Day Range</h3>
            <p><strong>High:</strong> ${day_high:.2f}</p>
            <p><strong>Low:</strong> ${day_low:.2f}</p>
            <p><strong>Range:</strong> ${day_high - day_low:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_volume = current_data['Volume'].sum()
        avg_volume = stock_info.info.get('averageVolume', 0)
        volume_ratio = total_volume / avg_volume if avg_volume > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <h3>Volume</h3>
            <p><strong>Today:</strong> {total_volume:,}</p>
            <p><strong>Avg:</strong> {avg_volume:,}</p>
            <p><strong>Ratio:</strong> {volume_ratio:.2f}x</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        market_cap = stock_info.info.get('marketCap', 0)
        pe_ratio = stock_info.info.get('trailingPE', 'N/A')
        
        # Format market cap safely
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            if market_cap >= 1e12:
                market_cap_str = f"${market_cap/1e12:.1f}T"
            elif market_cap >= 1e9:
                market_cap_str = f"${market_cap/1e9:.1f}B"
            elif market_cap >= 1e6:
                market_cap_str = f"${market_cap/1e6:.1f}M"
            else:
                market_cap_str = f"${market_cap:,.0f}"
        else:
            market_cap_str = "N/A"
            
        st.markdown(f"""
        <div class="metric-container">
            <h3>Key Metrics</h3>
            <p><strong>Market Cap:</strong> {market_cap_str}</p>
            <p><strong>P/E:</strong> {pe_ratio}</p>
            <p><strong>Updated:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)

def stock_heatmap_chart(tickers):
    data = yf.download(tickers, period="5d")['Close']
    pct_change = data.pct_change().iloc[-1] * 100

    heatmap_df = pd.DataFrame({
        'Stock': pct_change.index,
        'Change (%)': pct_change.values
    })

    fig = px.imshow(
        [heatmap_df['Change (%)'].values],
        labels=dict(x="Stock", y="", color="Change (%)"),
        x=heatmap_df['Stock'],
        y=["Performance"],
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(title="Stock Market Heatmap")
    return fig
def main():
    st.title("🚀 Advanced Real-Time Stock Analyzer")
    st.markdown("*Professional-grade stock analysis with real-time updates and advanced technical indicators*")

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
       
    # --- Portfolio Tracker Sidebar ---
    def set_selected_ticker(ticker):
        st.session_state["selected_ticker"] = ticker

    display_watchlist(selected_ticker_callback=set_selected_ticker)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Initialize dark_mode in session_state if it doesn't exist
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = False
        dark_mode = st.checkbox("🌙 Dark mode", 
                              key="dark_mode", 
                              value=st.session_state.get("dark_mode", False),
                              help="Toggle UI dark theme")
        
        # Apply theme CSS and Plotly template based on dark_mode
        if dark_mode:
            st.markdown(_dark_css, unsafe_allow_html=True)
            pio.templates.default = "custom_dark"
        else:
            st.markdown(_light_css, unsafe_allow_html=True)
            pio.templates.default = "custom_light"

       # ---------- MAIN DROPDOWN LOGIC ----------
        st.write("### Select or search for a stock")

        query = st.text_input(
            "Type a company or symbol", value="", placeholder="Zoom, PayPal, NIO, etc."
        ).strip()

        options = search_yahoo_stocks(query)
        selected = st.selectbox("Or select from dropdown", options, index=0)
        ticker = selected.split(" - ")[0].strip()


        # Validate ticker format
        if ticker and not ticker.replace('-', '').replace('.', '').isalnum():
            st.warning("⚠️ Please enter a valid ticker symbol (letters, numbers, hyphens, and dots only)")
            ticker = ""
        
        # Watchlist add button
        if ticker and st.button("⭐ Add to Watchlist", key="add_watchlist"):
            add_to_watchlist(ticker)
            st.success(f"{ticker} added to watchlist!")

        # Time period selection
        period_options = {
            "1 Day": "1d",
            "5 Days": "5d", 
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y"
        }
        selected_period = st.selectbox("📅 Time Period", list(period_options.keys()), index=6)
        period = period_options[selected_period]
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto Refresh (30s)", value=False)
        
        # Refresh button
        if st.button("🔄 Refresh Now"):
            st.cache_data.clear()
            st.cache_resource.clear()

    # If ticker in session_state due to sidebar selection, override
    if "selected_ticker" in st.session_state and st.session_state["selected_ticker"]:
        ticker = st.session_state.pop("selected_ticker")

    if not ticker:
        st.warning("Please enter a stock ticker symbol")
        return
    
    # Auto-refresh implementation using session state
    if auto_refresh:
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        current_time = time.time()
        if current_time - st.session_state.last_refresh >= 30:
            st.session_state.last_refresh = current_time
            st.cache_data.clear()
            st.rerun()
    
    try:
        # Get stock information
        with st.spinner(f"📈 Loading data for {ticker}..."):
            stock = get_stock_info(ticker)
            if not stock:
                return
                
            # Get historical data
            historical_data = stock.history(period=period)
            if historical_data.empty:
                st.error("No data available for this ticker")
                return
                
            # Calculate technical indicators
            historical_data = calculate_technical_indicators(historical_data)
                
            # Get real-time intraday data
            real_time_data = get_real_time_data(ticker)
            
        # Company header
        company_name = stock.info.get('longName', ticker)
        sector = stock.info.get('sector', 'N/A')
        st.subheader(f"📈 {company_name} ({ticker})")
        st.caption(f"Sector: {sector}")
             
        # Real-time metrics
        st.header("📊 Real-Time Overview")
        if not real_time_data.empty:
            display_real_time_metrics(stock, real_time_data)
        else:
            st.warning("Real-time data not available, showing latest market data")
            display_real_time_metrics(stock, historical_data.tail(1))
            
        # Main charts section
        st.header("📈 Advanced Charts")
            
        tab_names = [
            "📊 Price & Volume", 
            "🔬 Technical Indicators", 
            "📦 Volume Analysis",
            "📋 Financial Overview",
            "🌡️ Market Heatmap"
        ]
        chart_tabs = st.tabs(tab_names)
            
        try:
            with chart_tabs[0]:
                st.subheader("Price Action & Volume")
                if not real_time_data.empty:
                    intraday_chart = create_advanced_candlestick_chart(
                        real_time_data, f"{ticker} - Intraday (1-minute intervals)"
                    )
                    st.plotly_chart(intraday_chart, use_container_width=True)
                historical_chart = create_advanced_candlestick_chart(
                    historical_data, f"{ticker} - Historical ({selected_period})"
                )
                st.plotly_chart(historical_chart, use_container_width=True)
                    
            with chart_tabs[1]:
                st.subheader("Technical Indicators Dashboard")
                tech_chart = create_technical_indicators_chart(historical_data)
                st.plotly_chart(tech_chart, use_container_width=True)
                    
                # Technical analysis summary
                if 'RSI' in historical_data.columns and not historical_data['RSI'].empty:
                    latest_rsi = historical_data['RSI'].iloc[-1]
                    latest_macd = historical_data['MACD'].iloc[-1]
                    latest_signal = historical_data['MACD_Signal'].iloc[-1]
                        
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if not pd.isna(latest_rsi):
                            rsi_signal = "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral"
                            st.metric("RSI (14)", f"{latest_rsi:.1f}", rsi_signal)
                        else:
                            st.metric("RSI (14)", "N/A", "Insufficient data")
                        
                    with col2:
                        if not pd.isna(latest_macd) and not pd.isna(latest_signal):
                            macd_signal = "Bullish" if latest_macd > latest_signal else "Bearish"
                            st.metric("MACD Signal", macd_signal, f"{latest_macd - latest_signal:.4f}")
                        else:
                            st.metric("MACD Signal", "N/A", "Insufficient data")
                        
                    with col3:
                        if 'ATR' in historical_data.columns and not historical_data['ATR'].empty:
                            latest_atr = historical_data['ATR'].iloc[-1]
                            if not pd.isna(latest_atr):
                                st.metric("ATR (14)", f"${latest_atr:.2f}", "Volatility")
                            else:
                                st.metric("ATR (14)", "N/A", "Insufficient data")
                
            with chart_tabs[2]:
                st.subheader("Volume Analysis")
                volume_chart = create_volume_analysis_chart(historical_data)
                st.plotly_chart(volume_chart, use_container_width=True)
            
            with chart_tabs[3]:
                st.subheader("Financial Overview")
                    
                # Key financial metrics
                info = stock.info
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check the ticker symbol and try again.")
    
            selected_tickers = st.multiselect(
                "Select stocks to include in heatmap",
                options=default_tickers,
                default=default_tickers
            )
            if selected_tickers:
                heatmap_fig = stock_heatmap_chart(selected_tickers)
                st.plotly_chart(heatmap_fig, use_container_width=True)
            else:
                st.info("Please select at least one stock to display the heatmap.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check the ticker symbol and try again.")
                
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("Market Cap", info.get('marketCap', 0), "B", 1e9),
            ("Revenue", info.get('totalRevenue', 0), "B", 1e9),
            ("P/E Ratio", info.get('trailingPE', 0), "", 1),
            ("Dividend Yield", info.get('dividendYield', 0), "%", 100),
            ("ROE", info.get('returnOnEquity', 0), "%", 100),
            ("Profit Margin", info.get('profitMargins', 0), "%", 100),
            ("Debt/Equity", info.get('debtToEquity', 0), "", 1),
            ("Beta", info.get('beta', 0), "", 1)
        ]

        for i, (label, value, suffix, divisor) in enumerate(metrics):
            col = [col1, col2, col3, col4][i % 4]
            with col:
                if isinstance(value, (int, float)) and value != 0:
                    formatted_value = f"{value/divisor:.2f}{suffix}" if divisor > 1 else f"{value:.2f}{suffix}"
                else:
                    formatted_value = "N/A"
                st.metric(label, formatted_value)

        with chart_tabs[4]:  # Market Heatmap tab
            st.subheader("Stock Market Heatmap")

            # Default list of tickers
            default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA"]

            # User selects tickers
            selected_tickers = st.multiselect(
                "Select stocks to include in heatmap",
                options=default_tickers,
                default=default_tickers
            )
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check the ticker symbol and try again.")

        if selected_tickers:
            heatmap_fig = stock_heatmap_chart(selected_tickers)
            st.plotly_chart(heatmap_fig, use_container_width=True)
        else:
            st.info("Please select at least one stock to display the heatmap.")
        
    # Additional information sections
    if st.expander("📰 Recent News", expanded=False):
        news = stock.news
        if news:
            valid_news_count = 0
            for item in news:
                title = item.get('title', '').strip()
                if title and title != 'No title' and valid_news_count < 5:
                    st.markdown(f"**{title}**")
                        
                    if 'providerPublishTime' in item:
                        try:
                            publish_time = datetime.fromtimestamp(item['providerPublishTime'])
                            publisher = item.get('publisher', 'Unknown')
                            st.caption(f"📅 {publish_time.strftime('%Y-%m-%d %H:%M')} | 🏢 {publisher}")
                        except (ValueError, OSError):
                            st.caption(f"🏢 {item.get('publisher', 'Unknown')}")
                        
                    if 'link' in item and item['link']:
                        st.markdown(f"[Read more]({item['link']})")
                        
                    st.divider()
                    valid_news_count += 1
                
            if valid_news_count == 0:
                st.info("No recent news with valid titles available")
        else:
            st.info("No recent news available")
        
    if st.expander("🏢 Company Information", expanded=False):
        st.write(info.get('longBusinessSummary', 'No company information available.'))
            
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A'):,}")
            st.write(f"**Founded:** {info.get('startDate', 'N/A')}")
            
        with col2:
            st.write(f"**Website:** {info.get('website', 'N/A')}")
            st.write(f"**Country:** {info.get('country', 'N/A')}")
            st.write(f"**Currency:** {info.get('currency', 'N/A')}")
               
    # -------------------------------   
    # Stock Price Prediction
    # ----------------------------

    st.header("🔮 Future Stock Price Prediction")

    days = st.number_input("Days to predict:", min_value=1, max_value=30, value=5, key="days_input")
    predict_button = st.button("Predict Closing Prices", key="predict_button")

    if predict_button:
        with st.spinner("Predicting..."):
            try:
                ticker_symbol = st.session_state.get("autocomplete", "").strip()

                if not ticker_symbol:
                    st.warning("Please enter a valid stock ticker symbol first.")
                else:
                    stock = yf.Ticker(ticker_symbol)
                    data = stock.history(period="1y")

                    if data.empty:
                        st.error(f"Not enough historical data for '{ticker_symbol}' to make a prediction.")
                    else:
                        data.reset_index(inplace=True)
                        preds = predict_stock(data, days=days)

                        st.subheader(f"Predicted Closing Prices for {ticker_symbol.upper()}")
                        st.dataframe(preds)
                        st.subheader("Prediction Chart")
                        fig2, ax = plt.subplots(figsize=(10, 5))
                        plot_data= data
                    # Plot historical data
                        ax.plot(plot_data.index, plot_data['Close'], label='Actual Close')

                    # Plot predicted data
                        ax.plot(preds['Date'], preds['Predicted_Close'], label='Predicted Close', linestyle='--')
                    
                        ax.set_xlabel("Date")
                        ax.set_ylabel("Price")
                        ax.set_title(f"{ticker_symbol} Stock Price Prediction")
                        ax.legend()
                        st.pyplot(fig2)
                    # --- END OF PLOTTING CODE ---
            except Exception as e:
                st.error(f"Prediction failed. Error: {e}")

                if "No data found" in str(e) or "Invalid ticker" in str(e):
                    st.info("💡 **Tips:**")
                    st.info("• Make sure the ticker symbol is correct (e.g., AAPL, GOOGL, TSLA)")
                    st.info("• Some stocks may not have real-time data available")
                    st.info("• Try a major stock exchange symbol")
      

if __name__ == "__main__":
    main()


