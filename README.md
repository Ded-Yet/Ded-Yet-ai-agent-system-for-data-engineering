# AI Agent System for Data Engineering

A multi-agent system that answers natural language questions about a database by generating and executing SQL, built on top of a real data engineering pipeline (PostgreSQL, Docker, seeded sample data).

## What it does

Ask a plain-English question about an e-commerce dataset — e.g. *"Which customer has spent the most money?"* — and the system:

1. Understands the database schema
2. Generates a SQL query using Google's Gemini API
3. Runs it against a live PostgreSQL database
4. Returns a clear, natural-language answer

This project is built around the idea that **AI agents are only as good as the data engineering underneath them** — so the focus is on a real pipeline (schema, seeded data, evaluation) rather than just an LLM wrapper.

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
```

## Tech stack

- **Database:** PostgreSQL 16 (Docker)
- **LLM:** Google Gemini API (`gemini-3.6-flash`)
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

### 5. Ask a question
```bash
python src/agents/sql_agent.py
```


## Example

```
Ask a question about the store: Which customer spent the most money?
Dr. Holly Nunez spent the most money, with a total expenditure of $14,865.70.
```

## Evaluation

The agent is tested against a set of 10 hand-written questions covering counts, filters, joins, and aggregations. Each question has a known-correct SQL query; the agent's generated SQL is run and its result compared against the expected result.

```bash
python scripts/run_eval.py
```

**Results:** 20/20 (100%) on the current evaluation set, covering counts, filters, joins, and aggregations.

## Project structure

```
src/
  agents/        # AI agents (SQL generation, result explanation)
scripts/
  schema.sql     # Database schema
  seed_data.py   # Generates realistic fake data
  run_eval.py    # Runs the evaluation suite
tests/
  eval_questions.py  # Evaluation question set
docker-compose.yml   # PostgreSQL container
```