
import sqlite3

from src import database


def test_batch_insert_and_duplicate_detection(tmp_path, monkeypatch):

    test_db = tmp_path / "test_customers.db"

    monkeypatch.setattr(database, "DB_PATH", str(test_db))

    database.create_database()

    customer = {
        "customer_id": 501,
        "customer_name": "Test Customer",
        "email": "test@example.com",
        "age": 25,
        "city": "Hyderabad"
    }

    inserted, duplicates = database.insert_customers_batch(
        [customer, customer]
    )

    assert inserted == 1
    assert duplicates == 1

    with sqlite3.connect(test_db) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

    assert count == 1
