import sqlite3
import pandas as pd

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        website TEXT,
        phone TEXT,
        address TEXT,

        city TEXT,
        business_type TEXT,

        lead_score INTEGER,
        opportunity TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_businesses(df):

    if df is None:
        print("Database: DataFrame is None")
        return

    if df.empty:
        print("Database: DataFrame Empty")
        return

    # Required database columns
    required_columns = [
        "name",
        "website",
        "phone",
        "address",
        "city",
        "business_type",
        "lead_score",
        "opportunity"
    ]

    # Create missing columns
    for col in required_columns:

        if col not in df.columns:

            if col == "lead_score":
                df[col] = 0

            else:
                df[col] = ""

    # Keep only database columns
    df = df[required_columns].copy()

    # Replace NaN values
    df = df.fillna("")

    print("\n========== DATABASE DEBUG ==========")
    print(df.head())
    print(df.columns.tolist())
    print("Rows:", len(df))
    print("====================================\n")

    conn = get_connection()

    try:

        df.to_sql(
            "businesses",
            conn,
            if_exists="append",
            index=False
        )

        conn.commit()

        print(f"✅ Saved {len(df)} businesses successfully.")

    except Exception as e:

        print("❌ Database Save Error")
        print(e)

    finally:

        conn.close()


def load_businesses():

    conn = get_connection()

    try:

        df = pd.read_sql(
            "SELECT * FROM businesses",
            conn
        )

    except Exception as e:

        print(e)
        df = pd.DataFrame()

    finally:

        conn.close()

    return df


def total_businesses():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM businesses"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def clear_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM businesses"
    )

    conn.commit()

    conn.close()