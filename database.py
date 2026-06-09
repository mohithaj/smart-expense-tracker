"""
database.py - SQLite database connection and schema setup
"""
import sqlite3
import os


DB_NAME = "expenses.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def initialize_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL    NOT NULL CHECK(amount > 0),
            category    TEXT    NOT NULL,
            description TEXT    NOT NULL,
            date        TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"  Database ready: {os.path.abspath(DB_NAME)}")