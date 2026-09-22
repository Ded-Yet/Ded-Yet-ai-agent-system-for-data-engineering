import random
from datetime import date, timedelta

import psycopg2
from faker import Faker

fake = Faker()
random.seed(42)

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="agent_db",
    user="agent_user",
    password="agent_pass",
)
cur = conn.cursor()

NUM_CUSTOMERS = 50
NUM_PRODUCTS = 30
NUM_ORDERS = 200

categories = ["Electronics", "Clothing", "Home", "Books", "Sports", "Toys"]
statuses = ["completed", "pending", "cancelled", "shipped"]

# Customers
customer_ids = []
for _ in range(NUM_CUSTOMERS):
    name = fake.name()
    email = fake.unique.email()
    signup_date = fake.date_between(start_date="-2y", end_date="today")
    cur.execute(
        "INSERT INTO customers (name, email, signup_date) VALUES (%s, %s, %s) RETURNING customer_id",
        (name, email, signup_date),
    )
    customer_ids.append(cur.fetchone()[0])

# Products
product_ids = []
for _ in range(NUM_PRODUCTS):
    name = fake.word().capitalize() + " " + fake.word().capitalize()
    category = random.choice(categories)
    price = round(random.uniform(5, 500), 2)
    cur.execute(
        "INSERT INTO products (name, category, price) VALUES (%s, %s, %s) RETURNING product_id",
        (name, category, price),
    )
    product_ids.append(cur.fetchone()[0])

# Orders + order_items
for _ in range(NUM_ORDERS):
    customer_id = random.choice(customer_ids)
    order_date = fake.date_between(start_date="-1y", end_date="today")
    status = random.choice(statuses)
    cur.execute(
        "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s) RETURNING order_id",
        (customer_id, order_date, status),
    )
    order_id = cur.fetchone()[0]

    num_items = random.randint(1, 4)
    chosen_products = random.sample(product_ids, num_items)
    for product_id in chosen_products:
        quantity = random.randint(1, 3)
        cur.execute(
            "SELECT price FROM products WHERE product_id = %s", (product_id,)
        )
        price = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, price),
        )

conn.commit()
cur.close()
conn.close()

print("Seed data inserted successfully.")