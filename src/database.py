
import sqlite3
from pathlib import Path


DB_PATH = "data/output/customers.db"


def create_database():
    """Create customer and pipeline run tables."""

    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id TEXT PRIMARY KEY,
                input_file TEXT NOT NULL,
                start_time TEXT,
                end_time TEXT,
                total_records INTEGER,
                inserted_records INTEGER,
                duplicate_records INTEGER,
                rejected_records INTEGER,
                execution_time_seconds REAL,
                peak_memory_mb REAL,
                status TEXT
            )
        """)


def insert_customers_batch(customers):
    """Insert multiple customers using one database connection."""

    if not customers:
        return 0, 0

    inserted = 0
    duplicates = 0

    with sqlite3.connect(DB_PATH) as connection:

        for customer in customers:

            cursor = connection.execute("""
                INSERT OR IGNORE INTO customers
                (customer_id, customer_name, email, age, city)
                VALUES (?, ?, ?, ?, ?)
            """, (
                customer["customer_id"],
                customer["customer_name"],
                customer["email"],
                customer["age"],
                customer["city"]
            ))

            if cursor.rowcount == 1:
                inserted += 1
            else:
                duplicates += 1

    return inserted, duplicates


def save_pipeline_run(run_data):
    """Save pipeline execution metrics."""

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            INSERT INTO pipeline_runs (
                run_id,
                input_file,
                start_time,
                end_time,
                total_records,
                inserted_records,
                duplicate_records,
                rejected_records,
                execution_time_seconds,
                peak_memory_mb,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_data["run_id"],
            run_data["input_file"],
            run_data["start_time"],
            run_data["end_time"],
            run_data["total_records"],
            run_data["inserted_records"],
            run_data["duplicate_records"],
            run_data["rejected_records"],
            run_data["execution_time_seconds"],
            run_data["peak_memory_mb"],
            run_data["status"]
        ))
