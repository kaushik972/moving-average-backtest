"""Moving-average crossover backtest.

Reads prices.csv (date,close), computes a fast and a slow simple
moving average, trades the crossover (buy when fast crosses above
slow, sell when it crosses below) and compares the strategy with
buy-and-hold.

Usage:
    python backtest.py
    python backtest.py --file prices.csv --fast 10 --slow 30 --capital 100000
"""
import argparse
import csv


def load(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            rows.append((row["date"], float(row["close"])))
    rows.sort()
    return rows


def sma(values, window):
    out = [None] * len(values)
    for i in range(window - 1, len(values)):
        out[i] = sum(values[i - window + 1:i + 1]) / window
    return out


def main():
    p = argparse.ArgumentParser(description="Moving-average crossover backtest")
    p.add_argument("--file", default="prices.csv")
    p.add_argument("--fast", type=int, default=10)
    p.add_argument("--slow", type=int, default=30)
    p.add_argument("--capital", type=float, default=100000.0)
    a = p.parse_args()
    rows = load(a.file)
    closes = [c for _, c in rows]
    fast = sma(closes, a.fast)
    slow = sma(closes, a.slow)
    cash = a.capital
    shares = 0.0
    trades = []
    start = max(a.fast, a.slow)
    prev_diff = None
    for i in range(start, len(rows)):
        diff = fast[i] - slow[i]
        if prev_diff is not None:
            if prev_diff <= 0 < diff and shares == 0:
                shares = cash / closes[i]
                cash = 0.0
                trades.append((rows[i][0], "BUY", closes[i], shares))
            elif prev_diff >= 0 > diff and shares > 0:
                cash = shares * closes[i]
                trades.append((rows[i][0], "SELL", closes[i], shares))
                shares = 0.0
        prev_diff = diff
    if shares > 0:
        cash = shares * closes[-1]
        trades.append((rows[-1][0], "SELL (end)", closes[-1], shares))
        shares = 0.0
    final_value = cash
    strategy_return = final_value / a.capital - 1
    buy_hold = closes[-1] / closes[0] - 1
    print(f"Data: {len(rows)} days, {rows[0][0]} to {rows[-1][0]}")
    print(f"Strategy: MA({a.fast}) / MA({a.slow}) crossover, capital {a.capital:,.0f}")
    for date, side, price, qty in trades:
        print(f"  {date} {side:11} @ {price:8.2f}  ({qty:,.2f} shares)")
    print(f"Trades: {len(trades)}")
    print(f"Strategy final value: {final_value:,.2f} ({strategy_return:+.2%})")
    print(f"Buy-and-hold return:  {buy_hold:+.2%} "
          f"(final {a.capital * (1 + buy_hold):,.2f})")


if __name__ == "__main__":
    main()
