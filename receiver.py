import sys
from pika import BlockingConnection
from pika.credentials import PlainCredentials
from pika.connection import ConnectionParameters


connection = BlockingConnection(
    parameters=ConnectionParameters(
        host="localhost",
        credentials=PlainCredentials(username="user", password="bitnami"),
    )
)
binding_key = sys.argv[1:]
ch = connection.channel()
ch.exchange_declare(exchange="topic_log", exchange_type="topic")
result = ch.queue_declare("", exclusive=True)
qname = result.method.queue

ch.queue_bind(exchange="topic_log", routing_key=binding_key)


def cb(channel, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


ch.basic_consume(queue=qname, on_message_callback=cb, auto_ack=True)
ch.start_consuming()
