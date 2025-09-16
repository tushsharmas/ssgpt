import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from prediction.linear_regression import predict_stock


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock

def main():
    st.title("Stock Market Information App")

    # User input for stock ticker
    ticker = st.text_input("Enter stock ticker (e.g., AAPL for Apple Inc.):").upper()

    # This is the main block. All code that needs the 'ticker' must be inside it.
    if ticker:
        try:
            stock = get_stock_info(ticker)
            info = stock.info

            # Summary (check if company name exists to validate ticker)
            st.header("Summary")
            st.write(f"Company: {info['longName']}")
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Industry: {info.get('industry', 'N/A')}")
            st.write(f"Current Price: ${info.get('currentPrice', 'N/A')}")

            # Chart - This 'data' variable is used for prediction later
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
            st.subheader("Balance Sheet")
            balance_sheet = stock.balance_sheet
            st.dataframe(balance_sheet)
            st.subheader("Income Statement")
            income_stmt = stock.financials
            st.dataframe(income_stmt)
            st.subheader("Cash Flow")
            cash_flow = stock.cashflow
            st.dataframe(cash_flow)

            # News
            st.header("Recent News")
            news = stock.news
            for item in news[:5]:
                st.write(f"**{item['title']}**")
                st.write(item['link'])
                st.write("---")

            # -------------------------------
            # Stock Price Prediction
            # -------------------------------
            st.header("Future Stock Price Prediction")
            
            # Adding a unique key to the number_input widget
            days = st.number_input("Days to predict:", min_value=1, max_value=30, value=5, key="days_input")

            # Adding a unique key to the button widget
            if st.button("Predict Closing Prices", key="predict_button"):
                with st.spinner("Predicting..."):
                    
                    # Added reset_index() to create the 'Date' column needed for prediction
                    data_for_pred = data.copy() 
                    data_for_pred.reset_index(inplace=True)

                    preds = predict_stock(data_for_pred, days=days)
                    st.subheader("Predicted Closing Prices")
                    st.dataframe(preds)

                    # Plot actual vs predicted
                    fig2, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(data.index, data['Close'], label='Actual Close')
                    ax.plot(preds['Date'], preds['Predicted_Close'], label='Predicted Close', linestyle='--')
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Price")
                    ax.set_title(f"{ticker} Stock Price Prediction")
                    ax.legend()
                    st.pyplot(fig2)

        except (KeyError, IndexError):
            # This will catch errors for invalid tickers (e.g., 'longName' not found)
            st.error("Invalid stock ticker. Please enter a valid symbol (e.g., AAPL, GOOG).")
        except Exception as e:
            # This will catch other potential errors
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
