import streamlit as st
import pandas as pd
import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('traveleva_history.db')
query = "SELECT * FROM history"  # Change table name if needed
try:
    df = pd.read_sql_query(query, conn)
except Exception as e:
    st.error(f"Error loading history: {e}")
    df = pd.DataFrame()
conn.close()

st.title("Export History")

if not df.empty:
    st.write("Preview of history:", df.head())
    format = st.selectbox("Select export format", ["CSV", "JSON"])
    if format == "CSV":
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download history as CSV",
            data=csv,
            file_name="history.csv",
            mime="text/csv"
        )
    else:
        json_data = df.to_json(orient="records")
        st.download_button(
            label="Download history as JSON",
            data=json_data,
            file_name="history.json",
            mime="application/json"
        )
else:
    st.info("No history data available to export.")
