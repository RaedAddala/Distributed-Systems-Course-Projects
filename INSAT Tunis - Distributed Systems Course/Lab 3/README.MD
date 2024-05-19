# Lab 3: Distributed Reader/Writer Synchronization using RabbitMQ

This is a **Distributed Reader/Writer Synchronization using RabbitMQ**.

Implemented using **RabbitMQ**, **Docker**, **Python**, **PyQt5**, and **Pika**.

## Description

## Default Values

- Port: 15672 for the RabbitMQ web interface
- Port: 5672 for the RabbitMQ service

For RabbitMQ Dashboard access, use: <http://localhost:15672/>

- Username: "guest"
- Password: "guest"

## Run this Lab

- `docker-compose up` to start all images and run the MySQL Server and the RabbitMQ Server.
- `docker-compose up <SERVICE-NAME>` to start only the desired image.
- `docker-compose down -v --rmi all --remove-orphans` to close the images and clean things up.

## Application Usage
