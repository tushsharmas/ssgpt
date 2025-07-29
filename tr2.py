import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock

def plot_price_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title="Stock Price Chart", xaxis_title="Date", yaxis_title="Price")
    return fig

def plot_volume_chart(data):
    fig = px.bar(data, x=data.index, y='Volume', title='Trading Volume')
    return fig

def calculate_moving_averages(data):
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    return data

def plot_moving_averages(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-day MA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], mode='lines', name='200-day MA'))
    fig.update_layout(title="Price with Moving Averages", xaxis_title="Date", yaxis_title="Price")
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("Advanced Stock Market Information App")

    ticker = st.text_input("Enter stock ticker (e.g., AAPL for Apple Inc.):").upper()

    if ticker:
        stock = get_stock_info(ticker)
        info = stock.info

        # Summary
        st.header("Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Company: {info['longName']}")
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Industry: {info.get('industry', 'N/A')}")
        with col2:
            st.write(f"Current Price: ${info.get('currentPrice', 'N/A')}")
            st.write(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
            st.write(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
        with col3:
            st.write(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.write(f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
            st.write(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")

        # Charts
        st.header("Charts")
        data = stock.history(period="1y")
        
        tab1, tab2, tab3 = st.tabs(["Price Chart", "Volume Chart", "Moving Averages"])
        
        with tab1:
            st.plotly_chart(plot_price_chart(data), use_container_width=True)
        
        with tab2:
            st.plotly_chart(plot_volume_chart(data), use_container_width=True)

        with tab3:
            ma_data = calculate_moving_averages(data)
            st.plotly_chart(plot_moving_averages(ma_data), use_container_width=True)

        # Financial Metrics
        st.header("Financial Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Valuation Measures")
            st.write(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
            st.write(f"Enterprise Value: ${info.get('enterpriseValue', 'N/A'):,}")
            st.write(f"Trailing P/E: {info.get('trailingPE', 'N/A')}")
            st.write(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
            st.write(f"PEG Ratio: {info.get('pegRatio', 'N/A')}")
            st.write(f"Price/Sales: {info.get('priceToSalesTrailing12Months', 'N/A')}")
            st.write(f"Price/Book: {info.get('priceToBook', 'N/A')}")
        with col2:
            st.subheader("Financial Highlights")
            st.write(f"Profit Margin: {info.get('profitMargins', 'N/A')}")
            st.write(f"Operating Margin: {info.get('operatingMargins', 'N/A')}")
            st.write(f"Return on Assets: {info.get('returnOnAssets', 'N/A')}")
            st.write(f"Return on Equity: {info.get('returnOnEquity', 'N/A')}")
            st.write(f"Revenue Growth: {info.get('revenueGrowth', 'N/A')}")
            st.write(f"Earnings Growth: {info.get('earningsGrowth', 'N/A')}")

        # Financial Statements
        st.header("Financial Statements")
        
        tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
        
        with tab1:
            st.subheader("Income Statement")
            income_stmt = stock.financials
            st.dataframe(income_stmt)
        
        with tab2:
            st.subheader("Balance Sheet")
            balance_sheet = stock.balance_sheet
            st.dataframe(balance_sheet)
        
        with tab3:
            st.subheader("Cash Flow")
            cash_flow = stock.cashflow
            st.dataframe(cash_flow)

        # Analyst Recommendations
        st.header("Analyst Recommendations")
        recommendations = stock.recommendations
        if not recommendations.empty:
            st.dataframe(recommendations)
        else:
            st.write("No analyst recommendations available.")

        # News
        # News
        # News
        st.header("Recent News")
        news = stock.news
        for item in news[:5]:  # Display top 5 news items
            st.subheader(item.get('title', 'No title available'))
            if 'source' in item:
                st.write(f"Source: {item['source']}")
            if 'providerPublishTime' in item:
                st.write(f"Published: {datetime.fromtimestamp(item['providerPublishTime'])}")
            if 'link' in item:
                st.write(item['link'])
            st.write("---")
        # Technical Analysis
        st.header("Technical Analysis")

        # RSI Calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        st.subheader("Relative Strength Index (RSI)")
        fig_rsi = px.line(x=data.index, y=rsi, title='RSI (14-day)')
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        st.plotly_chart(fig_rsi, use_container_width=True)

        # MACD Calculation
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        st.subheader("Moving Average Convergence Divergence (MACD)")
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=data.index, y=macd, name="MACD"))
        fig_macd.add_trace(go.Scatter(x=data.index, y=signal, name="Signal"))
        fig_macd.add_trace(go.Bar(x=data.index, y=histogram, name="Histogram"))
        fig_macd.update_layout(title="MACD, Signal and Histogram")
        st.plotly_chart(fig_macd, use_container_width=True)

        # Bollinger Bands
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['20d_std'] = data['Close'].rolling(window=20).std()
        data['Upper_BB'] = data['MA20'] + (data['20d_std'] * 2)
        data['Lower_BB'] = data['MA20'] - (data['20d_std'] * 2)

        st.subheader("Bollinger Bands")
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['Upper_BB'], name="Upper BB"))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['MA20'], name="MA20"))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['Lower_BB'], name="Lower BB"))
        fig_bb.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Close"))
        fig_bb.update_layout(title="Bollinger Bands")
        st.plotly_chart(fig_bb, use_container_width=True)

        # Options Chain
        st.header("Options Chain")
        expiration_dates = stock.options

        if expiration_dates:
            selected_date = st.selectbox("Select expiration date", expiration_dates)
            options = stock.option_chain(selected_date)
            
            st.subheader("Call Options")
            st.dataframe(options.calls)
            
            st.subheader("Put Options")
            st.dataframe(options.puts)
        else:
            st.write("No options data available for this stock.")

          # Major Holders
        st.header("Major Holders")
        major_holders = stock.major_holders
        if not major_holders.empty:
            st.dataframe(major_holders)
        else:
            st.write("No major holders data available.")

        # Institutional Holders
        st.header("Institutional Holders")
        institutional_holders = stock.institutional_holders
        if not institutional_holders.empty:
            st.dataframe(institutional_holders)
        else:
            st.write("No institutional holders data available.")

        # Dividends
        st.header("Dividends")
        dividends = stock.dividends
        if not dividends.empty:
            fig_div = px.line(x=dividends.index, y=dividends.values, title='Dividend History')
            st.plotly_chart(fig_div, use_container_width=True)
        else:
            st.write("No dividend data available.")

        # Stock Splits
        st.header("Stock Splits")
        splits = stock.splits
        if not splits.empty:
            st.dataframe(splits)
        else:
            st.write("No stock split data available.")

        # Company Info
        st.header("Company Information")
        st.write(info.get('longBusinessSummary', 'No company information available.'))

        # Sustainability
        st.header("Sustainability")
        sustainability = stock.sustainability
        if sustainability is not None:
            st.dataframe(sustainability)
        else:
            st.write("No sustainability data available.")

        # Earnings
        st.header("Earnings")
        earnings = stock.earnings
        if not earnings.empty:
            fig_earnings = go.Figure()
            fig_earnings.add_trace(go.Bar(x=earnings.index, y=earnings['Earnings'], name='Earnings'))
            fig_earnings.add_trace(go.Bar(x=earnings.index, y=earnings['Revenue'], name='Revenue'))
            fig_earnings.update_layout(title='Earnings and Revenue History', barmode='group')
            st.plotly_chart(fig_earnings, use_container_width=True)
        else:
            st.write("No earnings data available.")

        # Earnings Calendar
        st.header("Earnings Calendar")
        earnings_dates = stock.earnings_dates
        if not earnings_dates.empty:
            st.dataframe(earnings_dates)
        else:
            st.write("No earnings calendar data available.")

if __name__ == "__main__":
    main()        
