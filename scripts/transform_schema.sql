CREATE TABLE IF NOT EXISTS customer_summary (
    customer_id INTEGER PRIMARY KEY REFERENCES customers(customer_id),
    total_orders INTEGER NOT NULL,
    total_spent NUMERIC(12, 2) NOT NULL,
    avg_order_value NUMERIC(12, 2) NOT NULL,
    last_order_date DATE
);