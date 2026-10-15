import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents.sql_agent import ask as ask_sql
from agents.log_agent import get_latest_log_entry, explain_quality_report


def main():
    print("AI Agent System for Data Engineering")
    print("1. Ask a question about the store data")
    print("2. Get a data quality report")
    choice = input("Choose (1 or 2): ").strip()

    if choice == "1":
        question = input("Ask a question about the store: ")
        print(ask_sql(question))
    elif choice == "2":
        entry = get_latest_log_entry()
        print(explain_quality_report(entry))
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()