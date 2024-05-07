# Lab 1

This is a ***Hello World Lab of Message Queues***.

This was done using **RabbitMQ**, **Docker**, **Python** and **Pika** Library.

With docker compose we spawn many consumers to showcase how to consume the same queue in parrallel.

## Default Values

- Port: 15672 for the web interface
- Port: 5672 for the rabbitmq service

For Dashboard access through: <http://localhost:15672/>

- Username: "guest"
- Password: "guest"

## Run this Lab

- `docker-compose up` to start all images and run the consumer, producer and the rabbitmq server
- `docker-compose up <SERVICE-NAME>` to start only the desired image
- `docker-compose down -v --rmi all --remove-orphans` to close the images and clean things up
