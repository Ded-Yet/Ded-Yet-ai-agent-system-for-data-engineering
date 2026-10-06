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

    # 1. A customer with a missing email
    cur.execute(
        "INSERT INTO customers (name, email, signup_date) VALUES (%s, %s, %s)",
        ("Test Ghost", "", "2024-01-01"),
    )

    # 2. A product with a negative price (data entry error)
    cur.execute(
        "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
        ("Broken Widget", "Electronics", -15.00),
    )

    # 3. An order_item with a negative quantity (e.g. a bad return record)
    cur.execute("SELECT order_id FROM orders LIMIT 1")
    order_id = cur.fetchone()[0]
    cur.execute("SELECT product_id FROM products LIMIT 1")
    product_id = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
        (order_id, product_id, -2, 19.99),
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Bad data injected for testing.")


if __name__ == "__main__":
    main()