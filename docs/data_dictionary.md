# Data Dictionary

## customers
- `customer_id`: Unique identifier for a customer.
- `name`: Full name of the customer.
- `email`: Customer's email address. Must be unique. Some older records may have missing emails due to a legacy signup form that didn't require it.
- `signup_date`: The date the customer created their account.

## products
- `product_id`: Unique identifier for a product.
- `name`: Product name.
- `category`: One of: Electronics, Clothing, Home, Books, Sports, Toys.
- `price`: Price in USD. Should always be positive — a price of 0 or less indicates a data entry error.

## orders
- `order_id`: Unique identifier for an order.
- `customer_id`: References the customer who placed the order.
- `order_date`: Date the order was placed.
- `status`: One of: pending, shipped, completed, cancelled.
  - `pending`: Order placed but not yet processed.
  - `shipped`: Order has left the warehouse.
  - `completed`: Order delivered and finalized.
  - `cancelled`: Order was cancelled before shipping.

## order_items
- `order_item_id`: Unique identifier for a line item within an order.
- `order_id`: References the parent order.
- `product_id`: References the product purchased.
- `quantity`: Number of units purchased. Should always be positive.
- `price_at_purchase`: The product's price at the time of purchase (may differ from the product's current price if it changed later).

## customer_summary
- `customer_id`: References the customer this summary is for.
- `total_orders`: Total number of orders this customer has placed.
- `total_spent`: Total amount this customer has spent across all orders.
- `avg_order_value`: Average amount spent per order.
- `last_order_date`: Date of the customer's most recent order. This is a precomputed/derived table, refreshed by running the transformation pipeline — it is not updated automatically when new orders come in.