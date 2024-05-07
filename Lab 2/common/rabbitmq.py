import pika
from pika.exceptions import AMQPError

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

def send_message(channel, queue_name, message):
    """Send a message to the specified queue."""
    try:
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2))  # Make message persistent
    except AMQPError as e:
        print(f"Failed to send message to {queue_name}: {e}")

def receive_messages(channel, queue_name, callback):
    """Start consuming messages from a specified queue with a callback function."""
    try:
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except AMQPError as e:
        print(f"Failed to receive messages from {queue_name}: {e}")

def close_connection(connection):
    """Close the RabbitMQ connection."""
    try:
        connection.close()
    except AMQPError as e:
        print(f"Failed to close RabbitMQ connection: {e}")
