# Dealer SQL Project

> ### Read me!
> If you head over pdf folder you will see the ERD Diagram for this project.
>
> Open Python Script, you will see two python file.
>  - If you open the autofill will create all the database in a single run.
> - `app.py`will insert over 3,000 piece of data in a single run. might take a couple seconds to complete the upload.
> - Right now the database is still running on my end, if you want to play around and see how it was made you are.

Feel free to fork this and play around.

First, we will brainstorm some ideas.\
We have the following specifications so far...


>    <li><code>Use PDF with an ERD</code></li>
>    <li><code>The ERD in PDF</code></li>
>    <li><code>SQL code that would be used to create the new database (DDL, DML).</code></li>
>    <li><code>Also, once the database and the tables are created, each person should have AT LEAST 2 pieces
records of data inside the tables. (You can add more if you want)</code></li>

So far we know we need three files: `ERD`, `DDL`, and `DML`.

## Week 4 - ERD Assignment

USE ERD to Create SQL Database

Instructions:
Create an ERD for a car dealership. The dealership sells both new and used cars,
and it operates a service facility.
Base your design on the following business rules:

By the previous approach im thinking in a single table for `<car table>` since in one column you can filter from new to
old.
having two table here for each condition of new vs old is useless because you would extend the piece of code to join
this tables
<blockquote>

### Let's think about this very quick

> In the world of data and SQL, bytes are like speed enhancers. When creating tables, we're like puzzle solvers,
> fitting data into compact capsules (1 to 4 bytes). Our goal? Super efficiency!
>
> Think big – even though we're handling a hundred lines now, reality involves millions or billions of data pieces
> daily. Writing massive code? It's like slowing down a Ferrari from 1ms to 2s.
>
> So, we're the data tailors, crafting sleek bytes for lightning-fast operations. Efficiency is our game, whether it's a
> hundred lines or a million pieces. 🚀🔍

So far I can see three department

> Sales
> staff
> customer

```mermaid
flowchart TD

subgraph Schema: dealer.public
    salesperson[Salesperson]
    dealership[Dealership]
    car[Car]
    customer[Customer]
    sales[Sales]
    service[Service]
    purchase[Purchase]
    invoice[Invoice]
    customer_car[Customer Car]
    customer_service[Customer Service]
    service_ticket[Service Ticket]
    mechanic[Mechanic]
    car_mechanic[Car Mechanic]
    br_invoice[BR Invoice]

    salesperson --> sales
    car --> sales
    sales --> customer
    car --> service
    service --> customer
    car --> purchase
    purchase --> customer
    car --> invoice
    salesperson --> invoice
    invoice --> customer
    customer --> customer_car
    car --> customer_car
    customer --> customer_service
    service --> customer_service
    car --> service_ticket
    service_ticket --> car
    mechanic --> service
    car --> car_mechanic
    mechanic --> car_mechanic
    invoice --> br_invoice
    customer --> br_invoice
end

salesperson --> dealership
car --> dealership
'''
