EVAL_QUESTIONS = [
    {
        "question": "How many customers are there in total?",
        "expected_sql": "SELECT COUNT(*) FROM customers;",
    },
    {
        "question": "How many orders are pending?",
        "expected_sql": "SELECT COUNT(*) FROM orders WHERE status = 'pending';",
    },
    {
        "question": "What is the most expensive product?",
        "expected_sql": "SELECT name FROM products ORDER BY price DESC LIMIT 1;",
    },
    {
        "question": "Which customer has spent the most money in total?",
        "expected_sql": """
            SELECT c.name, SUM(oi.quantity * oi.price_at_purchase) AS total_spent
            FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY c.name
            ORDER BY total_spent DESC
            LIMIT 1;
        """,
    },
    {
        "question": "How many products are in the Electronics category?",
        "expected_sql": "SELECT COUNT(*) FROM products WHERE category = 'Electronics';",
    },
    {
        "question": "What is the total revenue from all completed orders?",
        "expected_sql": """
            SELECT SUM(oi.quantity * oi.price_at_purchase) AS revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.status = 'completed';
        """,
    },
    {
        "question": "How many orders has each customer placed, for the top 3 customers?",
        "expected_sql": """
            SELECT c.name, COUNT(o.order_id) AS order_count
            FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.name
            ORDER BY order_count DESC
            LIMIT 3;
        """,
    },
    {
        "question": "What is the average price of products in the Books category?",
        "expected_sql": "SELECT AVG(price) FROM products WHERE category = 'Books';",
    },
    {
        "question": "How many orders were cancelled?",
        "expected_sql": "SELECT COUNT(*) FROM orders WHERE status = 'cancelled';",
    },
    {
        "question": "Which product category has the highest total revenue?",
        "expected_sql": """
            SELECT p.category
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.category
            ORDER BY SUM(oi.quantity * oi.price_at_purchase) DESC
            LIMIT 1;
        """,
    },
]