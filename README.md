# 🚀 JEV AI Crypto Scalping Engine

A high-frequency algorithmic crypto scalping simulator built with Python. The JEV Engine combines real-time technical indicators, live order book depth metrics, market sentiment analysis, and LLM-driven decision-making (`typesafe-sdk`) to execute automated paper trades on `BTC/USDT`.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Configuration Parameters](#-configuration-parameters)
- [Execution & Trading Scripts](#-execution--trading-scripts)
- [Trading Strategy & Decision Engine](#-trading-strategy--decision-engine)
- [Performance & Benchmark Results](#-performance--benchmark-results)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [Disclaimer](#-disclaimer)

---

## 🔍 Overview

The **JEV AI Crypto Scalping Engine** is designed to analyze 1-minute cryptocurrency market data in real time, generate high-conviction trade signals (`BUY`, `SELL`, `HOLD`), and simulate trade execution. 

Unlike basic rule-based systems, JEV synthesizes both technical indicators and order book liquidity dynamics to adapt to fast-moving market volatility while incorporating real-world constraints like exchange trading fees and dynamic risk management targets.

---

## ✨ Key Features

- **Live Market Data Fetching**: Retrieves real-time OHLCV candles (`1m` timeframe) directly from Binance using `ccxt`.
- **Advanced Technical Analysis**:
  - **RSI (14)**: Identifies overbought/oversold conditions.
  - **EMA (20 & 50)**: Tracks short-term trend directions and crossovers.
  - **MACD Histogram**: Detects momentum shifts and momentum divergence.
  - **Bollinger Bands**: Measures market volatility and price compression.
- **Orderbook Imbalance Analysis**: Measures bid/ask depth volume ratios from top 20 order book levels to detect buyer or seller dominance.
- **Sentiment Integration**: Fetches real-time crypto market mood using the **Fear & Greed Index** API.
- **AI Decision Model**: Queries `typesafe-sdk` with structured context to get signal predictions along with conviction scores.
- **Realistic Execution Simulation**:
  - **Binance Fee Modeling**: Deducts `0.1%` spot fee on entry and `0.1%` on exit (`0.2%` total round-trip fee).
  - **Dynamic TP/SL Tracking**: Real-time tick monitoring every 10 seconds for Take Profit (`+0.5%`) and Stop Loss (`-0.25%`).
  - **Timeout Protection**: Automatically exits open positions after a maximum holding window (`5 minutes`).

---

## 🛠️ Architecture & Tech Stack

- **Language**: Python 3.10+
- **Exchange Integration**: `ccxt` (Binance API)
- **Data Manipulation**: `pandas`, `pandas_ta`
- **AI / Decision SDK**: `typesafe_sdk`
- **HTTP / External APIs**: `requests`

---

## 📁 Project Structure

```text
jev/
├── myenv/                      # Python Virtual Environment
├── main.py                     # Primary execution entry point
├── multi_paper_trader.py       # Fixed 3-minute hold duration simulator (10 cycles)
├── fee_tp_sl_paper_trader.py   # Advanced simulator (Fees + Dynamic TP/SL + 10s monitoring)
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
