# AI Agent System for Data Engineering

A multi-agent system that answers natural language questions about a database and monitors data quality, built on top of a real data engineering pipeline (PostgreSQL, Docker, seeded sample data).

## What it does

This system has four agents working together: a router that classifies incoming questions, and three specialized agents that handle them.

**1. SQL Agent** — ask a plain-English question about an e-commerce dataset, e.g. *"Which customer has spent the most money?"*, and it:
1. Understands the database schema
2. Generates a SQL query using Google's Gemini API
3. Runs it against a live PostgreSQL database
4. Returns a clear, natural-language answer

**2. Log Analysis Agent** — reads the results of automated data quality checks (nulls, negative prices, invalid references, etc.) and summarizes them in plain English, the way an engineer would report issues to a non-technical manager.

**3. Router Agent** — classifies incoming questions and automatically routes them to the SQL agent or the log analysis agent, so the user never has to pick manually.

**4. RAG Agent** — answers questions about what tables and columns mean (e.g. "what does the status column mean?") by retrieving the relevant section from a data dictionary and generating an answer grounded in that context, rather than guessing.

This project is built around the idea that **AI agents are only as good as the data engineering underneath them** — so the focus is on a real pipeline (schema, seeded data, data quality checks, evaluation) rather than just an LLM wrapper.

## Architecture

```
Question (English)
      │
      ▼
 [Schema context] ──► Gemini API ──► Generated SQL
      │
      ▼
 PostgreSQL (Docker) ──► Query result
      │
      ▼
 Gemini API ──► Natural language answer


Data quality checks ──► quality_log.json ──► Gemini API ──► Plain-English report
```

## Tech stack

- **Database:** PostgreSQL 16 (Docker)
- **LLM:** Google Gemini API (`gemini-3.5-flash-lite`)
- **Language:** Python
- **Testing:** pytest
- **Data generation:** Faker

## Setup

### Prerequisites
- Python 3.11+
- Docker Desktop
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone and set up the environment
```bash
git clone <your-repo-url>
cd ai-data-engineering-agent
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e .
pip install faker psycopg2-binary google-genai python-dotenv
```

### 2. Start the database
```bash
docker compose up -d
```

### 3. Load the schema and sample data
```bash
Get-Content scripts/schema.sql | docker exec -i de_agent_db psql -U agent_user -d agent_db
python scripts/seed_data.py
```

### 4. Add your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

### 5. Run the system
```bash
python src/main.py
```
Just type what you want to know — a router agent automatically figures out whether it's a question about the store data, a data quality check, or a question about what a column/table means, and routes it to the right agent.

## Example

```
Ask a question about the store: Which customer spent the most money?
Dr. Holly Nunez spent the most money, with a total expenditure of $14,865.70.
```

## Evaluation

**SQL Agent** — tested against 20 hand-written questions covering counts, filters, joins, and aggregations. Each question has a known-correct SQL query; the agent's generated SQL is run and its result compared against the expected result.

```bash
python scripts/run_eval.py
```

Typically scores 90-100% (19-20/20) — Gemini's SQL generation isn't fully deterministic, so results vary slightly between runs.

**Router Agent** — tested against 8 example questions to verify it correctly classifies requests as either a SQL question or a data quality question.

```bash
python scripts/run_router_eval.py
```

Scores 8/8 (100%) on the current test set.


**RAG Agent** — tested against 5 questions about table/column meaning, checking whether the answer contains the expected key facts.

```bash
python scripts/run_rag_eval.py
```

Scores 5/5 (100%) on the current test set.

## Project structure

```
src/
  main.py        # Unified entry point with automatic routing
  agents/        # AI agents (SQL generation, result explanation, log analysis, routing)
  pipelines/     # Data quality check pipeline
scripts/
  schema.sql          # Database schema
  seed_data.py        # Generates realistic fake data
  inject_bad_data.py  # Injects known bad rows for testing data quality checks
  run_eval.py         # Runs the SQL agent evaluation suite
  run_router_eval.py  # Runs the router agent evaluation suite
tests/
  eval_questions.py        # SQL agent evaluation questions
  router_eval_questions.py # Router agent evaluation questions
docker-compose.yml     # PostgreSQL container
```