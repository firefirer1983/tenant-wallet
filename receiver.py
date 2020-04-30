from pika import BlockingConnection
from pika.connection import URLParameters


connection = BlockingConnection(
    parameters=URLParameters("amqp://guest:guest@192.168.77.6:5672/%2F")
)
ch = connection.channel()
ch.exchange_declare(exchange="tenant.chain.action.tx", exchange_type="topic")
ch.exchange_declare(
    exchange="tenant.chain.action.address", exchange_type="topic"
)
ch.exchange_declare(
    exchange="tenant.chain.commodity.action.chaintask", exchange_type="topic"
)
ch.queue_declare("tenant_chain_action_q", exclusive=True)

ch.queue_bind(
    queue="tenant_chain_action_q",
    exchange="tenant.chain.action.tx",
    routing_key="*.*.",
)


def cb(channel, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


ch.basic_consume(queue=qname, on_message_callback=cb, auto_ack=True)
ch.start_consuming()
