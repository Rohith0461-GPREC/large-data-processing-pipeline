
import sys
import sqlite3
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import database
from src.pipeline import run_pipeline


def benchmark_pipeline():

    input_file = "data/input/large_customers.csv"
    chunk_sizes = [500, 1000, 5000, 10000]

    original_db_path = database.DB_PATH
    results = []

    print("\nFAIR PIPELINE BENCHMARK")
    print("==============================")

    try:
        for size in chunk_sizes:

            print(f"\nTesting chunk size: {size}")

            benchmark_db = f"data/output/benchmark_{size}.db"

            Path(benchmark_db).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            Path(benchmark_db).unlink(missing_ok=True)

            database.DB_PATH = benchmark_db

            start_time = time.perf_counter()

            run_pipeline(input_file, chunk_size=size)

            execution_time = time.perf_counter() - start_time

            with sqlite3.connect(benchmark_db) as connection:

                row = connection.execute("""
                    SELECT
                        total_records,
                        inserted_records,
                        duplicate_records,
                        rejected_records,
                        peak_memory_mb
                    FROM pipeline_runs
                    ORDER BY rowid DESC
                    LIMIT 1
                """).fetchone()

            results.append({
                "chunk_size": size,
                "execution_time": round(execution_time, 4),
                "total_records": row[0],
                "inserted_records": row[1],
                "duplicates": row[2],
                "rejected": row[3],
                "peak_memory_mb": row[4]
            })

    finally:
        database.DB_PATH = original_db_path

    print("\nFINAL BENCHMARK COMPARISON")
    print("==============================")

    for result in results:

        print(f"\nChunk size: {result['chunk_size']}")
        print(f"Execution time: {result['execution_time']} seconds")
        print(f"Peak memory: {result['peak_memory_mb']} MB")
        print(f"Inserted: {result['inserted_records']}")
        print(f"Duplicates: {result['duplicates']}")
        print(f"Rejected: {result['rejected']}")


if __name__ == "__main__":
    benchmark_pipeline()
