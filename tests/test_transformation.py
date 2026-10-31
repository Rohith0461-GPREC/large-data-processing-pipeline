
from src.transformation import transform_customer


def test_transform_customer():

    customer = {
        "customer_id": "101",
        "customer_name": "  rahul reddy ",
        "email": " RAHUL@GMAIL.COM ",
        "age": "25",
        "city": " hyderabad "
    }

    result = transform_customer(customer)

    assert result["customer_id"] == 101
    assert result["customer_name"] == "Rahul Reddy"
    assert result["email"] == "rahul@gmail.com"
    assert result["age"] == 25
    assert result["city"] == "Hyderabad"
