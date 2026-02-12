![Python](https://img.shields.io/badge/Python-3.12-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Agents-green)
![Architecture](https://img.shields.io/badge/Pattern-Crew-orange)
Agentic Stock Analyzer — CrewAI (Crew Architecture)
Overview

This project implements a multi-agent stock analysis system using CrewAI Crews.

Given a stock ticker (e.g., AAPL), the system coordinates multiple specialized agents to produce a structured Buy / Hold / Sell recommendation.

The purpose of this repository is to demonstrate:

Role-based agent orchestration

Scoped tool access per agent

Declarative YAML configuration

Context-driven task chaining

Structured decision output

This is the Crew-based implementation of the stock analyzer.
A Flow-based implementation will be provided separately for architectural comparison.

Architecture

The system consists of four agents:

1️⃣ Market Agent

Calls price history tool

Computes technical indicators (SMA 20 / 50 / 200)

2️⃣ Fundamentals Agent

Analyzes revenue growth, margins, leverage

Evaluates financial quality metrics

3️⃣ News Agent

Retrieves recent headlines

Assesses sentiment

4️⃣ Decision Agent

Synthesizes prior agent outputs

Produces structured investment recommendation
Repo Structure
src/crewsdem/
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── tools/
│   └── stock_picker.py
├── crew.py
└── main.py

How It Works

Agents are defined in agents.yaml

Tasks are defined in tasks.yaml

Each agent has scoped tools

Tasks can depend on outputs of prior tasks

Final decision agent synthesizes results

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

Key Learnings

During development, we encountered and resolved:

Python interpreter version mismatches

src/ layout packaging issues

CrewAI tool validation errors

Pydantic v2 strict schema enforcement

YAML templating conflicts with JSON examples

This repo reflects real-world agent engineering challenges rather than a toy example.

Crew vs Flow

This implementation uses a Crew architecture, meaning:

Agents operate with role specialization

Tools are scoped per agent

Reasoning emerges from agent collaboration

Orchestration is dynamic

A Flow-based version of this project demonstrates deterministic pipeline orchestration for comparison.

Future Extensions

Replace mock tools with real market APIs

Introduce MCP-based tool server

Add JSON schema validation for final output

Add confidence scoring logic

Deploy as CLI or API service

Author

Built as part of a broader exploration of agentic orchestration strategies across CrewAI, LangGraph, and MCP.