from __future__ import annotations
from dataclasses import dataclass
import random
from datetime import date

def get_price_history(ticker: str, days: int = 365) -> dict:
    prices = []
    p = 100.0 + random.random() * 50
    for _ in range(days):
        p *= (1 + random.uniform(-0.02, 0.02))
        prices.append(round(p, 2))
    return {"ticker": ticker, "days": days, "last_close": prices[-1], "series_tail": prices[-60:]}

def compute_sma(series: list[float], window: int) -> float:
    window = max(1, window)
    if len(series) < window:
        return round(sum(series) / len(series), 2)
    return round(sum(series[-window:]) / window, 2)
def sma(series: list[float], window: int) -> float:
    return compute_sma(series, window)
def get_financials(ticker: str) -> dict:
    return {
        "ticker": ticker,
        "revenue_growth_yoy": round(random.uniform(-0.10, 0.35), 3),
        "gross_margin": round(random.uniform(0.20, 0.75), 3),
        "free_cash_flow_margin": round(random.uniform(-0.05, 0.35), 3),
        "debt_to_equity": round(random.uniform(0.0, 2.5), 2),
    }

def get_recent_news(ticker: str, n: int = 5) -> dict:
    sentiment = random.choice(["positive", "neutral", "negative"])
    headlines = [f"{ticker}: headline {i+1}" for i in range(n)]
    return {"ticker": ticker, "sentiment": sentiment, "headlines": headlines, "asof": str(date.today())}
