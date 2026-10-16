import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents.sql_agent import ask as ask_sql
from agents.log_agent import get_latest_log_entry, explain_quality_report
from agents.rag_agent import answer_question as answer_dictionary
from agents.router_agent import route


def main():
    print("AI Agent System for Data Engineering")
    user_input = input("What would you like to know? ")

    destination = route(user_input)

    if destination == "sql":
        print(ask_sql(user_input))
    elif destination == "quality":
        entry = get_latest_log_entry()
        print(explain_quality_report(entry))
    else:
        print(answer_dictionary(user_input))


if __name__ == "__main__":
    main()