import os
import psycopg2
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "agent_db",
    "user": "agent_user",
    "password": "agent_pass",
}

SCHEMA_TEXT = """
Tables:

customers(customer_id, name, email, signup_date)
products(product_id, name, category, price)
orders(order_id, customer_id, order_date, status)
order_items(order_item_id, order_id, product_id, quantity, price_at_purchase)

Relationships:
orders.customer_id -> customers.customer_id
order_items.order_id -> orders.order_id
order_items.product_id -> products.product_id
"""


def get_schema_text() -> str:
    return SCHEMA_TEXT


def generate_sql(question: str) -> str:
    prompt = f"""You are a SQL expert. Given this PostgreSQL schema:

{get_schema_text()}

Write a single PostgreSQL query to answer this question:
"{question}"

Rules:
- Return ONLY the SQL query, no explanation, no markdown formatting, no backticks.
- Use only the tables and columns listed above.
"""
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )
    sql = interaction.output_text.strip()
    return sql


if __name__ == "__main__":
    question = "How many orders are pending?"
    sql = generate_sql(question)
    print("Generated SQL:")
    print(sql)