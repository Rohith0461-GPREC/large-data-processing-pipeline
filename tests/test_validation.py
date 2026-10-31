
from src.validation import validate_customer


def test_valid_customer():
    customer = {
        "customer_id": "101",
        "customer_name": "Rahul",
        "email": "rahul@gmail.com",
        "age": "25",
        "city": "Hyderabad"
    }

    is_valid, error = validate_customer(customer)

    assert is_valid is True
    assert error is None


def test_invalid_email():
    customer = {
        "customer_id": "102",
        "customer_name": "Anjali",
        "email": "invalid-email",
        "age": "28",
        "city": "Bangalore"
    }

    is_valid, error = validate_customer(customer)

    assert is_valid is False
    assert error == "Invalid email address"


def test_invalid_age():
    customer = {
        "customer_id": "103",
        "customer_name": "Kiran",
        "email": "kiran@gmail.com",
        "age": "15",
        "city": "Chennai"
    }

    is_valid, error = validate_customer(customer)

    assert is_valid is False
    assert error == "Age must be between 18 and 100"



def test_valid_schema():
    from src.validation import validate_schema, REQUIRED_FIELDS

    is_valid, error = validate_schema(REQUIRED_FIELDS)

    assert is_valid is True
    assert error is None


def test_missing_schema_column():
    from src.validation import validate_schema

    fields = ["customer_id", "customer_name", "age", "city"]

    is_valid, error = validate_schema(fields)

    assert is_valid is False
    assert "email" in error


def test_empty_schema():
    from src.validation import validate_schema

    is_valid, error = validate_schema([])

    assert is_valid is False
    assert error == "Input file has no header or schema."

