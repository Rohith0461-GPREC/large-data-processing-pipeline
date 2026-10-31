
import json

from src.ingestion import read_json_in_chunks


def test_read_json_in_chunks(tmp_path):

    file_path = tmp_path / "customers.json"

    customers = [
        {
            "customer_id": "201",
            "customer_name": "Rohit",
            "email": "rohit@gmail.com",
            "age": "25",
            "city": "Hyderabad"
        },
        {
            "customer_id": "202",
            "customer_name": "Sneha",
            "email": "sneha@gmail.com",
            "age": "28",
            "city": "Bangalore"
        },
        {
            "customer_id": "203",
            "customer_name": "Kiran",
            "email": "kiran@gmail.com",
            "age": "22",
            "city": "Chennai"
        }
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(customers, file)

    chunks = list(read_json_in_chunks(file_path, chunk_size=2))

    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1
    assert chunks[0][0]["customer_id"] == "201"
