import csv

from src.ingestion import read_csv_in_chunks


def test_read_csv_in_chunks(tmp_path):

    file_path = tmp_path / "customers.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "customer_id",
            "customer_name",
            "email",
            "age",
            "city"
        ])

        writer.writerow(["101", "Rahul", "rahul@gmail.com", "25", "Hyderabad"])
        writer.writerow(["102", "Anjali", "anjali@gmail.com", "28", "Bangalore"])
        writer.writerow(["103", "Kiran", "kiran@gmail.com", "22", "Chennai"])

    chunks = list(read_csv_in_chunks(file_path, chunk_size=2))

    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1
    assert chunks[0][0]["customer_id"] == "101"


def test_read_empty_csv(tmp_path):

    file_path = tmp_path / "empty.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["customer_id", "customer_name", "email", "age", "city"])

    chunks = list(read_csv_in_chunks(file_path, chunk_size=2))

    assert chunks == []