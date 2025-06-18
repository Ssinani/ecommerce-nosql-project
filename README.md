
# E-Commerce Database Migration Project

This project demonstrates the migration of a relational MySQL database to a NoSQL MongoDB database using Python.

## Team members:

- Diana Iljazi
- Sara Sinani

## Project Structure

- `migrate_extended.py` – Python script to migrate and transform relational data into MongoDB  
- `NoSQL_Project_Report.docx` – Full documentation and report  
- `screenshots/` – Visual proof of relational and NoSQL data  
- `ecommerce_schema.sql` – SQL schema  
- `README.md` – Instructions and dependencies  

---

## Relational DB Overview

Database: `ecommerce_db`

Tables:
- `users`
- `addresses`
- `categories`
- `products`
- `orders`
- `order_items`

Populated with data using phpMyAdmin.

## Technologies Used
MongoDB (via Docker container)
MySQL (managed using phpMyAdmin)
Python (for migration scripts)
Visual Studio Code (as the code editor)
Docker (for containerized NoSQL environment)
Graph Generator: Random online graph generation tool

## Dependencies
To run the migration scripts, the following Python libraries are required:

pymysql – Connects Python to MySQL
pymongo – Connects Python to MongoDB
dnspython (optional) – Required if you're using a MongoDB Atlas connection string with mongodb+srv://

## Installation
Install dependencies using pip:

pip install pymysql pymongo dnspython

## NoSQL Database

MongoDB was chosen for:
- Document-based model
- Native support for embedded structures
- Schema flexibility and scalability

Example structure of it:
```json
{
  "_id": 1,
  "order_date": "2024-06-01T10:00:00.000Z",
  "user": {
    "name": "...",
    "addresses": [ ... ]
  },
  "items": [
    {
      "name": "...",
      "category": "..."
    }
  ]
}

# ecommerce-nosql-project
NoSQL project worked with multiple tools.