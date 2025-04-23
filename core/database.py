import sqlite3
import os
import re
from config import DB_PATH

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "w").close()
    return sqlite3.connect(DB_PATH)

def ensure_table(guild_id: int):
    table_name = f"memory_{guild_id}"
    if not re.fullmatch(r"[\w]+", table_name):
        raise ValueError("Unsafe table name detected!")

    with get_connection() as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                target TEXT PRIMARY KEY,
                content TEXT
            )
        """)
        conn.commit()
