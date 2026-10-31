
import re


REQUIRED_FIELDS = [
    "customer_id",
    "customer_name",
    "email",
    "age",
    "city"
]


def validate_schema(field_names):
    """
    Check whether all required customer fields exist.
    """

    if not field_names:
        return False, "Input file has no header or schema."

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in field_names
    ]

    if missing_fields:
        return False, f"Missing required columns: {', '.join(missing_fields)}"

    return True, None


def validate_customer(row):
    """
    Validate a single customer record.
    Returns (is_valid, error_message).
    """

    for field in REQUIRED_FIELDS:
        if not row.get(field) or not str(row[field]).strip():
            return False, f"Missing required field: {field}"

    if not str(row["customer_id"]).isdigit():
        return False, "Invalid customer ID"

    if not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        str(row["email"])
    ):
        return False, "Invalid email address"

    try:
        age = int(row["age"])
    except (ValueError, TypeError):
        return False, "Age must be a number"

    if age < 18 or age > 100:
        return False, "Age must be between 18 and 100"

    return True, None
