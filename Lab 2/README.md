# Lab 2: Database Synchronization using RabbitMQ

This is a ***Distributed Database Synchronization using RabbitMQ***.

Done using **RabbitMQ**, **MySQL**, **Docker**, **Python**, **PyQT5** and **Pika**.

## Description

**GOAL:** Synchronize Distributed SQL Databases across different instances using RabbitMQ message queues.

This projects runs a RabbitMQ Server and a MySQL Server on a docker image and exposes their services through their default ports.

Then the java code is divided into two parts:

- Head Office Code (*master*)
- Branch Office Code

Considering the limiting constraints of real life scenarios:

- Connection loss
- Servers/Systems failures

Synchronization is a must to ensure consistency between different instances of the DB

For this lab we assume one Head Office (HO) and 2 Branch offices (BO) for sales. The 2 sales branches are physically separated from the Head office. They manage their databases independently and they need to synchronise their data to the Head office that maintain the whole data of sales.

## Default Values

- Port: 15672 for the web interface
- Port: 5672 for the rabbitmq service
- Port: 3306 for MySQL Database Server

For RabbitMQ Dashboard, access through: <http://localhost:15672/>

- Username: "guest"
- Password: "guest"

## Run this Lab

- `docker-compose up` to start all images and run the MySQL Server and the RabbitMQ Server
- `docker-compose up <SERVICE-NAME>` to start only the desired image
- `docker-compose down -v --rmi all --remove-orphans` to close the images and clean things up
