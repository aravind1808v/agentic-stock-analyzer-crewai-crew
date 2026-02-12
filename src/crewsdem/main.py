# src/crewsdem/main.py
from __future__ import annotations

import os
import argparse

from .crew import run_crew


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CrewAI Stock Analyzer (Crew demo)")
    parser.add_argument(
        "--ticker",
        type=str,
        default=os.getenv("TICKER", "AAPL"),
        help="Stock ticker symbol (default: AAPL or $TICKER env var)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_crew(args.ticker)
    print(result)


if __name__ == "__main__":
    main()
