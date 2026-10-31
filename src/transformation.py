
def transform_customer(row):
    """
    Convert validated customer data into
    standardized database-ready format.
    """

    return {
        "customer_id": int(row["customer_id"]),
        "customer_name": row["customer_name"].strip().title(),
        "email": row["email"].strip().lower(),
        "age": int(row["age"]),
        "city": row["city"].strip().title()
    }
