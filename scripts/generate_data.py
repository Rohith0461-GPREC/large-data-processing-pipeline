
import csv
import random
from pathlib import Path


def generate_customers(total_records=100000):

    output_file = Path("data/input/large_customers.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    cities = ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Pune"]

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "customer_id",
            "customer_name",
            "email",
            "age",
            "city"
        ])

        for customer_id in range(1001, 1001 + total_records):

            name = f"Customer{customer_id}"
            email = f"customer{customer_id}@example.com"
            age = random.randint(18, 100)
            city = random.choice(cities)

            writer.writerow([
                customer_id,
                name,
                email,
                age,
                city
            ])

    print(f"Successfully generated {total_records} records.")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    generate_customers(100000)
