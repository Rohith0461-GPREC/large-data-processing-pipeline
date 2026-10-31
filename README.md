# Large-Scale Data Processing Pipeline

## Project Overview

A Python-based data processing pipeline designed to process large CSV and JSON files efficiently using chunk-based ingestion.

The pipeline validates records, transforms valid data, stores customers in an SQLite database, and quarantines invalid records.

## Key Features

- Chunk-based CSV ingestion
- Streaming JSON ingestion using ijson
- Schema and record-level validation
- Data transformation and standardization
- SQLite database integration
- Duplicate detection and idempotent processing
- Rejected record handling
- Execution time and memory monitoring
- Record reconciliation
- Automated unit and integration tests
- Synthetic data generation for 100,000+ records
- Chunk-size benchmarking

## Technology Stack

- Python 3.11
- SQLite
- CSV
- ijson
- pytest
- tracemalloc

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
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
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

This generates 100,000 synthetic customer records.

## Run the Pipeline

```bash
python -m src.pipeline
```

To process a different input file, call `run_pipeline()` with its path and desired chunk size.

## Run Tests

```bash
pytest -v
```

## Benchmark

```bash
python scripts/benchmark.py
```

The benchmark compares different chunk sizes using execution time and memory measurements.

## Database

The pipeline stores customer records and execution metrics in SQLite:

- `customers`: processed customer records
- `pipeline_runs`: execution metrics and reconciliation status

## Current Test Results

11 automated tests passed during the latest test run.

## Performance Notes

The pipeline was tested with 100,000 synthetic customer records. The observed performance depends on the machine, database state, and chunk size.

Memory measurements using `tracemalloc` represent Python-tracked memory, not total system RAM.

## Future Improvements

- Stronger error handling and failed-run tracking
- More comprehensive performance benchmarking with fresh databases
- Additional schema and malformed-input tests
- Architecture and data dictionary documentation
