import os
import logging
from ..core.poll import Poll
from ..core.rabbitmq.queue import RabbitQueue
from ..core.rabbitmq.exchange import TopicExchange
from ..core.rabbitmq.binding import Binding, ConsumerBinding


log = logging.getLogger(__name__)

tenant = os.environ.get("tenant", "EGamer")
chain = os.environ.get("chain", "eth")

status_check_binding = ConsumerBinding(
    RabbitQueue("tenant_chain_action_q"),
    TopicExchange("tenant.chain.action.chain_task"),
)

status_check_result_binding = Binding(
    RabbitQueue("tenant_chain_status_q"),
    TopicExchange("tenant.chain.commodity.action.tx"),
)


# @status_check_binding.listen_on("%s.%s.txcheck" % (tenant, chain))
@status_check_binding.listen_on("*.*.*")
def check_transaction_status(channel, *args, **kwargs):
    log.info("check status request:")
    log.info(channel)
    log.info(args)
    log.info(kwargs)


class TransactionStatusPoll(Poll):
    def __init__(self):
        super().__init__(status_check_binding, status_check_result_binding)
        self.set_poll_interval(5)

    def poll(self):
        log.info("Transaction status polling alive!")
