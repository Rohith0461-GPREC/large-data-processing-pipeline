# Data Dictionary

## Customer Input Dataset

The pipeline accepts customer records in CSV and JSON formats.

| Field | Data Type | Description | Validation |
|---|---|---|---|
| customer_id | Integer | Unique customer identifier | Must contain numeric digits |
| customer_name | String | Full name of the customer | Required, cannot be empty |
| email | String | Customer email address | Must follow a valid email format |
| age | Integer | Customer age | Must be between 18 and 100 |
| city | String | Customer's city | Required, cannot be empty |

## Database Output

The processed customer records are stored in the SQLite `customers` table.

| Column | Data Type | Description |
|---|---|---|
| customer_id | INTEGER | Primary key |
| customer_name | TEXT | Standardized customer name |
| email | TEXT | Lowercase email address |
| age | INTEGER | Validated customer age |
| city | TEXT | Standardized city name |

## Pipeline Run Metrics

The `pipeline_runs` table stores execution information.

| Column | Description |
|---|---|
| run_id | Unique identifier for each pipeline execution |
| input_file | Source file path |
| start_time | Pipeline start timestamp |
| end_time | Pipeline completion timestamp |
| total_records | Total records processed |
| inserted_records | New records inserted |
| duplicate_records | Records skipped because their IDs already exist |
| rejected_records | Records that failed validation |
| execution_time_seconds | Pipeline execution duration |
| peak_memory_mb | Peak Python-tracked memory |
| status | SUCCESS or FAILED |

## Data Processing Rules

- Required fields must be present.
- Customer IDs must be numeric.
- Email addresses must follow the configured validation pattern.
- Customer age must be between 18 and 100.
- Customer names and cities are standardized using title case.
- Emails are converted to lowercase.
- Duplicate customer IDs are ignored by the database.
