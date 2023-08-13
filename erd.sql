CREATE TABLE if not exists salesperson
(
    salesperson_id SERIAL PRIMARY KEY,
    salesperson_name VARCHAR(100) NOT NULL,
    salesperson_email VARCHAR(100) UNIQUE NOT NULL,
    salesperson_phone_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists dealership
(
    dealership_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    location VARCHAR(100)
);

CREATE TABLE if not exists Car
(
    car_id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    customer_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    condition VARCHAR(255) NOT NULL,
    dealership_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vin VARCHAR(17) UNIQUE NOT NULL,
    FOREIGN KEY (dealership_id) REFERENCES dealership (dealership_id)
);



CREATE TABLE if not exists customer
(
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists sales
(
    sales_id SERIAL PRIMARY KEY,
    salesperson_id INT NOT NULL,
    car_id INT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (salesperson_id) REFERENCES salesperson (salesperson_id),
    FOREIGN KEY (car_id) REFERENCES car (car_id)
);

CREATE TABLE if not exists Service
(
    service_id SERIAL PRIMARY KEY,
    car_id INTEGER REFERENCES Car (car_id),
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    customer_id INTEGER REFERENCES Customer (customer_id),
    service_date DATE NOT NULL,
    service_description TEXT NOT NULL,
    service_cost DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists purchase
(
    purchase_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    car_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (car_id) REFERENCES car (car_id)
);

CREATE TABLE if not exists invoice
(
    invoice_id SERIAL PRIMARY KEY,
    salesperson_id INT NOT NULL,
    car_id INT NOT NULL,
    sale_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (salesperson_id) REFERENCES salesperson (salesperson_id),
    FOREIGN KEY (car_id) REFERENCES car (car_id)
);

CREATE TABLE if not exists customer_car
(
    customer_car_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    car_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (car_id) REFERENCES car (car_id)
);

CREATE TABLE if not exists customer_service
(
    customer_service_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    service_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (service_id) REFERENCES service (service_id)
);

CREATE TABLE if not exists service_ticket
(
    ticket_id SERIAL PRIMARY KEY,
    car_id INT NOT NULL,
    service_date DATE NOT NULL,
    service_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES car (car_id)
);

CREATE TABLE if not exists mechanic
(
    mechanic_id SERIAL PRIMARY KEY,
    mechanic_name VARCHAR(100) NOT NULL,
    mechanic_email VARCHAR(100) UNIQUE NOT NULL,
    mechanic_phone_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists car_mechanic
(
    car_mechanic_id SERIAL PRIMARY KEY,
    car_id INT NOT NULL,
    mechanic_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES Car (car_id),
    FOREIGN KEY (mechanic_id) REFERENCES mechanic (mechanic_id)
);

CREATE TABLE if not exists br_invoice
(
    br_invoice_id SERIAL PRIMARY KEY,
    invoice_id INT NOT NULL,
    customer_id INT NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoice (invoice_id),
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);


ALTER TABLE Service
    ADD COLUMN mechanic_id INT NOT NULL,
    ADD FOREIGN KEY (mechanic_id) REFERENCES mechanic (mechanic_id);

ALTER TABLE purchase
    ADD COLUMN purchase_price DECIMAL(10, 2) NOT NULL;

ALTER TABLE invoice
    ADD COLUMN payment_status VARCHAR(20) NOT NULL;

ALTER TABLE customer_car
    ADD COLUMN purchase_date DATE NOT NULL;

ALTER TABLE customer_service
    ADD COLUMN service_cost DECIMAL(10, 2) NOT NULL;

ALTER TABLE service_ticket
    ADD COLUMN ticket_status VARCHAR(20) NOT NULL;

ALTER TABLE mechanic
    ADD COLUMN mechanic_specialty VARCHAR(100) NOT NULL;

ALTER TABLE br_invoice
    ADD COLUMN br_invoice_date DATE NOT NULL;