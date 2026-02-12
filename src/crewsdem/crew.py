from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Type

import yaml
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# Your repo shows tools/stock_picker.py
from .tools import stock_picker as local_tools

BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"
AGENTS_YAML = CONFIG_DIR / "agents.yaml"
TASKS_YAML = CONFIG_DIR / "tasks.yaml"


# ----------------------------
# BaseTool wrappers (Pydantic v2 compatible)
# ----------------------------
class PriceHistoryInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker, e.g., AAPL")
    days: int = Field(365, description="Number of days of history to generate")


class PriceHistoryTool(BaseTool):
    name: str = "Price history"
    description: str = "Get mock historical prices for a ticker (returns last_close and series_tail)."
    args_schema: Type[BaseModel] = PriceHistoryInput

    def _run(self, ticker: str, days: int = 365) -> dict:
        return local_tools.get_price_history(ticker=ticker, days=days)

class SMAInput(BaseModel):
    series_tail: List[float] = Field(..., description="Price series tail from price history output")
    window: int = Field(..., description="SMA window size")
    
class SMATool(BaseTool):
    name: str = "Compute SMA"
    description: str = "Compute simple moving average from a numeric series_tail list."
    args_schema: Type[BaseModel] = SMAInput

    def _run(self, series_tail: List[float], window: int) -> float:
        return local_tools.sma(series=series_tail, window=window)


class FinancialsInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker, e.g., AAPL")


class FinancialsTool(BaseTool):
    name: str = "Financials"
    description: str = "Get mock company financial metrics (growth, margins, leverage)."
    args_schema: Type[BaseModel] = FinancialsInput

    def _run(self, ticker: str) -> dict:
        return local_tools.get_financials(ticker=ticker)


class NewsInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker, e.g., AAPL")
    n: int = Field(5, description="Number of headlines to generate")


class NewsTool(BaseTool):
    name: str = "Recent news"
    description: str = "Get mock recent news headlines and a sentiment label."
    args_schema: Type[BaseModel] = NewsInput

    def _run(self, ticker: str, n: int = 5) -> dict:
        return local_tools.get_recent_news(ticker=ticker, n=n)


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    return yaml.safe_load(path.read_text()) or {}


def _build_agents(agents_cfg: Dict[str, Any]) -> Dict[str, Agent]:
    # Instantiate tools once
    price_tool = PriceHistoryTool()
    sma_tool = SMATool()
    fin_tool = FinancialsTool()
    news_tool = NewsTool()

    agent_tools = {
        "market_agent": [price_tool, sma_tool],
        "fundamentals_agent": [fin_tool],
        "news_agent": [news_tool],
        "decision_agent": [],  # synthesis only
    }

    agents: Dict[str, Agent] = {}
    for agent_key, cfg in agents_cfg.items():
        agents[agent_key] = Agent(
            role=cfg.get("role", agent_key),
            goal=cfg.get("goal", ""),
            backstory=cfg.get("backstory", ""),
            allow_delegation=bool(cfg.get("allow_delegation", False)),
            verbose=bool(cfg.get("verbose", True)),
            tools=agent_tools.get(agent_key, []),
        )
    return agents



def _format(template: str, inputs: Dict[str, Any]) -> str:
    # Only substitute {ticker}. Leave any other braces untouched.
    return (template or "").replace("{ticker}", str(inputs.get("ticker", "")))

def _build_tasks(tasks_cfg: Dict[str, Any], agents: Dict[str, Agent], inputs: Dict[str, Any]) -> Dict[str, Task]:
    tasks: Dict[str, Task] = {}

    # Create tasks
    for task_key, cfg in tasks_cfg.items():
        agent_key = cfg.get("agent")
        if agent_key not in agents:
            raise ValueError(f"Task '{task_key}' references unknown agent '{agent_key}'")
        tasks[task_key] = Task(
            description=_format(cfg.get("description", ""), inputs),
            expected_output=cfg.get("expected_output", ""),
            agent=agents[agent_key],
        )

    # Wire contexts
    for task_key, cfg in tasks_cfg.items():
        ctx = cfg.get("context") or []
        if ctx:
            tasks[task_key].context = [tasks[name] for name in ctx]

    return tasks


def build_crew(*, ticker: str, process: Process = Process.sequential) -> Crew:
    agents_cfg = _load_yaml(AGENTS_YAML)
    tasks_cfg = _load_yaml(TASKS_YAML)

    agents = _build_agents(agents_cfg)
    tasks = _build_tasks(tasks_cfg, agents, {"ticker": ticker})

    ordered_tasks: List[Task] = [tasks[k] for k in tasks_cfg.keys()]
    used_agent_keys = {tasks_cfg[t]["agent"] for t in tasks_cfg.keys()}
    ordered_agents: List[Agent] = [agents[k] for k in agents_cfg.keys() if k in used_agent_keys]

    return Crew(
        agents=ordered_agents,
        tasks=ordered_tasks,
        process=process,
        verbose=True,
    )


def run_crew(ticker: str) -> Any:
    crew = build_crew(ticker=ticker, process=Process.sequential)
    return crew.kickoff(inputs={"ticker": ticker})
