import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

LOG_PATH = "data/quality_log.json"


def get_latest_log_entry() -> dict:
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()
    return json.loads(lines[-1])


def explain_quality_report(log_entry: dict) -> str:
    prompt = f"""You are a data engineer summarizing a data quality report for a manager who is not technical.

Here are the results of automated checks run on an e-commerce database:

{json.dumps(log_entry, indent=2)}

Write a short, clear summary (3-5 sentences) that:
- States whether the data looks healthy overall
- Calls out any specific issues found, in plain language (no SQL/technical jargon)
- Suggests what should be done next if there are issues

Do not just repeat the raw numbers mechanically — explain what they mean.
"""
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )
    return interaction.output_text.strip()


if __name__ == "__main__":
    entry = get_latest_log_entry()
    summary = explain_quality_report(entry)
    print(summary)