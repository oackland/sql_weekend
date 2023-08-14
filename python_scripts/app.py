import csv
import os
import random

import psycopg2
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

db_database = os.getenv("DB_DATABASE")
db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_port = os.getenv("DB_PORT")

conn = psycopg2.connect(
    database=db_database, user=db_user, password=db_password, host=db_host, port=db_port
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a Faker instance
fake = Faker()

# Define the table schema
table_schema = """
-- #done
CREATE TABLE "salesperson"
(
    "salesperson_id" SERIAL PRIMARY KEY,
    "salesperson_name" VARCHAR(100) NOT NULL,
    "salesperson_email" VARCHAR(100) UNIQUE NOT NULL,
    "salesperson_phone_number" VARCHAR(20) NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);
-- # done
CREATE TABLE "dealership"
(
    "dealership_id" SERIAL PRIMARY KEY,
    "name" VARCHAR(30),
    "location" VARCHAR(100)
);
-- # done
CREATE TABLE "car"
(
    "car_id" SERIAL PRIMARY KEY,
    "make" VARCHAR(50) NOT NULL,
    "model" VARCHAR(50) NOT NULL,
    "year" INTEGER NOT NULL,
    "customer_id" INT NOT NULL,
    "price" DECIMAL(10, 2) NOT NULL,
    "condition" VARCHAR(255) NOT NULL,
    "dealership_id" INT,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
    "vin" VARCHAR(17) UNIQUE NOT NULL
);

CREATE TABLE "customer"
(
    "customer_id" SERIAL PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(100) UNIQUE NOT NULL,
    "phone_number" VARCHAR(20) NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "sales"
(
    "sales_id" SERIAL PRIMARY KEY,
    "salesperson_id" INT NOT NULL,
    "car_id" INT NOT NULL,
    "sale_date" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "service"
(
    "service_id" SERIAL PRIMARY KEY,
    "car_id" INTEGER,
    "service_name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "customer_id" INTEGER,
    "service_date" DATE NOT NULL,
    "service_description" TEXT NOT NULL,
    "service_cost" DECIMAL(10, 2) NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "purchase"
(
    "purchase_id" SERIAL PRIMARY KEY,
    "customer_id" INT NOT NULL,
    "car_id" INT NOT NULL,
    "purchase_date" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "invoice"
(
    "invoice_id" SERIAL PRIMARY KEY,
    "salesperson_id" INT NOT NULL,
    "car_id" INT NOT NULL,
    "sale_date" DATE NOT NULL,
    "total_price" DECIMAL(10, 2) NOT NULL,
    "invoice_date" timestamp DEFAULT (CURRENT_TIMESTAMP),
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "customer_car"
(
    "customer_car_id" SERIAL PRIMARY KEY,
    "customer_id" INT NOT NULL,
    "car_id" INT NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "customer_service"
(
    "customer_service_id" SERIAL PRIMARY KEY,
    "customer_id" INT NOT NULL,
    "service_id" INT NOT NULL,
    "service_date" DATE NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "service_ticket"
(
    "ticket_id" SERIAL PRIMARY KEY,
    "car_id" INT NOT NULL,
    "service_date" DATE NOT NULL,
    "service_description" TEXT,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "mechanic"
(
    "mechanic_id" SERIAL PRIMARY KEY,
    "mechanic_name" VARCHAR(100) NOT NULL,
    "mechanic_email" VARCHAR(100) UNIQUE NOT NULL,
    "mechanic_phone_number" VARCHAR(20) NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "car_mechanic"
(
    "car_mechanic_id" SERIAL PRIMARY KEY,
    "car_id" INT NOT NULL,
    "mechanic_id" INT NOT NULL,
    "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "br_invoice"
(
    "br_invoice_id" SERIAL PRIMARY KEY,
    "invoice_id" INT NOT NULL,
    "customer_id" INT NOT NULL
);

ALTER TABLE "car"
    ADD FOREIGN KEY ("dealership_id") REFERENCES "dealership" ("dealership_id");

ALTER TABLE "sales"
    ADD FOREIGN KEY ("salesperson_id") REFERENCES "salesperson" ("salesperson_id");

ALTER TABLE "sales"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "service"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "service"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "purchase"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "purchase"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "invoice"
    ADD FOREIGN KEY ("salesperson_id") REFERENCES "salesperson" ("salesperson_id");

ALTER TABLE "invoice"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "customer_car"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "customer_car"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "customer_service"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "customer_service"
    ADD FOREIGN KEY ("service_id") REFERENCES "service" ("service_id");

ALTER TABLE "service_ticket"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "car_mechanic"
    ADD FOREIGN KEY ("car_id") REFERENCES "car" ("car_id");

ALTER TABLE "car_mechanic"
    ADD FOREIGN KEY ("mechanic_id") REFERENCES "mechanic" ("mechanic_id");

ALTER TABLE "br_invoice"
    ADD FOREIGN KEY ("invoice_id") REFERENCES "invoice" ("invoice_id");

ALTER TABLE "br_invoice"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");
"""

# List of tables to generate data for
tables = [
    "salesperson",
    "dealership",
    "car",
    "customer",
    "sales",
    "service",
    "purchase",
    "invoice",
    "customer_car",
    "customer_service",
    "service_ticket",
    "mechanic",
    "car_mechanic",
    "br_invoice",
]

# Generate and insert data into each table
for table in tables:
    if table == "salesperson":
        num_rows = 50
        for _ in range(num_rows):
            salesperson_name = fake.name()
            salesperson_email = fake.email()
            salesperson_phone_number = fake.phone_number()
            insert_query = """
            INSERT INTO public.salesperson ("salesperson_name", "salesperson_email", "salesperson_phone_number")
            VALUES (%s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (salesperson_name, salesperson_email, salesperson_phone_number),
            )

    elif table == "dealership":
        num_rows = 20
        for _ in range(num_rows):
            name = fake.company()
            location = fake.city()
            insert_query = """
            INSERT INTO public.dealership ("name", "location")
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (name, location))

    elif table == "customer":
        num_rows = 300
        for _ in range(num_rows):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone_number = fake.phone_number()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
                INSERT INTO public.customer ("first_name", "last_name", "email", "phone_number", "date_of_birth", "created_at")
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (first_name, last_name, email, phone_number, date_of_birth, created_at),
            )

    elif table == "service":
        num_rows = 100
        for _ in range(num_rows):
            car_id = random.randint(1, 100)
            service_name = fake.word()
            description = fake.paragraph()
            customer_id = random.randint(1, 100)
            service_date = fake.date_between(start_date="-3y", end_date="today")
            service_description = fake.paragraph()
            service_cost = round(random.uniform(10, 500), 2)

            insert_query = """
                INSERT INTO public.service ("car_id", "service_name", "description", "customer_id", "service_date", "service_description", "service_cost")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (
                    car_id,
                    service_name,
                    description,
                    customer_id,
                    service_date,
                    service_description,
                    service_cost,
                ),
            )

    elif table == "sales":
        num_rows = 500
        for _ in range(num_rows):
            salesperson_id = random.randint(1, 10)
            car_id = random.randint(1, 100)
            sale_date = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
            INSERT INTO public.sales ("salesperson_id", "car_id", "sale_date")
            VALUES (%s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (salesperson_id, car_id, sale_date),
            )

    elif table == "car":
        num_rows = 1000
        car_makes_models = []
        with open("car_makes_models.csv", "r") as file:
            csv_data = csv.DictReader(file)
            for row in csv_data:
                make = row["make"]
                model = row["model"]
                car_makes_models.append((make, model))

        for _ in range(num_rows):
            make, model = random.choice(car_makes_models)
            year = random.randint(1990, 2022)
            customer_id = random.randint(1, 100)
            price = round(random.uniform(5000, 50000), 2)
            car_condition = random.choice(["new", "used"])
            dealership_id = random.randint(1, 5)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")
            vin = fake.unique.random_number(digits=17)

            insert_query = """
            INSERT INTO public.car ("make", "model", "year", "customer_id",
                "price", "condition", "dealership_id", "created_at", "vin")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                insert_query,
                (
                    make,
                    model,
                    year,
                    customer_id,
                    price,
                    car_condition,
                    dealership_id,
                    created_at,
                    vin,
                ),
            )

    elif table == "service_ticket":
        num_rows = 300
        for _ in range(num_rows):
            car_id = random.randint(1, 100)
            service_date = fake.date_between(start_date="-5y", end_date="now")
            service_description = fake.sentence(nb_words=6, variable_nb_words=True)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
            INSERT INTO public.service_ticket ("car_id", "service_date", "service_description", "created_at")
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (car_id, service_date, service_description, created_at),
            )

    elif table == "mechanic":
        num_rows = 50
        for _ in range(num_rows):
            mechanic_name = fake.name()
            mechanic_email = fake.email()
            mechanic_phone_number = fake.phone_number()

            insert_query = """
            INSERT INTO public.mechanic ("mechanic_name", "mechanic_email", "mechanic_phone_number")
            VALUES (%s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (mechanic_name, mechanic_email, mechanic_phone_number),
            )

    elif table == "invoice":
        num_rows = 100
        for _ in range(num_rows):
            salesperson_id = random.randint(1, 10)
            car_id = random.randint(1, 100)
            sale_date = fake.date_time_between(start_date="-5y", end_date="now").date()
            total_price = round(random.uniform(5000, 50000), 2)
            invoice_date = fake.date_time_between(start_date="-5y", end_date="now")
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
            INSERT INTO public.invoice ("salesperson_id", "car_id", "sale_date", "total_price", "invoice_date", "created_at")
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    salesperson_id,
                    car_id,
                    sale_date,
                    total_price,
                    invoice_date,
                    created_at,
                ),
            )

    elif table == "customer_car":
        num_rows = 100
        for _ in range(num_rows):
            customer_id = random.randint(1, 100)
            car_id = random.randint(1, 100)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
            INSERT INTO public.customer_car ("customer_id", "car_id", "created_at")
            VALUES (%s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (customer_id, car_id, created_at),
            )

    elif table == "customer_service":
        num_rows = 100
        for _ in range(num_rows):
            customer_id = random.randint(1, 100)
            service_id = random.randint(1, 100)
            service_date = fake.date_between(start_date="-5y", end_date="now")
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
                INSERT INTO public.customer_service ("customer_id", "service_id", "service_date", "created_at")
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (customer_id, service_id, service_date, created_at),
            )

    elif table == "service_ticket":
        num_rows = 100
        for _ in range(num_rows):
            car_id = random.randint(1, 100)
            service_date = fake.date_between(start_date="-5y", end_date="now")
            service_description = fake.sentence(nb_words=6, variable_nb_words=True)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
                INSERT INTO public.service_ticket ("car_id", "service_date", "service_description", "created_at")
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (car_id, service_date, service_description, created_at),
            )

    elif table == "mechanic":
        num_rows = 10
        for _ in range(num_rows):
            mechanic_name = fake.name()
            mechanic_email = fake.email()
            mechanic_phone_number = fake.phone_number()

            insert_query = """
                INSERT INTO public.mechanic ("mechanic_name", "mechanic_email", "mechanic_phone_number")
                VALUES (%s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (mechanic_name, mechanic_email, mechanic_phone_number),
            )

    elif table == "car_mechanic":
        num_rows = 100
        for _ in range(num_rows):
            car_id = random.randint(1, 100)
            mechanic_id = random.randint(1, 10)
            created_at = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
                INSERT INTO public.car_mechanic ("car_id", "mechanic_id", "created_at")
                VALUES (%s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (car_id, mechanic_id, created_at),
            )

    elif table == "br_invoice":
        num_rows = 50
        for _ in range(num_rows):
            invoice_id = random.randint(1, 50)
            customer_id = random.randint(1, 100)

            insert_query = """
                INSERT INTO public.br_invoice ("invoice_id", "customer_id")
                VALUES (%s, %s)
                """
            cursor.execute(
                insert_query,
                (invoice_id, customer_id),
            )

    elif table == "purchase":
        num_rows = 100
        for _ in range(num_rows):
            customer_id = random.randint(1, 100)
            car_id = random.randint(1, 100)
            purchase_date = fake.date_time_between(start_date="-5y", end_date="now")

            insert_query = """
                INSERT INTO public.purchase ("customer_id", "car_id", "purchase_date")
                VALUES (%s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (customer_id, car_id, purchase_date),
            )


# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data generation complete.")
