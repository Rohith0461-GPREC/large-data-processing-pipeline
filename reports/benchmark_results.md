# Benchmark Results

## 1. Overview

The data processing pipeline was benchmarked using 100,000 synthetic customer records.

Four different chunk sizes were tested to compare execution time and memory usage.

Each benchmark run used a separate, fresh SQLite database to ensure that records were newly inserted rather than counted as duplicates.

## 2. Benchmark Environment

- Language: Python 3.11
- Database: SQLite
- Input format: CSV
- Input records: 100,000
- Chunk sizes: 500, 1,000, 5,000, 10,000

## 3. Benchmark Results

| Chunk Size | Execution Time (seconds) | Peak Memory (MB) |
|---:|---:|---: