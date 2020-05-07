import functools
import logging

log = logging.getLogger(__name__)


class Exchange:
    def __init__(self, exchange_name, exchange_type):
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._channel = None

    @property
    def exchange_type(self):
        return self._exchange_type

    @property
    def exchange_name(self):
        return self._exchange_name

    def __str__(self):
        return str(self.exchange_name)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def attach_channel(self, channel):
        self._channel = channel

    def setup_queues(self, binding, _unused_frame):
        log.info(_unused_frame)
        log.info(binding)
        queue = binding.queue
        queue.attach_channel(self._channel)
        if binding.is_consumer:
            cb = functools.partial(
                queue.setup_binding, userdata=str(binding.exchange)
            )
        else:
            cb = None
        self._channel.queue_declare(queue=str(queue), callback=cb)


class TopicExchange(Exchange):
    def __init__(self, exchange_name):
        super().__init__(exchange_name, "topic")
