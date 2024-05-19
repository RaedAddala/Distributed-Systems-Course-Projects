import threading
import json
import pika
from pika.exceptions import AMQPError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

def create_connection():
    """Create and return a RabbitMQ connection and channel."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        return connection, channel
    except AMQPError as e:
        print(f"Failed to create a RabbitMQ connection: {e}")
        return None, None

def setup_common_exchange(channel, exchange_name='common_exchange'):
    """Declare a common fanout exchange for all messages."""
    try:
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)
    except AMQPError as e:
        print(f"Failed to declare common exchange {exchange_name}: {e}")

def send_message(channel, exchange_name, data):
    """Send a message to the specified exchange."""
    try:
        message = json.dumps(data)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='',  # Not used with fanout exchange
            body=message,
            properties=pika.BasicProperties(delivery_mode=2))  # Make message persistent
        print("Message sent successfully.")
    except AMQPError as e:
        print(f"Failed to send message to exchange {exchange_name}: {e}")

def receive_messages(channel, exchange_name, session, update_gui_callback):
    """Start consuming messages from a specified exchange and handle data in a separate thread."""
    # Each consumer needs its own queue, which gets messages from the exchange
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def callback(ch, method, properties, body):
        try:
            message = process_message(session, body)
            update_gui_callback(message)  # Update the GUI with the processed data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except SQLAlchemyError as e:
            print(f"Database error during insertion: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    def start_consuming():
        try:
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except AMQPError as e:
            print(f"Failed to receive messages from {exchange_name}: {e}")

    # Use a separate thread to not block the main GUI thread
    thread = threading.Thread(target=start_consuming)
    thread.daemon = True
    thread.start()

def insert_data(session, **data):
    try:
        command = text("""
        INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total)
        VALUES (:Date, :Region, :Product, :Qty, :Cost, :Amount, :Tax, :Total)
        """)
        session.execute(command, data)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")

def process_message(session, body):
    """Process incoming message and insert into the local database."""
    try:
        data = json.loads(body.decode('utf-8'))
        command = text("""
        INSERT INTO sales (Date, Region, Product, Qty, Cost, Amount, Tax, Total)
        VALUES (:Date, :Region, :Product, :Qty, :Cost, :Amount, :Tax, :Total)
        """)
        session.execute(command, data)
        session.commit()
        return f"Data inserted: {data}"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Database error: {e}"
    except json.JSONDecodeError:
        return "Failed to decode the message."

def close_connection(connection):
    """Close the RabbitMQ connection."""
    try:
        connection.close()
    except AMQPError as e:
        print(f"Failed to close RabbitMQ connection: {e}")
