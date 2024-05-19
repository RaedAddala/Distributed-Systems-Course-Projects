import pika
import os
import sys
import logging
import time

# setting Logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='producer.log')


def main():
    pass
    # # logging all informations 
    # logger.info('Started Producer!')

    # MESSAGE = "Hi!! - Learning RabbitMQ"

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

    # # publish a 100 messages to the queue
    # # for each 10 messages sleep for 2 seconds
    # for i in range(1,1001):
    #     if (i % 10 == 0):
    #         time.sleep(2)
    #     try:
    #         channel.basic_publish(exchange='', routing_key= QUEUE_NAME,body=MESSAGE)
    #         logger.info("Produced the message number "+str(i)+" successfully!")
    #     except Exception as e:
    #         logger.critical("Message Sending Failed at message number " + str(i))
    #         logger.critical("ERROR: " + e)
    
    # # close the channel and connection
    # channel.close()
    # connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)