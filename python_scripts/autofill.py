import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db_database = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')
db_port = os.getenv('DB_PORT')
try:
	conn = psycopg2.connect(
		database=db_database,
		user=db_user,
		password=db_password,
		host=db_host,
		port=db_port
	)
	cur = conn.cursor()

	create_table_salesperson = '''
    CREATE TABLE IF NOT EXISTS public.salesperson(
        "salesperson_id" SERIAL PRIMARY KEY,
        "salesperson_name" VARCHAR(100) NOT NULL,
        "salesperson_email" VARCHAR(100) UNIQUE NOT NULL,
        "salesperson_phone_number" VARCHAR(20) NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_salesperson)

	create_table_dealership = '''
    CREATE TABLE IF NOT EXISTS public.dealership(
        "dealership_id" SERIAL PRIMARY KEY,
        "name" VARCHAR(30),
        "location" VARCHAR(100)
    );
    '''
	cur.execute(create_table_dealership)

	create_table_car = '''
    CREATE TABLE IF NOT EXISTS public.car(
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
    '''
	cur.execute(create_table_car)

	create_table_customer = '''
    CREATE TABLE IF NOT EXISTS public.customer(
        "customer_id" SERIAL PRIMARY KEY,
        "first_name" VARCHAR(50) NOT NULL,
        "last_name" VARCHAR(50) NOT NULL,
        "email" VARCHAR(100) UNIQUE NOT NULL,
        "phone_number" VARCHAR(20) NOT NULL,
        "date_of_birth" DATE NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_customer)

	create_table_sales = '''
    CREATE TABLE IF NOT EXISTS public.sales(
        "sales_id" SERIAL PRIMARY KEY,
        "salesperson_id" INT NOT NULL,
        "car_id" INT NOT NULL,
        "sale_date" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_sales)

	create_table_service = '''
    CREATE TABLE IF NOT EXISTS public.service(
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
    '''
	cur.execute(create_table_service)

	create_table_purchase = '''
    CREATE TABLE IF NOT EXISTS public.purchase(
        "purchase_id" SERIAL PRIMARY KEY,
        "customer_id" INT NOT NULL,
        "car_id" INT NOT NULL,
        "purchase_date" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_purchase)

	create_table_invoice = '''
    CREATE TABLE IF NOT EXISTS public.invoice(
        "invoice_id" SERIAL PRIMARY KEY,
        "salesperson_id" INT NOT NULL,
        "car_id" INT NOT NULL,
        "sale_date" DATE NOT NULL,
        "total_price" DECIMAL(10, 2) NOT NULL,
        "invoice_date" timestamp DEFAULT (CURRENT_TIMESTAMP),
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_invoice)

	create_table_customer_car = '''
    CREATE TABLE IF NOT EXISTS public.customer_car(
        "customer_car_id" SERIAL PRIMARY KEY,
        "customer_id" INT NOT NULL,
        "car_id" INT NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_customer_car)

	create_table_customer_service = '''
    CREATE TABLE IF NOT EXISTS public.customer_service(
        "customer_service_id" SERIAL PRIMARY KEY,
        "customer_id" INT NOT NULL,
        "service_id" INT NOT NULL,
        "service_date" DATE NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_customer_service)

	create_table_service_ticket = '''
    CREATE TABLE IF NOT EXISTS public.service_ticket(
        "ticket_id" SERIAL PRIMARY KEY,
        "car_id" INT NOT NULL,
        "service_date" DATE NOT NULL,
        "service_description" TEXT,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_service_ticket)

	create_table_mechanic = '''
    CREATE TABLE IF NOT EXISTS public.mechanic(
        "mechanic_id" SERIAL PRIMARY KEY,
        "mechanic_name" VARCHAR(100) NOT NULL,
        "mechanic_email" VARCHAR(100) UNIQUE NOT NULL,
        "mechanic_phone_number" VARCHAR(20) NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_mechanic)

	create_table_car_mechanic = '''
    CREATE TABLE IF NOT EXISTS public.car_mechanic(
        "car_mechanic_id" SERIAL PRIMARY KEY,
        "car_id" INT NOT NULL,
        "mechanic_id" INT NOT NULL,
        "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
    );
    '''
	cur.execute(create_table_car_mechanic)

	create_table_br_invoice = '''
    CREATE TABLE IF NOT EXISTS public.br_invoice(
        "br_invoice_id" SERIAL PRIMARY KEY,
        "invoice_id" INT NOT NULL,
        "customer_id" INT NOT NULL
    );
    '''
	cur.execute(create_table_br_invoice)

	conn.commit()
	conn.close()
	print("Finished script.")
except psycopg2.Error as e:
	print("Error connecting to the database:", e)
