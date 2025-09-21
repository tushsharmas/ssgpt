import yfinance as yf
from prediction.linear_regression import predict_stock

# Download last 6 months of Apple stock data
data = yf.download("AAPL", period="6mo")
data.reset_index(inplace=True)

# Run prediction
preds = predict_stock(data, days=5)
print(preds)
