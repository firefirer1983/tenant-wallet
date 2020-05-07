import pickle
from pika import BlockingConnection
from pika.connection import URLParameters


class Msg:
    def __init__(self, content):
        self._content = content


connection = BlockingConnection(
    parameters=URLParameters("amqp://guest:guest@localhost:5672/%2F")
)
ch = connection.channel()
ch.exchange_declare(exchange="tenant.chain.action.chain_task", exchange_type="topic")

ch.queue_declare("tenant_chain_action_q")

ch.queue_bind(
    queue="tenant_chain_action_q",
    exchange="tenant.chain.action.chain_task",
    routing_key="*.*.*",
)


def cb(channel, method, properties, body):
    if isinstance(body, bytes):
        print(" [x] %r:%r" % (method.routing_key, pickle.loads(body)))
    else:
        print(" [x] %r:%r" % (method.routing_key, body))


ch.basic_consume(
    queue="tenant_chain_action_q", on_message_callback=cb, auto_ack=True
)
ch.start_consuming()
