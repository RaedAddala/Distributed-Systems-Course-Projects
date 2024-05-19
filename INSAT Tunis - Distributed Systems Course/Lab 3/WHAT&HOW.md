# Explaining RabbitMQ

## What is RabbitMQ

**RabbitMQ** is an _open-source_ _**message-broker**_ software that allows applications to communicate by exchanging data as messages via queues.

It supports multiple messaging protocols and provides features for _reliable delivery_, _routing_, and _federation_, making it versatile for various use cases such as decoupling services and streaming.

## What is a message broker

A **message broker** is an intermediary software that enables applications, systems, and services to communicate and exchange information by translating messages between different messaging protocols. It facilitates **decoupling of processes within systems, ensuring that senders can issue messages without knowing the receivers’ details**. This allows for:

- reliable message storage
- guaranteed delivery
- asynchronous communication

## How does RabbitMQ works

**RabbitMQ** works by **defining queues** to store messages sent by producers. These messages are stored until consuming applications retrieve and process them. It uses a **publish-subscribe model** where messages are sent to _**“exchanges"**_ and then routed to relevant _**“queues”**_ based on configurable rules. This allows for the design and implementation of distributed systems, where a system is divided into independent modules that communicate through messages.

## RabbitMQ use cases

- Handling Background Jobs (i.e: manage long-running tasks and/or high-throughput background jobs)
- Decoupling Applications/Services (easy and reliable communication making it one of the best technologies that microservices rely on)
- Complex Routing Schemes within big systems

In a Nutshell, RabbitMQ solves a lot of Distributed Systems problems.

## Ressources & Further Studies

- [RabbitMQ for beginners - What is RabbitMQ](https://www.cloudamqp.com/blog/part1-rabbitmq-for-beginners-what-is-rabbitmq.html)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [RabbitMQ - an introduction](https://www.confluent.io/learn/rabbitmq/)
