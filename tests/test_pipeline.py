import json
import sqlite3
import pytest

from src.pipeline import run_pipeline
from src import database


def test_json_pipeline(tmp_path, monkeypatch):

    test_db = tmp_path / "test_pipeline.db"
    input_file = tmp_path / "customers.json"

    monkeypatch.setattr(database, "DB_PATH", str(test_db))

    customers = [
        {
            "customer_id": "901",
            "customer_name": "Test User",
            "email": "test@example.com",
            "age": "25",
            "city": "Hyderabad"
        },
        {
            "customer_id": "902",
            "customer_name": "Another User",
            "email": "another@example.com",
            "age": "28",
            "city": "Bangalore"
        }
    ]

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(customers, file)

    run_pipeline(str(input_file), chunk_size=1)

    with sqlite3.connect(test_db) as connection:

        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        run_count = connection.execute(
            "SELECT COUNT(*) FROM pipeline_runs"
        ).fetchone()[0]

    assert count == 2
    assert run_count == 1


def test_idempotent_processing(tmp_path, monkeypatch):

    test_db = tmp_path / "idempotency.db"
    input_file = tmp_path / "customers.json"

    monkeypatch.setattr(database, "DB_PATH", str(test_db))

    customers = [
        {
            "customer_id": "951",
            "customer_name": "Test Customer",
            "email": "test@example.com",
            "age": "25",
            "city": "Hyderabad"
        },
        {
            "customer_id": "952",
            "customer_name": "Another Customer",
            "email": "another@example.com",
            "age": "28",
            "city": "Bangalore"
        }
    ]

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(customers, file)

    # First execution
    run_pipeline(str(input_file), chunk_size=2)

    # Second execution with the same input
    run_pipeline(str(input_file), chunk_size=2)

    with sqlite3.connect(test_db) as connection:

        customer_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        run_metrics = connection.execute("""
            SELECT inserted_records, duplicate_records, status
            FROM pipeline_runs
            ORDER BY rowid
        """).fetchall()

    assert customer_count == 2

    assert run_metrics[0] == (2, 0, "SUCCESS")
    assert run_metrics[1] == (0, 2, "SUCCESS")


def test_missing_input_file():

    with pytest.raises(FileNotFoundError):
        run_pipeline("data/input/missing_test.csv")


def test_invalid_chunk_size():

    with pytest.raises(ValueError, match="Chunk size"):
        run_pipeline("data/input/customers.csv", chunk_size=0)


def test_malformed_json(tmp_path, monkeypatch):

    test_db = tmp_path / "invalid_json.db"
    input_file = tmp_path / "invalid.json"

    monkeypatch.setattr(database, "DB_PATH", str(test_db))

    input_file.write_text(
        '[{"customer_id": 901, "customer_name": "Test"',
        encoding="utf-8"
    )

    with pytest.raises(Exception):
        run_pipeline(str(input_file))

    with sqlite3.connect(test_db) as connection:

        result = connection.execute(
            "SELECT status FROM pipeline_runs"
        ).fetchone()

    assert result is not None
    assert result[0] == "FAILED"