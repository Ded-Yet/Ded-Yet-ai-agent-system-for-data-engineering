import os
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DICTIONARY_PATH = "docs/data_dictionary.md"


def load_sections() -> list[dict]:
    """Split the data dictionary into sections, one per ## heading."""
    with open(DICTIONARY_PATH, "r") as f:
        text = f.read()

    # Split on "## " headings, keeping the heading with its content
    parts = re.split(r"\n(?=## )", text)
    sections = []
    for part in parts:
        part = part.strip()
        if part.startswith("## "):
            title = part.split("\n")[0].replace("## ", "").strip()
            sections.append({"title": title, "content": part})
    return sections

STOP_WORDS = {"the", "what", "does", "mean", "is", "are", "a", "an", "of", "in", "on", "for", "to", "and", "or"}


def retrieve_relevant_sections(question: str, sections: list[dict], top_n: int = 2) -> list[dict]:
    question_lower = question.lower()
    words = [w for w in re.findall(r"\w+", question_lower) if len(w) > 2 and w not in STOP_WORDS]

    scored = []
    for section in sections:
        score = 0
        content_lower = section["content"].lower()
        for word in words:
            if word in content_lower:
                score += 1
        scored.append((score, section))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [section for score, section in scored[:top_n] if score > 0]

def answer_question(question: str) -> str:
    sections = load_sections()
    relevant = retrieve_relevant_sections(question, sections)

    if not relevant:
        return "I couldn't find anything relevant to that in the data dictionary."

    context = "\n\n".join(s["content"] for s in relevant)

    prompt = f"""You are answering questions using ONLY the following data dictionary excerpt. 
Do not use any outside knowledge. If the answer isn't in the excerpt, say so.

Data dictionary excerpt:
{context}

Question: {question}

Answer clearly and concisely, in plain English.
"""
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )
    return interaction.output_text.strip()

if __name__ == "__main__":
    question = input("Ask about the data: ")
    print(answer_question(question))