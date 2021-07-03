from os import getenv
from celery import Celery, states

REDIS_HOST = getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = getenv("REDIS_PORT", "6379")
REDIS_PASS = getenv("REDIS_PASS", "password")
REDIS_DB = getenv("REDIS_DB_BACKEND", "0")

RABBITMQ_HOST = getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = getenv("RABBITMQ_PORT", "5672")
RABBITMQ_USER = getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = getenv("RABBITMQ_PASS", "guest")
RABBITMQ_VHOST = getenv("RABBITMQ_VHOST", "")

# RabbitMQ connection string: amqp://user:pass@localhost:5672/myvhost
BROKER = "amqp://{userpass}{hostname}{port}{vhost}".format(
    hostname=RABBITMQ_HOST,
    userpass=RABBITMQ_USER + ":" + RABBITMQ_PASS + "@" if RABBITMQ_USER else "",
    port=":" + RABBITMQ_PORT if RABBITMQ_PORT else "",
    vhost="/" + RABBITMQ_VHOST if RABBITMQ_VHOST else ""
)

# Redis connection string: redis://user:pass@hostname:port/db_number
BACKEND = "redis://{password}{hostname}{port}{db}".format(
    hostname=REDIS_HOST,
    password=':' + REDIS_PASS + '@' if REDIS_PASS else '',
    port=":" + REDIS_PORT if REDIS_PORT else "",
    db="/" + REDIS_DB if REDIS_DB else ""
)

tasks = Celery(broker=BROKER, backend=BACKEND)
