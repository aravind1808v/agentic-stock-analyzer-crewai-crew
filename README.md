![Python](https://img.shields.io/badge/Python-3.12-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Agents-green)
![Architecture](https://img.shields.io/badge/Pattern-Crew-orange)
# Agentic Stock Analyzer — CrewAI (Crew Architecture)
## Overview

This project implements a multi-agent stock analysis system using CrewAI Crews.

Given a stock ticker (e.g., AAPL), the system coordinates multiple specialized agents to produce a structured Buy / Hold / Sell recommendation.

The purpose of this repository is to demonstrate:

1.Role-based agent orchestration

2.Scoped tool access per agent

3.Declarative YAML configuration

4.Context-driven task chaining

5.Structured decision output

This is the Crew-based implementation of the stock analyzer.
A Flow-based implementation will be provided separately for architectural comparison.

##Architecture

The system consists of four agents:

1️⃣ Market Agent

-Calls price history tool

-Computes technical indicators (SMA 20 / 50 / 200)

2️⃣ Fundamentals Agent

-Analyzes revenue growth, margins, leverage

-Evaluates financial quality metrics

3️⃣ News Agent

-Retrieves recent headlines

-Assesses sentiment

4️⃣ Decision Agent

-Synthesizes prior agent outputs

-Produces structured investment recommendation
##Repo Structure
src/crewsdem/
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── tools/
│   └── stock_picker.py
├── crew.py
└── main.py

## How It Works

1.Agents are defined in agents.yaml

2.Tasks are defined in tasks.yaml

3.Each agent has scoped tools

4.Tasks can depend on outputs of prior tasks

5.Final decision agent synthesizes results

Tools are implemented as BaseTool subclasses to ensure compatibility with Pydantic v2 and CrewAI validation requirements.

Installation
1️⃣ Create Virtual Environment
uv venv --python 3.12
source .venv/bin/activate

2️⃣ Install Dependencies
pip install crewai pyyaml

3️⃣ Run the System
export PYTHONPATH="$(pwd)/src"
python -m crewsdem.main --ticker AAPL


This repo reflects real-world agent engineering challenges rather than a toy example.

## Crew vs Flow

This implementation uses a Crew architecture, meaning:

1.Agents operate with role specialization

2.Tools are scoped per agent

3.Reasoning emerges from agent collaboration

4.Orchestration is dynamic

A Flow-based version of this project demonstrates deterministic pipeline orchestration for comparison.

## Future Extensions

1.Replace mock tools with real market APIs

2.Introduce MCP-based tool server

3.Add JSON schema validation for final output

4.Add confidence scoring logic

5.Deploy as CLI or API service

## Author

Built as part of a broader exploration of agentic orchestration strategies across CrewAI, LangGraph, and MCP.