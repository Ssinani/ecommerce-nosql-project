import mysql.connector
from pymongo import MongoClient
from datetime import datetime

# -----------------------------
# Step 1: Connecting to MySQL
# -----------------------------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_db"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)  # Accessing columns by name

# -----------------------------
# Step 2: Connect to MongoDB
# -----------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_mongo"]
orders_collection = mongo_db["orders"]

# Clearing old data to avoid duplicates
orders_collection.delete_many({})

# -----------------------------
# Step 3: Fetching Orders and Migrate
# -----------------------------
mysql_cursor.execute("""
    SELECT o.id AS order_id, o.order_date, u.id AS user_id, u.name, u.email
    FROM orders o
    JOIN users u ON o.user_id = u.id
""")
orders = mysql_cursor.fetchall()

migrated_count = 0  # Track successful migrations

for order in orders:
    user_id = order["user_id"]

    # Get user addresses
    mysql_cursor.execute("""
        SELECT street, city, country, postal_code
        FROM addresses
        WHERE user_id = %s
    """, (user_id,))
    addresses = mysql_cursor.fetchall()

    # Get items in the order, with product and category info
    mysql_cursor.execute("""
        SELECT 
            oi.product_id,
            p.name AS product_name,
            p.category_id,
            c.name AS category_name,
            oi.quantity,
            oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE oi.order_id = %s
    """, (order["order_id"],))
    items = mysql_cursor.fetchall()

    # Creating the MongoDB document
    mongo_doc = {
        "_id": order["order_id"],
        "order_date": order["order_date"].isoformat() if order["order_date"] else str(datetime.now()),
        "user": {
            "user_id": user_id,
            "name": order["name"],
            "email": order["email"],
            "addresses": addresses
        },
        "items": [
            {
                "product_id": item["product_id"],
                "name": item["product_name"],
                "category": item["category_name"],
                "quantity": item["quantity"],
                "price": float(item["price"])
            } for item in items
        ]
    }

    # Inserting into MongoDB with error handling
    try:
        orders_collection.insert_one(mongo_doc)
        migrated_count += 1
    except Exception as e:
        print(f" Failed to insert order {order['order_id']}: {e}")

# -----------------------------
# Step 4: Done – Show Result and Close
# -----------------------------
print(f" Migration complete. {migrated_count} orders inserted into MongoDB.")

# Cleaning up connections
mysql_cursor.close()
mysql_conn.close()
mongo_client.close()
