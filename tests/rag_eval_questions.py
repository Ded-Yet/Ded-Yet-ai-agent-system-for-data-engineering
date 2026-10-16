RAG_EVAL_QUESTIONS = [
    {
        "question": "What does the status column mean?",
        "must_contain": ["pending", "shipped", "completed", "cancelled"],
    },
    {
        "question": "What is price_at_purchase?",
        "must_contain": ["price", "purchase"],
    },
    {
        "question": "What does the customer_id field reference?",
        "must_contain": ["customer"],
    },
    {
        "question": "Is customer_summary updated automatically?",
        "must_contain": ["not", "automatically"],
    },
    {
        "question": "What are the possible product categories?",
        "must_contain": ["electronics", "clothing"],
    },
]