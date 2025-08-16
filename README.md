<div align="center">

# 📈 StockGPT & ✈️ TravelEva
### *Advanced Stock Market Information App & AI Travel Assistant*

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**StockGPT**: An **interactive, all-in-one stock market dashboard** powered by  
**Streamlit + Yahoo Finance API (`yfinance`) + Plotly**.

**TravelEva**: An **AI-powered travel assistant** with history tracking and clipboard functionality.

</div>

---

## 🎥 Quick Demo & Screenshots

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

### 📈 StockGPT Features
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

### ✈️ TravelEva Features
- **🤖 AI Travel Assistant** – Get expert travel advice and recommendations
- **📚 History Feature** – Store and retrieve last 10 question-answer pairs using SQLite
- **📋 Copy-to-Clipboard** – Copy questions, answers, or Q&A pairs with one click
- **🗺️ Travel Categories** – Organized advice for flights, accommodation, destinations, planning, and safety
- **💡 Sample Questions** – Quick-start with common travel questions
- **📱 Responsive Design** – Works seamlessly on desktop and mobile devices
- **🔄 Question Replay** – Easily re-ask questions from your history

---

## 🛠 Technologies Used

### Core Technologies
- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/) - For history storage
- [pyperclip](https://pypi.org/project/pyperclip/) - For clipboard functionality

### StockGPT Specific
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Scikit-learn](https://scikit-learn.org/)

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

## ▶️ Run the Apps

### StockGPT (Stock Market Analysis)
```bash
streamlit run tr2.py
```

### TravelEva (AI Travel Assistant)
```bash
streamlit run traveleva.py
```

Then open:
```
http://localhost:8501
```

---

## 📖 Usage

### 📈 StockGPT Usage
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

### ✈️ TravelEva Usage
1. **Ask Questions**: Type any travel-related question in the text area
2. **Select Category**: Choose from Flights, Accommodation, Destinations, Planning, Safety, etc.
3. **Get AI Advice**: Click "Get Travel Advice" for personalized recommendations
4. **Copy Answers**: Use the copy buttons to save answers to your clipboard
5. **View History**: Check the sidebar for your recent questions and answers
6. **Replay Questions**: Click "Ask Again" from history to re-ask previous questions
7. **Quick Start**: Use sample questions to explore different travel topics

---

## 📂 Project Structure

```
.
├── tr2.py                    # Advanced StockGPT application
├── tr.py                     # Basic StockGPT application
├── tr3.py                    # Enhanced StockGPT with history features
├── traveleva.py              # TravelEva AI Travel Assistant
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── traveleva_history.db      # SQLite database for TravelEva history (auto-created)
├── stock_history.db          # SQLite database for StockGPT history (auto-created)
└── assets/
    ├── demo.gif              # Demo animation for README
    ├── screenshot1.png       # Candlestick chart screenshot
    ├── screenshot2.png       # Technical indicators screenshot
    └── screenshot3.png       # Volume analysis screenshot
```

---

## 🆕 New Features Implementation

### 1. History Feature
- **SQLite Database**: Persistent storage of question-answer pairs
- **Efficient Storage**: Automatically maintains only the last 10 entries to prevent database bloat
- **Sidebar Display**: Easy access to recent questions with expandable details
- **Quick Replay**: One-click to re-ask previous questions
- **Categorized History**: Questions are stored with their categories for better organization

### 2. Copy-to-Clipboard Feature
- **pyperclip Integration**: Reliable clipboard functionality across platforms
- **Multiple Copy Options**: Copy questions, answers, or complete Q&A pairs
- **User Feedback**: Success/error messages for copy operations
- **Fallback Support**: Manual copy option if clipboard access fails
- **Unique Keys**: Proper button key management to prevent conflicts

### 3. Cross-Platform Compatibility
- **Windows**: Full clipboard support with pyperclip
- **macOS**: Native clipboard integration
- **Linux**: X11 clipboard support (requires xclip or xsel)
- **Responsive Design**: Works on desktop and mobile browsers

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
