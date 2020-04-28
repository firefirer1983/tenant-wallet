import sys
from pika import BlockingConnection
from pika.credentials import PlainCredentials
from pika.connection import ConnectionParameters


rkey = sys.argv[1]
msg = " ".join(sys.argv[2:])

connection = BlockingConnection(
    parameters=ConnectionParameters(
        host="localhost",
        credentials=PlainCredentials(username="user", password="bitnami"),
    )
)
ch = connection.channel()
exchange = ch.exchange_declare(exchange="topic_log", exchange_type="topic")
ch.basic_publish(exchange="topic_log", routing_key=rkey, body=msg)
connection.close()
