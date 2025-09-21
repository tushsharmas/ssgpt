import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_stock(df, days=5):
    """
    Predict next 'days' closing prices using Linear Regression.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain at least 'Date' and 'Close' columns.
    days : int
        Number of future days to predict.

    Returns
    -------
    predictions : pandas.DataFrame
        DataFrame with future dates and predicted closing prices.
    """

    # Make sure Date is in datetime format
    df = df[['Date', 'Close']].copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert dates into numeric sequence
    df['Days'] = np.arange(len(df))

    # Features and target
    X = df[['Days']]
    y = df['Close']

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future days
    future_days = np.arange(len(df), len(df) + days).reshape(-1, 1)
    future_dates = pd.date_range(df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=days)

    # Predict
    predictions = model.predict(future_days).flatten()

    # Return as DataFrame
    result = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Close': predictions
    })

    return result
