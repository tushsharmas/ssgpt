import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import numpy as np
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure page
st.set_page_config(
    page_title="Advanced Real-Time Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='black')),
        row=4, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Technical Indicators Dashboard",
        template="plotly_white",
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
    
    # Calculate volume indicators
    data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
    data['Volume_Ratio'] = data['Volume'] / data['Volume_SMA']
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Volume vs Moving Average', 'Volume Ratio'),
        row_heights=[0.6, 0.4]
    )
    
    # Volume bars
    colors = ['red' if close < open else 'green' 
              for close, open in zip(data['Close'], data['Open'])]
    
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors, opacity=0.7),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Volume_SMA'], name='Volume SMA(20)', 
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Volume ratio
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Volume_Ratio'], name='Volume Ratio', 
                  line=dict(color='purple')),
        row=2, col=1
    )
    fig.add_hline(y=1.5, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=1.0, line_dash="solid", line_color="gray", row=2, col=1)
    fig.add_hline(y=0.5, line_dash="dash", line_color="green", row=2, col=1)
    
    fig.update_layout(
        title="Volume Analysis",
        template="plotly_white",
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
        st.markdown(f"""
        <div class="metric-container">
            <h3>Key Metrics</h3>
            <p><strong>Market Cap:</strong> ${market_cap/1e9:.1f}B</p>
            <p><strong>P/E:</strong> {pe_ratio}</p>
            <p><strong>Updated:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.title("🚀 Advanced Real-Time Stock Analyzer")
    st.markdown("*Professional-grade stock analysis with real-time updates and advanced technical indicators*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Stock ticker input
        ticker = st.text_input(
            "📊 Stock Ticker", 
            value="AAPL", 
            help="Enter stock symbol (e.g., AAPL, GOOGL, TSLA)"
        ).upper()
        
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
        auto_refresh = st.checkbox("🔄 Auto Refresh (30s)", value=True)
        
        # Refresh button
        if st.button("🔄 Refresh Now"):
            st.cache_data.clear()
    
    if not ticker:
        st.warning("Please enter a stock ticker symbol")
        return
    
    # Auto-refresh logic
    if auto_refresh:
        placeholder = st.empty()
        time.sleep(1)  # Small delay for smooth updates
    
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
        
        chart_tabs = st.tabs([
            "📊 Price & Volume", 
            "🔬 Technical Indicators", 
            "📦 Volume Analysis",
            "📋 Financial Overview"
        ])
        
        with chart_tabs[0]:
            st.subheader("Price Action & Volume")
            if not real_time_data.empty:
                # Show intraday chart for current day
                intraday_chart = create_advanced_candlestick_chart(
                    real_time_data, f"{ticker} - Intraday (1-minute intervals)"
                )
                st.plotly_chart(intraday_chart, use_container_width=True)
            
            # Historical chart
            historical_chart = create_advanced_candlestick_chart(
                historical_data, f"{ticker} - Historical ({selected_period})"
            )
            st.plotly_chart(historical_chart, use_container_width=True)
        
        with chart_tabs[1]:
            st.subheader("Technical Indicators Dashboard")
            tech_chart = create_technical_indicators_chart(historical_data)
            st.plotly_chart(tech_chart, use_container_width=True)
            
            # Technical analysis summary
            if 'RSI' in historical_data.columns:
                latest_rsi = historical_data['RSI'].iloc[-1]
                latest_macd = historical_data['MACD'].iloc[-1]
                latest_signal = historical_data['MACD_Signal'].iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    rsi_signal = "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral"
                    st.metric("RSI (14)", f"{latest_rsi:.1f}", rsi_signal)
                
                with col2:
                    macd_signal = "Bullish" if latest_macd > latest_signal else "Bearish"
                    st.metric("MACD Signal", macd_signal, f"{latest_macd - latest_signal:.4f}")
                
                with col3:
                    if 'ATR' in historical_data.columns:
                        latest_atr = historical_data['ATR'].iloc[-1]
                        st.metric("ATR (14)", f"${latest_atr:.2f}", "Volatility")
        
        with chart_tabs[2]:
            st.subheader("Volume Analysis")
            volume_chart = create_volume_analysis_chart(historical_data)
            st.plotly_chart(volume_chart, use_container_width=True)
        
        with chart_tabs[3]:
            st.subheader("Financial Overview")
            
            # Key financial metrics
            info = stock.info
            
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
        
        # Additional information sections
        if st.expander("📰 Recent News", expanded=False):
            news = stock.news
            if news:
                valid_news_count = 0
                for item in news:
                    # Only show news items with valid titles
                    title = item.get('title', '').strip()
                    if title and title != 'No title' and valid_news_count < 5:
                        st.markdown(f"**{title}**")
                        
                        # Add publication info if available
                        if 'providerPublishTime' in item:
                            try:
                                publish_time = datetime.fromtimestamp(item['providerPublishTime'])
                                publisher = item.get('publisher', 'Unknown')
                                st.caption(f"📅 {publish_time.strftime('%Y-%m-%d %H:%M')} | 🏢 {publisher}")
                            except (ValueError, OSError):
                                # Handle invalid timestamp
                                st.caption(f"🏢 {item.get('publisher', 'Unknown')}")
                        
                        # Add link if available
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
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check the ticker symbol and try again.")
    
    # Auto-refresh implementation
    if auto_refresh:
        time.sleep(30)  # Wait 30 seconds before next refresh
        st.rerun()

if __name__ == "__main__":
    main()