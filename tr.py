import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock

def main():
    st.title("Stock Market Information App")

    # User input for stock ticker
    ticker = st.text_input("Enter stock ticker (e.g., AAPL for Apple Inc.):").upper()

    if ticker:
        stock = get_stock_info(ticker)

        # Summary
        st.header("Summary")
        info = stock.info
        st.write(f"Company: {info['longName']}")
        st.write(f"Sector: {info.get('sector', 'N/A')}")
        st.write(f"Industry: {info.get('industry', 'N/A')}")
        st.write(f"Current Price: ${info.get('currentPrice', 'N/A')}")

        # Chart
        st.header("Chart")
        data = stock.history(period="1y")
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
        st.plotly_chart(fig)

        # Statistics
        st.header("Key Statistics")
        st.write(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
        st.write(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
        st.write(f"EPS (TTM): ${info.get('trailingEps', 'N/A')}")
        st.write(f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")

        # Historical Data
        st.header("Historical Data")
        hist_data = stock.history(period="1mo")
        st.dataframe(hist_data)

        # Financial Statements
        st.header("Financial Statements")
        
        # Balance Sheet
        st.subheader("Balance Sheet")
        balance_sheet = stock.balance_sheet
        st.dataframe(balance_sheet)

        # Income Statement
        st.subheader("Income Statement")
        income_stmt = stock.financials
        st.dataframe(income_stmt)

        # Cash Flow
        st.subheader("Cash Flow")
        cash_flow = stock.cashflow
        st.dataframe(cash_flow)

        # News
        st.header("Recent News")
        news = stock.news
        for item in news[:5]:  # Display top 5 news items
            st.write(f"**{item['title']}**")
            st.write(item['link'])
            st.write("---")

if __name__ == "__main__":
    main()