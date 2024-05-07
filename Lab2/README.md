# Lab 2: Database Synchronization using RabbitMQ

This is a **Distributed Database Synchronization using RabbitMQ**.

Implemented using **RabbitMQ**, **MySQL**, **Docker**, **Python**, **PyQt5**, and **Pika**.

## Description

**GOAL:** Synchronize Distributed SQL Databases across different instances using RabbitMQ message queues.

This project runs a RabbitMQ Server and a MySQL Server on a docker image and exposes their services through their default ports.

The application is now developed in Python and utilizes PyQt5 for the GUI. It is divided into two main parts:

- **Head Office Code (HO)**: Responsible for aggregating and displaying synchronized data.
- **Branch Office Code (BO)**: Manages local data and synchronizes updates to the Head Office.

Considering the limiting constraints of real-life scenarios such as connection loss and server/system failures, synchronization is crucial to ensure consistency between different instances of the databases.

For this lab, we assume one Head Office (HO) and 2 Branch Offices (BO) for sales. The 2 sales branches are physically separated from the Head Office. They manage their databases independently and need to synchronize their data to the Head Office that maintains the whole data of sales.

## Default Values

- Port: 15672 for the RabbitMQ web interface
- Port: 5672 for the RabbitMQ service
- Port: 3306 for the MySQL Database Server

For RabbitMQ Dashboard access, use: <http://localhost:15672/>

- Username: "guest"
- Password: "guest"

## Run this Lab

- `docker-compose up` to start all images and run the MySQL Server and the RabbitMQ Server.
- `docker-compose up <SERVICE-NAME>` to start only the desired image.
- `docker-compose down -v --rmi all --remove-orphans` to close the images and clean things up.

In the Docker Desktop MySQL image, to connect to the MySQL shell, use: `mysql -u USERNAME -p`.

- To see all databases, use: `SHOW DATABASES;`.
- To use one particular database, use: `USE database_name;`.

## Application Usage

- Start the Head Office and Branch Office applications. Ensure that both are connected to their respective databases and the RabbitMQ service.
- Use the GUI provided to enter and synchronize data across offices.
