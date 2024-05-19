import pika
import os
import sys
import logging
import time

# setting Logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='consumer.log')

# def callback_function(ch, method, properties, body):
#     """function to receive the message from rabbitmq
#     print it
#     sleep for 1 second
#     ack the message"""

#     logger.info('Received msg : ', body.decode('utf-8'))
#     time.sleep(1)
#     logger.info('Acking it')
#     ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # logging all informations 
    logger.info('PASS')

    # # read rabbitmq connection url and queue name from environment variables
    # AMQP_URL = os.environ['AMQP_URL']
    # QUEUE_NAME = os.environ['QUEUE_NAME']
    
    # if not AMQP_URL or not QUEUE_NAME:
    #     logger.critical("ENVIRONMENT VARIABLES PROBLEMS: Make sure to pass AMQP_URL and QUEUE_NAME as an env var!")
    #     raise Exception('ENVIRONMENT VARIABLE UNSPECIFICED')
    # url_params = pika.URLParameters(AMQP_URL)
    # if not url_params:
    #     logger.critical("URL Params extraction Failed")
    #     raise Exception('URL Params extraction Failed')
    # # connect to rabbitmq
    # connection = pika.BlockingConnection(url_params) # Connect to RabbitMQ
    # if not connection:
    #     logger.critical("Connection to RabbitMQ Failed")
    #     raise Exception('Connection to RabbitMQ Failed')
    
    # logger.info("Connexion is established successfully")
    
    # channel = connection.channel() # start a channel
    # if not channel:
    #     logger.critical("Channel Creation Failed")
    #     raise Exception('Channel Creation Failed')
    
    # logger.info("Channel is created successfully")

    # try:
    #     channel.queue_declare(queue=QUEUE_NAME,durable=True) # Declare a queue
    #     logger.info(QUEUE_NAME + " queue is created successfully")
    # # durable flag is set so that messages are retained
    # # in the rabbitmq volume even between restarts 
    # except Exception as e:
    #     logger.critical("Queue Creation Failed")
    #     logger.critical("ERROR: " + e)       

    
    # # to make sure the consumer receives only one message at a time
    # # next message is received only after acking the previous one
    # channel.basic_qos(prefetch_count=1)

    # # define the queue consumption
    # channel.basic_consume(queue=QUEUE_NAME,on_message_callback=callback_function)
    # logger.info("Waiting to consume.")
    # # start consuming
    # channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)