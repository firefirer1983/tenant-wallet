from pika import BlockingConnection
from pika.connection import URLParameters
import pickle


class Msg:
    def __init__(self, content):
        self._content = content


connection = BlockingConnection(
    parameters=URLParameters("amqp://guest:guest@localhost:5672/%2F")
)
ch = connection.channel()
# ch.exchange_declare(exchange="tenant.chain.action.tx", exchange_type="topic")
# ch.exchange_declare(
#     exchange="tenant.chain.action.address", exchange_type="topic"
# )
# ch.exchange_declare(
#     exchange="tenant.chain.commodity.action.chaintask", exchange_type="topic"
# )
ch.basic_publish(
    exchange="tenant.chain.action.chain_task",
    routing_key="EGamer.eth.txcheck",
    body=pickle.dumps(Msg("Hello world!")),
)
