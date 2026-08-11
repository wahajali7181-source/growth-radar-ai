import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "growthradar.db"

print("DATABASE:")
print(DB_PATH)
print()

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

cursor.execute("""
    SELECT
        id,
        full_name,
        email,
        plan,
        role,
        subscription_status,
        created_at,
        last_login
    FROM users
    ORDER BY id DESC
""")

users = cursor.fetchall()

print("TOTAL USERS:", len(users))
print("-" * 80)

for user in users:

    print(
        f"ID: {user[0]} | "
        f"Name: {user[1]} | "
        f"Email: {user[2]} | "
        f"Plan: {user[3]} | "
        f"Role: {user[4]} | "
        f"Status: {user[5]} | "
        f"Created: {user[6]} | "
        f"Last Login: {user[7]}"
    )

conn.close()