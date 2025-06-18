import mysql.connector
from pymongo import MongoClient
from datetime import datetime

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_db"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_mongo"]
orders_collection = mongo_db["orders"]

orders_collection.delete_many({})

mysql_cursor.execute("""
    SELECT o.id AS order_id, o.order_date, u.id AS user_id, u.name, u.email
    FROM orders o
    JOIN users u ON o.user_id = u.id
""")
orders = mysql_cursor.fetchall()

for order in orders:
    order_id = order["order_id"]

    mysql_cursor.execute("""
        SELECT oi.product_id, p.name AS product_name, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = mysql_cursor.fetchall()

    mongo_order = {
        "_id": order_id,
        "order_date": order["order_date"].isoformat() if order["order_date"] else str(datetime.now()),
        "user": {
            "user_id": order["user_id"],
            "name": order["name"],
            "email": order["email"]
        },
        "items": [
            {
                "product_id": item["product_id"],
                "name": item["product_name"],
                "quantity": item["quantity"],
                "price": float(item["price"])
            } for item in items
        ]
    }

    orders_collection.insert_one(mongo_order)

print("Data migration is complete. Check MongoDB Compass (ecommerce_mongo > orders)")
