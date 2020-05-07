import os
import abc
from .rabbitmq.channel import Channel

amqp_url = os.environ.get("amqp_url", "amqp://guest:guest@localhost:5672/%2F")


class Poll(abc.ABC):
    def __init__(self, *bindings):
        self._poll_interval = 500
        self._channel = self.init_mq(amqp_url, *bindings)

    @abc.abstractmethod
    def poll(self):
        pass

    @staticmethod
    def init_mq(url, *bindings):
        return Channel(url, *bindings)

    @property
    def poll_interval(self):
        return self._poll_interval

    def set_poll_interval(self, interval):
        self._poll_interval = interval

    def run(self):
        self._channel.install_poll(self.poll, self._poll_interval)
        self._channel.run()

    @property
    def channel(self):
        return self._channel
