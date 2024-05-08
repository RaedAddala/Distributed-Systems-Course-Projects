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

def setup_common_queue(channel, queue_name='common_queue'):
    """Declare a common queue for all messages."""
    try:
        channel.queue_declare(queue=queue_name, durable=True)
    except AMQPError as e:
        print(f"Failed to declare common queue {queue_name}: {e}")

def send_message(channel, queue_name, data):
    """Send a message to the specified queue."""
    try:
        message = json.dumps(data)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2))  # Make message persistent
        print("Message sent successfully.")
    except AMQPError as e:
        print(f"Failed to send message to {queue_name}: {e}")


def receive_messages(channel, queue_name, session, update_gui_callback):
    """Start consuming messages from a specified queue and handle data in a separate thread."""
    def callback(ch, method, properties, body):
        try:
            # Insert the data into the database
            message = process_message(session,body)
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
            print(f"Failed to receive messages from {queue_name}: {e}")

    # Start the consuming process in a separate thread to prevent blocking the main GUI thread
    thread = threading.Thread(target=start_consuming)
    thread.daemon = True  # Daemonize thread to close when the main program exits
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
