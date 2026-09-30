# 🚀 JEV AI Crypto Scalping Engine

An automated real-time crypto scalping simulator built in Python that combines Technical Analysis (TA), Binance Orderbook Imbalance metrics, market sentiment, and AI decision-making.

---

## ✨ Features

- **Real-Time Data Integration**: Fetches live candles (`1m`), order book depth (bids/asks ratio), and Fear & Greed Index.
- **Technical Indicators**: Calculates RSI, EMA (20/50), MACD, and Bollinger Bands using `pandas_ta`.
- **AI Signal Generation**: Uses `typesafe_sdk` (JEV System) to synthesize market state into actionable `BUY`, `SELL`, or `HOLD` signals.
- **Risk Management**: Dynamic Take Profit (`+0.5%`) and Stop Loss (`-0.25%`) tracking with multi-cycle execution.
- **Exchange Fee Simulation**: Accurately accounts for Binance Spot trading fees (`0.1%` per order side) for realistic PnL evaluation.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/jev-scalping-engine.git](https://github.com/your-username/jev-scalping-engine.git)
cd jev-scalping-engine
