# Moving-Average Crossover Backtest

A classic trend-following strategy in plain Python (standard library only): buy when the fast moving average crosses above the slow one, sell when it crosses below.

## What it does

- Reads `prices.csv` (`date,close`)
- Computes fast/slow simple moving averages (default 10/30 days)
- Trades every crossover and prints each trade
- Compares the strategy's final value with buy-and-hold over the same period

## Usage

```bash
python backtest.py
python backtest.py --file prices.csv --fast 10 --slow 30 --capital 100000
```

## Sample data

`prices.csv` holds 60 days of sample closes: a rising trend, a pullback, then a second rise — so the strategy makes a few real trades instead of sitting out.

## Notes

A learning tool, not investment advice. It ignores trading costs, slippage and dividends, and a 60-day sample proves nothing about a strategy — try it on longer real price history before drawing conclusions.
