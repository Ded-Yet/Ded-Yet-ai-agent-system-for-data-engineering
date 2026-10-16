import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "agent_db",
    "user": "agent_user",
    "password": "agent_pass",
}


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Clear old summary data before recomputing (idempotent transform)
    cur.execute("DELETE FROM customer_summary;")

    cur.execute("""
        INSERT INTO customer_summary (customer_id, total_orders, total_spent, avg_order_value, last_order_date)
        SELECT
            c.customer_id,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) AS total_spent,
            COALESCE(SUM(oi.quantity * oi.price_at_purchase) / NULLIF(COUNT(DISTINCT o.order_id), 0), 0) AS avg_order_value,
            MAX(o.order_date) AS last_order_date
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        GROUP BY c.customer_id;
    """)

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM customer_summary;")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    print(f"Transformation complete: {count} customer summary rows created.")


if __name__ == "__main__":
    main()