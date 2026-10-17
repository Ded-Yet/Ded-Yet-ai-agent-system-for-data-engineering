import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st

from agents.sql_agent import ask as ask_sql
from agents.log_agent import get_latest_log_entry, explain_quality_report
from agents.rag_agent import answer_question as answer_dictionary
from agents.router_agent import route

st.set_page_config(page_title="AI Agent System for Data Engineering")

st.title("AI Agent System for Data Engineering")
st.write("Ask a question about the store data, the data quality, or what a column/table means.")

user_input = st.text_input("What would you like to know?")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        destination = route(user_input)

        if destination == "sql":
            answer = ask_sql(user_input)
        elif destination == "quality":
            entry = get_latest_log_entry()
            answer = explain_quality_report(entry)
        else:
            answer = answer_dictionary(user_input)

    st.caption(f"Routed to: {destination}")
    st.write(answer)