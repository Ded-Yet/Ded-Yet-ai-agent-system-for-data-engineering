import json
from datetime import datetime, timezone

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "agent_db",
    "user": "agent_user",
    "password": "agent_pass",
}

LOG_PATH = "data/quality_log.json"


def run_check(cur, name: str, sql: str):
    cur.execute(sql)
    count = cur.fetchone()[0]
    return {"check": name, "issue_count": count}


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    checks = [
        ("orders_with_negative_total",
         """
         SELECT COUNT(*) FROM order_items WHERE price_at_purchase < 0 OR quantity < 0;
         """),
        ("customers_missing_email",
         "SELECT COUNT(*) FROM customers WHERE email IS NULL OR email = '';"),
        ("orders_with_invalid_customer",
         """
         SELECT COUNT(*) FROM orders o
         LEFT JOIN customers c ON o.customer_id = c.customer_id
         WHERE c.customer_id IS NULL;
         """),
        ("products_with_zero_or_negative_price",
         "SELECT COUNT(*) FROM products WHERE price <= 0;"),
    ]

    results = [run_check(cur, name, sql) for name, sql in checks]

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    cur.close()
    conn.close()

    print("Data quality check complete:")
    for r in results:
        print(f"  {r['check']}: {r['issue_count']} issue(s)")


if __name__ == "__main__":
    main()