import random
import string
from datetime import datetime, date
import psycopg2  # Import the psycopg2 library

# Database connection parameters
db_params = {
		"dbname":   "dealer",
		"user":     "postgres",
		"password": "mypgdbpass",
		"host":     "96.73.17.121",
		"port":     "5432"
}


# Function to execute SQL queries
def execute_query(query):
	connection = psycopg2.connect(**db_params)
	cursor = connection.cursor()
	cursor.execute(query)
	connection.commit()
	cursor.close()
	connection.close()


def generate_random_name():
	first_names = ["John", "Jane", "Michael", "Emily", "William", "Olivia", "James", "Sophia", "Daniel", "Ava"]
	last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
	return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_random_email():
	domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]
	name = generate_random_name().replace(" ", "").lower()
	domain = random.choice(domains)
	return f"{name}@{domain}"


def generate_random_phone_number():
	area_code = ''.join(random.choices(string.digits, k=3))
	middle_digits = ''.join(random.choices(string.digits, k=3))
	last_digits = ''.join(random.choices(string.digits, k=4))
	return f"({area_code}) {middle_digits}-{last_digits}"


def generate_random_location():
	cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "Seattle", "Boston", "Atlanta", "Denver",
			  "Dallas"]
	return f"{random.choice(cities)}, {random.choice(['CA', 'NY', 'IL', 'TX', 'FL', 'WA', 'MA', 'GA', 'CO', 'TX'])}"


def generate_random_vin():
	letters = string.ascii_uppercase
	digits = string.digits
	vin = ''.join(random.choice(letters + digits) for _ in range(17))
	return vin


# Generate INSERT statements for dealerships
num_dealerships = 5
num_salespersons = 10
num_customers = 15
num_cars = 20
num_sales = 50

generated_emails = set()
generated_phone_numbers = set()

try:
	for _ in range(num_dealerships):
		name = f"Dealer {random.randint(100, 999)}"
		location = generate_random_location()

		insert_dealership = (f"INSERT INTO dealer.public.dealership "
							 f"(name, location) "
							 f"VALUES('{name}', '{location}')")
		execute_query(insert_dealership)
		print("Inserted dealership:", insert_dealership)

	for _ in range(num_salespersons):
		name = generate_random_name()
		email = generate_random_email()

		# Ensure unique email address
		while email in generated_emails:
			email = generate_random_email()

		generated_emails.add(email)  # Add the email to the set

		phone = generate_random_phone_number()

		insert_salesperson = (
				f"INSERT INTO dealer.public.salesperson "
				f"(salesperson_name, salesperson_email, salesperson_phone_number, created_at) "
				f"VALUES('{name}', '{email}', '{phone}', '{datetime.now()}')"
		)
		execute_query(insert_salesperson)
		print(insert_salesperson)

	for _ in range(num_customers):
		first_name = generate_random_name().split()[0]
		last_name = generate_random_name().split()[1]
		email = generate_random_email()

		# Ensure unique email address
		while email in generated_emails:
			email = generate_random_email()

		generated_emails.add(email)

		phone_number = generate_random_phone_number()

		# Ensure unique phone number
		while phone_number in generated_phone_numbers:
			phone_number = generate_random_phone_number()

		generated_phone_numbers.add(phone_number)

		date_of_birth = date(random.randint(1950, 2005), random.randint(1, 12), random.randint(1, 28))

		insert_customer = (
				f"INSERT INTO dealer.public.customer "
				f"(first_name, last_name, email, phone_number, date_of_birth, created_at) "
				f"VALUES('{first_name}', '{last_name}', '{email}', '{phone_number}', '{date_of_birth}', '{datetime.now()}')"
		)

		execute_query(insert_customer)  # Use the retry function
		print(insert_customer)

	for _ in range(num_cars):
		make = random.choice(
			["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", "Audi", "Subaru"])
		model = f"{random.randint(1, 9)} Series"
		year = random.randint(2000, 2023)
		customer_id = random.randint(1, num_customers)  # Corrected customer ID range
		price = round(random.uniform(10000, 50000), 2)
		condition = random.choice(["New", "Used"])
		dealership_id = random.randint(1, num_dealerships)  # Assuming dealership IDs are within this range
		vin = generate_random_vin()

		insert_car = (
				f"INSERT INTO dealer.public.car "
				f"(make, model, year, customer_id, price, condition, dealership_id, vin) "
				f"VALUES('{make}', '{model}', {year}, {customer_id}, {price}, '{condition}', {dealership_id}, '{vin}')"
		)
		execute_query(insert_car)
		print(insert_car)

	print("Finished inserting data.")
except Exception as e:
	print(f"An error occurred while inserting data: {str(e)}")