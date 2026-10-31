# Large-Scale Data Processing Pipeline

## Project Overview

A Python-based data processing pipeline designed to efficiently process large CSV and JSON files using memory-efficient chunk-based ingestion and streaming techniques.

The pipeline validates input schemas and individual records, transforms valid customer data, stores processed records in an SQLite database, and quarantines invalid records for further inspection.

## Key Features

- Chunk-based CSV ingestion
- Streaming JSON ingestion using `ijson`
- Input schema validation
- Record-level data validation
- Data transformation and standardization
- SQLite database integration
- Duplicate detection and idempotent processing
- Rejected record handling with error reasons
- Execution time and memory monitoring
- Record reconciliation and processing metrics
- Pipeline execution logging
- Automated unit and integration tests
- Synthetic data generation for 100,000+ records
- Chunk-size performance benchmarking
- Failed pipeline execution tracking

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| SQLite | Data storage |
| CSV | Structured input processing |
| ijson | Streaming JSON ingestion |
| pytest | Automated testing |
| tracemalloc | Python memory monitoring |

## Project Structure

```text
large-data-processing-pipeline/
├── data/
│   ├── input/
│   ├── output/
│   └── rejected/
├── src/
│   ├── ingestion.py
│   ├── validation.py
│   ├── transformation.py
│   ├── database.py
│   ├── monitoring.py
│   └── pipeline.py
├── tests/
├── scripts/
│   ├── generate_data.py
│   └── benchmark.py
├── reports/
│   └── benchmark_results.md
├── requirements.txt
├── pytest.ini
├── ARCHITECTURE.md
├── DATA_DICTIONARY.md
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Rohith0461-GPREC/large-data-processing-pipeline.git
cd large-data-processing-pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Generate Test Data

```bash
python scripts/generate_data.py
```

This generates 100,000 synthetic customer records in `data/input/large_customers.csv`.

## Run the Pipeline

```bash
python -m src.pipeline
```

The default input file is `data/input/customers.csv`.

The pipeline also supports custom input paths and chunk sizes through the `run_pipeline()` function.

## Run Automated Tests

```bash
pytest -v
```

**Latest test result: 19 tests passed.**

The test suite covers validation, transformation, CSV and JSON ingestion, database operations, and pipeline execution.

## Performance Benchmarking

```bash
python scripts/benchmark.py
```

The benchmark evaluates different chunk sizes using execution time and Python memory measurements.

### Benchmark Results

Tested with 100,000 synthetic customer records.

| Chunk Size | Execution Time | Peak Memory |
|---:|---:|---:|
| 500 | 3.9651 sec | 0.71 MB |
| 1,000 | 2.9204 sec | 1.37 MB |
| 5,000 | 2.3888 sec | 6.67 MB |
| 10,000 | 2.3908 sec | 13.31 MB |

In this benchmark run, a chunk size of 5,000 provided the best observed execution time.

Results may vary depending on hardware and system conditions. These measurements are from a single benchmark run.

See `reports/benchmark_results.md` for the detailed results.

## Database Design

The pipeline uses SQLite with two main tables:

- **customers:** Stores validated and transformed customer records.
- **pipeline_runs:** Stores execution metrics, record counts, timestamps, and pipeline status.

## Error Handling and Reconciliation

- Invalid records are written to separate rejected-record files.
- Duplicate customer IDs are ignored during database insertion.
- Pipeline failures are logged.
- Processing counts are reconciled to identify unaccounted records.
- Execution metrics are stored for monitored pipeline runs.

## Documentation

Additional project documentation:

- `ARCHITECTURE.md` – Pipeline architecture and processing flow.
- `DATA_DICTIONARY.md` – Input fields and database metrics.

## Performance Notes

The pipeline was tested using 100,000 synthetic customer records.

CSV processing uses chunk-based ingestion, while JSON processing uses streaming with `ijson`.

Memory measurements using `tracemalloc` represent Python-tracked memory and not total system RAM.

## Future Improvements

- Process-level RAM monitoring
- Stronger error recovery and retry mechanisms
- More extensive malformed-input and edge-case testing
- Additional input formats
- Improved database transaction management
- Larger-scale performance testing