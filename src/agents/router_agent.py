import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def route(user_input: str) -> str:
    prompt = f"""You are a router for a data system with two capabilities:

1. "sql" — answering questions about the store's data (customers, orders, products, revenue, counts, etc.)
2. "quality" — reporting on data quality issues (missing fields, bad prices, broken records, "is the data healthy", etc.)

Given this user input, respond with ONLY one word: either "sql" or "quality".

User input: "{user_input}"
"""
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )
    decision = interaction.output_text.strip().lower()
    return "quality" if "quality" in decision else "sql"


if __name__ == "__main__":
    test_input = input("Say something: ")
    print(f"Routed to: {route(test_input)}")



def route(user_input: str) -> str:
    prompt = f"""You are a router for a data system with three capabilities:

1. "sql" — answering questions about the store's data (customers, orders, products, revenue, counts, etc.)
2. "quality" — reporting on data quality issues (missing fields, bad prices, broken records, "is the data healthy", etc.)
3. "dictionary" — explaining what a column or table means, or clarifying definitions/terminology (e.g. "what does X column mean", "what's the difference between X and Y")

Given this user input, respond with ONLY one word: "sql", "quality", or "dictionary".

User input: "{user_input}"
"""
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )
    decision = interaction.output_text.strip().lower()
    if "dictionary" in decision:
        return "dictionary"
    if "quality" in decision:
        return "quality"
    return "sql"