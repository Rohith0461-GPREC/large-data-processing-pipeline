
import csv
import ijson
from pathlib import Path


def read_csv_in_chunks(file_path, chunk_size=1000):
    """
    Read a CSV file in smaller chunks.
    """

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        while True:
            rows = []

            for _ in range(chunk_size):
                row = next(reader, None)

                if row is None:
                    break

                rows.append(row)

            if not rows:
                break

            yield rows


def read_json_in_chunks(file_path, chunk_size=1000):
    """
    Stream JSON records in smaller chunks using ijson.
    Expects a JSON array of customer objects.
    """

    with open(file_path, mode="rb") as file:

        records = ijson.items(file, "item")

        while True:
            chunk = []

            for _ in range(chunk_size):
                record = next(records, None)

                if record is None:
                    break

                chunk.append(record)

            if not chunk:
                break

            yield chunk
