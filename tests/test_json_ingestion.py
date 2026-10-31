import json

from src.ingestion import read_json_in_chunks


def test_read_json_in_chunks(tmp_path):

    file_path = tmp_path / "customers.json"

    customers = [
        {"customer_id": "201", "customer_name": "Rohit"},
        {"customer_id": "202", "customer_name": "Sneha"},
        {"customer_id": "203", "customer_name": "Kiran"}
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(customers, file)

    chunks = list(read_json_in_chunks(file_path, chunk_size=2))

    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1
    assert chunks[0][0]["customer_id"] == "201"


def test_read_empty_json_array(tmp_path):

    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")

    chunks = list(read_json_in_chunks(file_path, chunk_size=2))

    assert chunks == []


def test_read_single_json_record(tmp_path):

    file_path = tmp_path / "single.json"

    file_path.write_text(
        '[{"customer_id": "201", "customer_name": "Priya"}]',
        encoding="utf-8"
    )

    chunks = list(read_json_in_chunks(file_path, chunk_size=2))

    assert len(chunks) == 1
    assert len(chunks[0]) == 1
    assert chunks[0][0]["customer_id"] == "201"

def test_json_null_record_does_not_stop_streaming(tmp_path):

    file_path = tmp_path / "null_record.json"

    file_path.write_text(
        '[{"customer_id": "301"}, null, {"customer_id": "302"}]',
        encoding="utf-8"
    )

    chunks = list(read_json_in_chunks(file_path, chunk_size=2))

    assert len(chunks) == 2
    assert chunks[0][0]["customer_id"] == "301"
    assert chunks[0][1] is None
    assert chunks[1][0]["customer_id"] == "302"