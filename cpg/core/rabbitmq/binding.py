import logging

log = logging.getLogger(__name__)


class Binding:
    def __init__(self, queue, exchange):
        self._queue = queue
        self._exchange = exchange

    @property
    def exchange(self):
        return self._exchange

    @property
    def queue(self):
        return self._queue

    @property
    def is_consumer(self):
        return isinstance(self, ConsumerBinding)


class ConsumerBinding(Binding):
    def __init__(self, queue, exchange):
        super().__init__(queue, exchange)

    def listen_on(self, binding_key):
        self._queue.binding_key = binding_key

        def _f(cb):
            self._queue.register_on_message(cb)

        return _f
