import sys

sys.path.insert(0, '.')

import random
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import text

from common.rabbitmq import send_message

import uuid

DATABASE_URI = "mysql+pymysql://root:rootpassword@localhost/"

def get_engine(database=None):
    """Create and return an SQLAlchemy engine."""
    database_uri = f"{DATABASE_URI}{database}" if database else DATABASE_URI
    return create_engine(database_uri, echo=True, pool_pre_ping=True)

def initialize_database():
    """Create a new database with a unique name, create tables, and populate with initial data."""
    db_name = f"product_sales_{uuid.uuid4().hex[:8]}"
    engine = get_engine()  # Connect without specifying the database
    conn = engine.connect()
    
    # Attempt to create the database if it doesn't exist
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.close()  # Close the connection to the default database

    # Reconnect with the new database
    engine = get_engine(db_name)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    
    if not session:
        engine.dispose()
        return None, None, None
    try:
        create_tables(session)
    except SQLAlchemyError as e:
        print(f"Error during table creation: {e}")
        session.rollback()
        session.close()
        engine.dispose()
        return None, None, None
    return db_name, engine, Session


def create_tables(session):
    """Create the sales table in the database."""
    create_table_command =text("""
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
    """)
    try:
        session.execute(create_table_command)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
        session.rollback()

def populate_initial_data(session, channel, exchange_name='common_exchange'):
    """Populate the sales table with random initial data."""
    products = [('Paper', 12.95), ('Pens', 2.19), ('Staples', 5.00)]
    for _ in range(10):
        date = f"2024-04-{random.randint(1, 30):02d}"
        region = random.choice(['East', 'West', 'North', 'South'])
        product, base_price = random.choice(products)
        qty = random.randint(1, 100)
        cost = round(base_price * random.uniform(0.95, 1.05), 2)
        amount = round(cost * qty, 2)
        tax = round(amount * 0.07, 2)
        total = round(amount + tax, 2)
        data = {
            'Date': date, 
            'Region': region, 
            'Product': product, 
            'Qty': qty, 
            'Cost': cost, 
            'Amount': amount, 
            'Tax': tax, 
            'Total': total
        }
        try:
            session.execute(
                text("INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total) VALUES (:Date, :Region, :Product, :Qty, :Cost, :Amount, :Tax, :Total)"),
                data)
            session.commit()
            send_message(channel, exchange_name, data)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error inserting data: {e}")


def insert_data(Session, data):
    """Inserting new data to the table"""
    session = Session()
    try:
        command = text("""
        INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total)
        VALUES (:Date, :Region, :Product, :Qty, :Cost, :Amount, :Tax, :Total)
        """)
        session.execute(command,data)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting data: {e}")

def get_data(Session):
    """Getting all data from the table"""
    session = Session()
    try:
        command = text("SELECT * FROM sales")
        result = session.execute(command)
        return result.fetchall()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error getting data: {e}")


def close_database(engine):
    """Close the database connection."""
    engine.dispose()
