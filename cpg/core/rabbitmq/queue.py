import functools
import logging


log = logging.getLogger(__name__)


class RabbitQueue:
    def __init__(self, queue_name, qos=1):
        self._name = queue_name
        self._qos = qos
        self._channel = None
        self._binding_key = None
        self.was_consuming = True
        self._consuming = False
        self._consumer_tag = None
        self._on_message = None

    def register_on_message(self, cb):
        self._on_message = cb

    def attach_channel(self, channel):
        self._channel = channel

    def setup_binding(self, _unused_frame, userdata):
        self._channel.queue_bind(
            self._name,
            userdata,
            routing_key=self.binding_key,
            callback=self.setup_qos,
        )

    def setup_qos(self, _unused_frame):
        self._channel.basic_qos(
            prefetch_count=self._qos, callback=self.start_consuming
        )

    def start_consuming(self, _unused_frame):
        log.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        cb = functools.partial(self._on_message, self._channel)
        self._consumer_tag = self._channel.basic_consume(self._name, cb)
        self.was_consuming = True
        self._consuming = True
        self._channel.activate_consumer_queue()

    def add_on_cancel_callback(self):
        log.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_cancelok(self, _unused_frame, userdata):

        self._consuming = False
        log.info(
            "RabbitMQ acknowledged the cancellation of the consumer: %s",
            userdata,
        )
        self._channel.deactivate_consumer_queue()
        if self._channel.consumer_queue_count == 0:
            self._channel.close_channel()

    def on_consumer_cancelled(self, method_frame):
        log.info(
            "Queue: %s Consumer was cancelled remotely, shutting down: %r",
            self._name,
            method_frame,
        )
        self._channel.deactivate_consumer_queue()
        if self._channel.consumer_queue_count <= 0:
            self._channel.close_channel()

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def binding_key(self):
        return self._binding_key

    @binding_key.setter
    def binding_key(self, val):
        self._binding_key = val
