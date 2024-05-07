import random
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import uuid

DATABASE_URI = "mysql+pymysql://user:password@localhost/"

def initialize_database():
    """Create a new database with a unique name, create tables, and populate with initial data."""
    db_name = f"product_sales_{uuid.uuid4().hex[:8]}"
    try:
        engine = create_engine(f"{DATABASE_URI}{db_name}")
        session = get_session(engine)
    except SQLAlchemyError as e:
        print(f"Error initialising engine and session: {e}")
        return None, None, None
    try:
        create_tables(session)
        populate_initial_data(session)
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
        session.rollback()
        session.close_all()
        engine.dispose()
        return None, None, None
    return db_name, engine, session

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables(session):
    """Create the sales table in the database."""
    create_table_command = """
    CREATE TABLE sales (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE,
        Region VARCHAR(255),
        Product VARCHAR(255),
        Qty INT,
        Cost DECIMAL(10, 2),
        Amount DECIMAL(10, 2),
        Tax DECIMAL(10, 2),
        Total DECIMAL(10, 2)
    );
    """
    try:
        session.execute(create_table_command)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating tables: {e}")

def populate_initial_data(session):
    """Populate the sales table with random initial data."""
    products = [
        ('Paper', 12.95),
        ('Pens', 2.19),
        ('Staples', 5.00)
    ]
    for _ in range(10):  # Generate 10 entries
        date = f"2024-04-{random.randint(1, 30):02d}"
        region = random.choice(['East', 'West', 'North', 'South'])
        product, base_price = random.choice(products)
        qty = random.randint(1, 100)
        cost = round(base_price * random.uniform(0.95, 1.05), 2)
        amount = round(cost * qty, 2)
        tax = round(amount * 0.07, 2)
        total = round(amount + tax, 2)
        command = f"INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total) VALUES ({date}, {region}, {product}, {qty}, {cost}, {amount}, {tax}, {total})"
        try:
            session.execute(command)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error inserting data: {e}")

def insert_data(session, date, region, product, qty, cost, amount, tax, total):
    """Inserting new data to the table"""
    try:
        command = f"INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total) VALUES ({date}, {region}, {product}, {qty}, {cost}, {amount}, {tax}, {total})"
        session.execute(command)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting data: {e}")

def get_data(session):
    """Getting all data from the table"""
    try:
        command = "SELECT * FROM sales"
        result = session.execute(command)
        return result.fetchall()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error getting data: {e}")


def close_database(engine):
    """Close the database connection."""
    engine.dispose()
