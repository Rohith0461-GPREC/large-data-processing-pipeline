
import csv
import tracemalloc
from pathlib import Path

from src.ingestion import read_csv_in_chunks, read_json_in_chunks
from src.validation import validate_customer, validate_schema
from src.transformation import transform_customer
from src.database import (
    create_database,
    insert_customers_batch,
    save_pipeline_run
)
from src.monitoring import (
    create_run_id,
    get_timestamp,
    setup_logging,
    start_monitoring,
    stop_monitoring
)


def run_pipeline(file_path, chunk_size=1000):

    logger = setup_logging()
    run_id = create_run_id()

    start_time = get_timestamp()
    monitor_start = None

    total_records = 0
    inserted_records = 0
    rejected_records = 0
    duplicate_records = 0
    schema_checked = False

    rejected_file = f"data/rejected/rejected_{run_id}.csv"

    try:
        input_path = Path(file_path)

        # Check input file
        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file not found: {file_path}"
            )

        if not input_path.is_file():
            raise ValueError("Input path is not a file.")

        # Validate chunk size
        if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer.")

        # Identify file format
        file_extension = input_path.suffix.lower()

        if file_extension == ".csv":
            read_chunks = read_csv_in_chunks
        elif file_extension == ".json":
            read_chunks = read_json_in_chunks
        else:
            raise ValueError(
                "Unsupported file format. Use CSV or JSON."
            )

        logger.info(f"Pipeline started. Run ID: {run_id}")

        create_database()
        Path(rejected_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        monitor_start = start_monitoring()

        for chunk in read_chunks(file_path, chunk_size):

            if not schema_checked:

                is_valid_schema, schema_error = validate_schema(
                    chunk[0].keys()
                )

                if not is_valid_schema:
                    raise ValueError(schema_error)

                schema_checked = True

                logger.info("Input schema validation passed")

            valid_batch = []

            for row in chunk:

                total_records += 1

                is_valid, error = validate_customer(row)

                if not is_valid:

                    rejected_records += 1

                    file_exists = Path(rejected_file).exists()

                    with open(
                        rejected_file,
                        "a",
                        newline="",
                        encoding="utf-8"
                    ) as file:

                        writer = csv.DictWriter(
                            file,
                            fieldnames=list(row.keys()) + ["error"]
                        )

                        if not file_exists:
                            writer.writeheader()

                        rejected_row = row.copy()
                        rejected_row["error"] = error

                        writer.writerow(rejected_row)

                    logger.warning(
                        f"Rejected record: {error}"
                    )

                    continue

                customer = transform_customer(row)
                valid_batch.append(customer)

            inserted, duplicates = insert_customers_batch(
                valid_batch
            )

            inserted_records += inserted
            duplicate_records += duplicates

        if not schema_checked:
            raise ValueError(
                "Input file contains no records to process."
            )

        accounted_records = (
            inserted_records
            + duplicate_records
            + rejected_records
        )

        if accounted_records != total_records:
            raise RuntimeError(
                "Record reconciliation failed."
            )

        status = "SUCCESS"

    except Exception:

        status = "FAILED"

        logger.exception("Pipeline failed")

        raise

    finally:

        end_time = get_timestamp()

        performance = {
            "execution_time_seconds": 0,
            "peak_memory_mb": 0
        }

        if monitor_start is not None and tracemalloc.is_tracing():
            performance = stop_monitoring(monitor_start)

        if monitor_start is not None:

            run_data = {
                "run_id": run_id,
                "input_file": str(file_path),
                "start_time": start_time,
                "end_time": end_time,
                "total_records": total_records,
                "inserted_records": inserted_records,
                "duplicate_records": duplicate_records,
                "rejected_records": rejected_records,
                "execution_time_seconds": performance[
                    "execution_time_seconds"
                ],
                "peak_memory_mb": performance[
                    "peak_memory_mb"
                ],
                "status": status
            }

            save_pipeline_run(run_data)

    print("\nPIPELINE REPORT")
    print("-----------------------")
    print(f"Run ID: {run_id}")
    print(f"Input file: {file_path}")
    print(f"Total records: {total_records}")
    print(f"New records inserted: {inserted_records}")
    print(f"Duplicate records: {duplicate_records}")
    print(f"Rejected records: {rejected_records}")

    print("\nRECONCILIATION REPORT")
    print("-----------------------")
    print(f"Accounted records: {accounted_records}")
    print(f"Unaccounted records: {total_records - accounted_records}")
    print(f"Reconciliation: {status}")

    print("\nPERFORMANCE REPORT")
    print("-----------------------")
    print(
        f"Execution time: "
        f"{performance['execution_time_seconds']} seconds"
    )
    print(
        f"Peak memory usage: "
        f"{performance['peak_memory_mb']} MB"
    )

    print("\nRUN METRICS")
    print("-----------------------")
    print("Pipeline execution details saved to SQLite database.")
    print(f"Rejected records file: {rejected_file}")


if __name__ == "__main__":
    run_pipeline("data/input/customers.csv")
