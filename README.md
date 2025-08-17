<div align="center">

# 📈 StockGPT  
### *Advanced Stock Market Information App*

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An **interactive, all-in-one stock market dashboard** powered by  
**Streamlit + Yahoo Finance API (`yfinance`) + Plotly**.  

</div>

---

## 🎥 Quick Demo & Screenshots
Try out the live demo here:  

👉 [**Open Streamlit App**](https://tushsharmas-ssgpt.streamlit.app/)


<div align="center">

<!-- Carousel-style screenshots (replace with your actual image paths) -->
<p>
  <img src="assets/demo.gif" alt="App Demo" width="800">
</p>

<table>
  <tr>
    <td><img src="https://github.com/Srinivas26k/ssgpt/blob/docs/update-readme/assets/dashboard.png" width="350" alt="Candlestick Chart"></td>
    <td><img src="https://github.com/Srinivas26k/ssgpt/blob/docs/update-readme/assets/technical_indicators.png" width="350" alt="Technical Indicators"></td>
    <td><img src="https://github.com/Srinivas26k/ssgpt/blob/docs/update-readme/assets/volume_analysis.png" width="350" alt="Volume Analysis"></td>
  </tr>
  <tr>
    <td align="center">Candlestick & Price Chart</td>
    <td align="center">RSI, MACD, SMA, EMA</td>
    <td align="center">Volume Analysis</td>
  </tr>
</table>

</div>

> *Above: Example showing AAPL stock overview, candlestick charts, technical indicators, and financial statements.*

---

## 🚀 Features

- **📊 Real-Time Market Data** – Price, market cap, P/E ratio, dividend yield, etc. (auto-refresh & manual refresh)
- **🕒 Historical & Intraday Charts** – Candlestick, volume, moving averages (SMA, EMA).
- **📈 Technical Indicators** – RSI, MACD, Bollinger Bands, ATR, Stochastic Oscillator.
- **📦 Volume Analysis** – Volume bars, moving average, volume ratio.
- **💼 Financial Statements** – Income statement, balance sheet, cash flow.
- **📢 Market Insights** – Analyst ratings, recent news, earnings calendar.
- **📜 Corporate Actions** – Dividends, stock splits.
- **📑 Options Data** – View call and put options.
- **🌱 ESG & Sustainability** – Company environmental and governance metrics.
- **✨ Interactive UI** – Tabs, charts, and metrics for a modern dashboard experience.

---

## 🛠 Technologies Used

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)

---

## ⚙️ Installation & Setup

> We use [`uv`](https://github.com/astral-sh/uv) for faster package installation and virtual environment management.

### 1️⃣ Install `uv`
```bash
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/stockgpt.git
cd stockgpt
```

### 3️⃣ Create and Activate Virtual Environment

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 4️⃣ Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run tr2.py
```

Then open:

```
http://localhost:8501
```

---

## 📖 Usage

1. Enter a stock ticker (e.g., `AAPL`, `TSLA`, `MSFT`).
2. Browse tabs for:

   * Real-Time Overview & Key Stats
   * Interactive Price & Volume Charts (Candlestick, SMA, EMA)
   * Technical Indicators (RSI, MACD, Bollinger Bands, ATR, Stochastic)
   * Volume Analysis
   * Financial Statements
   * Analyst Ratings & News
   * Options Chain
   * Dividends & Splits
   * ESG Data
   * Earnings History & Calendar
3. Enjoy live, interactive data exploration with auto-refresh and advanced charting.

---

## 📂 Project Structure

```
.
├── tr2.py              # Main Streamlit application (advanced)
├── tr.py               # Basic Streamlit application
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── assets/
    ├── demo.gif        # Demo animation for README
    ├── screenshot1.png # Candlestick chart screenshot
    ├── screenshot2.png # Technical indicators screenshot
    └── screenshot3.png # Volume analysis screenshot
```

---

## 🤝 Contributing

We welcome contributions!
Here’s the process:

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/my-feature

# 3. Commit your changes
git commit -m "Add my new feature"

# 4. Push and open a Pull Request
git push origin feature/my-feature
```

---

## 📬 Issues

**Issues:** [GitHub Issues](https://github.com/tushsharmas/ssgpt/issues)

---
## 👥 Contributors

[![](https://contrib.rocks/image?repo=Srinivas26k/ssgpt)](https://github.com/Srinivas26k/ssgpt/graphs/contributors)

Thanks to these amazing people!

---

## 📜 License

This project is licensed under the MIT License – free to use, modify, and distribute.

---

<div align="center">
  <sub>Built with ❤️ using Python & Streamlit</sub>
</div>

---
