import time
import ccxt
import pandas as pd
import pandas_ta as ta
import requests
from typesafe_sdk import Choice, Score, TypeSafeClient

# Clients Setup
client = TypeSafeClient()
exchange = ccxt.binance()

# Portfolio Initial Config
WALLET_BALANCE = 1000.0  # $1,000 Demo Funds
TRADE_AMOUNT_USD = 200.0  # $200 per Trade Position
TRADE_DURATION_SEC = 180  # 3 Minutes per Scalp Trade
TOTAL_CYCLES = 10  # 10 Trades * 3 Mins = 30 Minutes Session

trade_history = []


def fetch_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/"
        res = requests.get(url, timeout=5).json()
        return res["data"][0]["value"], res["data"][0]["value_classification"]
    except Exception:
        return "50", "Neutral"


def fetch_orderbook_metrics(symbol="BTC/USDT"):
    try:
        orderbook = exchange.fetch_order_book(symbol, limit=20)
        total_bids = sum([b[1] for b in orderbook["bids"]])
        total_asks = sum([a[1] for a in orderbook["asks"]])
        ratio = round(total_bids / total_asks, 2) if total_asks else 1.0
        return total_bids, total_asks, ratio
    except Exception:
        return 0.0, 0.0, 1.0


def get_live_market_data(symbol="BTC/USDT"):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=60)
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["RSI"] = ta.rsi(df["close"], length=14)
    df["EMA_20"] = ta.ema(df["close"], length=20)
    df["EMA_50"] = ta.ema(df["close"], length=50)

    # MACD
    macd = ta.macd(df["close"])
    macd_hist_col = [c for c in macd.columns if "h" in c.lower()][0]
    df["MACD_hist"] = macd[macd_hist_col]

    # Bollinger Bands
    bb = ta.bbands(df["close"], length=20, std=2)
    bbu_col = [c for c in bb.columns if c.startswith("BBU")][0]
    bbl_col = [c for c in bb.columns if c.startswith("BBL")][0]
    df["BB_upper"] = bb[bbu_col]
    df["BB_lower"] = bb[bbl_col]

    latest = df.iloc[-1]
    _, _, bid_ask_ratio = fetch_orderbook_metrics(symbol)
    fng_val, fng_class = fetch_fear_and_greed()

    market_state = f"""
    === LIVE PAIR: {symbol} (1m Timeframe) ===
    - Current Price: ${latest['close']:.2f}
    - RSI (14): {latest['RSI']:.2f}
    - EMA Trend: EMA_20 (${latest['EMA_20']:.2f}) vs EMA_50 (${latest['EMA_50']:.2f})
    - MACD Histogram: {latest['MACD_hist']:.4f}
    - Orderbook Imbalance: {bid_ask_ratio}
    - Fear & Greed Index: {fng_val}/100 ({fng_class})
    """
    return market_state, latest["close"]


def get_jev_trade_signal(market_state):
    response = client.system_one(
        state=market_state,
        questions={
            "signal": Choice(
                instructions="Determine immediate 1m to 3m scalp trade signal",
                criteria={
                    "buy": "Bullish indicators or buy orderbook dominance present",
                    "sell": "Bearish indicators or sell pressure dominance present",
                    "hold": "No clear momentum or neutral conditions",
                },
            ),
            "confidence": Score(
                instructions="Rate signal conviction",
                criteria=["Low", "Medium", "High"],
            ),
        },
    )
    return response.answers["signal"].choice, response.answers["confidence"].score


def run_30min_scalp_session(symbol="BTC/USDT"):
    global WALLET_BALANCE

    print("================================================================")
    print("      STARTING 30-MINUTE JEV SCALPING SIMULATION SESSION        ")
    print(
        f" Initial Balance: ${WALLET_BALANCE:.2f} | Cycles: {TOTAL_CYCLES} (3 Mins Each)"
    )
    print("================================================================\n")

    for cycle in range(1, TOTAL_CYCLES + 1):
        print(
            f"\n--- [TRADE {cycle}/{TOTAL_CYCLES}] Analyzing Market at {time.strftime('%H:%M:%S')} ---"
        )
        market_state, entry_price = get_live_market_data(symbol)
        signal, conf = get_jev_trade_signal(market_state)

        print(
            f"Entry Price: ${entry_price:.2f} | JEV Signal: {signal.upper()} (Conf: {conf})"
        )

        if signal == "hold":
            print("Signal is HOLD. Skipping trade for this cycle...")
            trade_history.append(
                {
                    "cycle": cycle,
                    "signal": "HOLD",
                    "pnl": 0.0,
                    "result": "SKIPPED",
                }
            )
            time.sleep(TRADE_DURATION_SEC)
            continue

        position_btc = TRADE_AMOUNT_USD / entry_price
        print(
            f"Executed {signal.upper()} position of ${TRADE_AMOUNT_USD} ({position_btc:.6f} BTC)."
        )
        print(f"Waiting {TRADE_DURATION_SEC} seconds (3 mins) for Exit...")

        time.sleep(TRADE_DURATION_SEC)

        # Match Exit Price
        _, exit_price = get_live_market_data(symbol)
        price_diff = exit_price - entry_price

        if signal == "buy":
            pnl_usd = position_btc * price_diff
        else:  # sell
            pnl_usd = position_btc * (-price_diff)

        WALLET_BALANCE += pnl_usd
        result_status = "WIN" if pnl_usd >= 0 else "LOSS"

        trade_history.append(
            {
                "cycle": cycle,
                "signal": signal.upper(),
                "entry": entry_price,
                "exit": exit_price,
                "pnl": pnl_usd,
                "result": result_status,
            }
        )

        print(
            f"Exit Price: ${exit_price:.2f} | PnL: ${pnl_usd:+.2f} ({result_status})"
        )
        print(f"Updated Wallet Balance: ${WALLET_BALANCE:.2f}")

    # ================= 30-MINUTE FINAL SUMMARY REPORT =================
    print("\n\n==========================================================")
    print("          30-MINUTE OVERALL SCALPING REPORT               ")
    print("==========================================================")
    wins = sum(1 for t in trade_history if t["result"] == "WIN")
    losses = sum(1 for t in trade_history if t["result"] == "LOSS")
    skipped = sum(1 for t in trade_history if t["result"] == "SKIPPED")
    total_trades = wins + losses

    total_pnl = WALLET_BALANCE - 1000.0
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0

    print(f"Initial Starting Capital : $1000.00")
    print(f"Final Wallet Balance     : ${WALLET_BALANCE:.2f}")
    print(f"Overall Profit / Loss    : ${total_pnl:+.2f}")
    print(f"Total Scalps Executed    : {total_trades}")
    print(f"Successful Trades (Wins) : {wins}")
    print(f"Failed Trades (Losses)   : {losses}")
    print(f"Skipped Cycles (Hold)    : {skipped}")
    print(f"Strategy Win Rate        : {win_rate:.1f}%")
    print("==========================================================")


if __name__ == "__main__":
    run_30min_scalp_session("BTC/USDT")
