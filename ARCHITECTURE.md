# System Architecture

## 1. Overview

The Large-Scale Data Processing Pipeline processes customer data from CSV and JSON files using chunk-based ingestion.

It validates, transforms, and stores valid records in SQLite while moving invalid records into separate rejected files.

## 2. Architecture Flow

```text
       CSV / JSON Input
              |
              v
      Chunk-Based Ingestion
              |
              v
        Schema Validation
              |
              v
       Record Validation
          /       \
         /         \
      Valid       Invalid
        |            |
        v            v
  Transformation  Rejected
        |          Records
        v
   SQLite Database
        |
        v
  Run Metrics and
   Reconciliation
```

## 3. Main Components

| Component | Responsibility |
|---|---|
| ingestion.py | Reads CSV and JSON files in chunks |
| validation.py | Validates schema and individual records |
| transformation.py | Standardizes customer data |
| database.py | Creates SQLite tables and inserts records |
| monitoring.py | Tracks execution time and memory usage |
| pipeline.py | Coordinates the complete processing workflow |

## 4. Processing Workflow

1. Generate a unique run ID.
2. Identify the input file format.
3. Read records in configurable chunks.
4. Validate the input schema.
5. Validate each customer record.
6. Write invalid records to a rejected-record file.
7. Transform valid records.
8. Insert valid records into SQLite.
9. Detect duplicates using the customer ID primary key.
10. Record execution metrics.
11. Reconcile inserted, duplicate, and rejected records against the total.

## 5. Database Design

The pipeline uses SQLite with two tables:

- **customers:** Stores processed customer records.
- **pipeline_runs:** Stores execution metrics and processing status.

The `customer_id` column is the primary key in the customers table. `INSERT OR IGNORE` prevents duplicate IDs from being inserted again.

## 6. Memory Management

The pipeline processes data in configurable chunks rather than loading the entire input file into memory.

CSV files are read using Python's built-in CSV module. JSON arrays are streamed using the ijson library.

## 7. Error and Reconciliation Handling

Records that fail validation are written to rejected files with their corresponding error messages.

The pipeline checks:

`Total Records = Inserted Records + Duplicate Records + Rejected Records`

A successful reconciliation means all processed records have been accounted for.

## 8. Performance Monitoring

The pipeline records:

- Execution time
- Peak Python-tracked memory usage
- Total records processed
- Inserted records
- Duplicate records
- Rejected records

These metrics help evaluate processing performance across different chunk sizes.
