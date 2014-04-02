from anypubsub import ConfigurationError
from anypubsub.interfaces import Subscriber, PubSub
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class AmqpSubscriber(Subscriber):
    def __init__(self, amqp_chan, exchanges):
        self.channel = amqp_chan
        self.messages = Queue(maxsize=0)
        qname, _, _ = self.channel.queue_declare()
        for exchange in exchanges:
            self.channel.queue_bind(qname, exchange)
        self.channel.basic_consume(queue=qname, callback=self.callback)

    def callback(self, msg):
        self.channel.basic_ack(msg.delivery_tag)
        self.messages.put_nowait(msg.body)

    def __iter__(self):
        return self

    def next(self):
        while self.messages.empty():
            self.channel.wait()
        return self.messages.get_nowait()

    __next__ = next   # PY3


class AmqpPubSub(PubSub):
    def __init__(self, host='localhost', userid='guest', password='guest', **kwargs):
        kwargs = dict(host=host, userid=userid, password=password, **kwargs)
        if kwargs['host'].startswith('amqp'):
            kwargs = self.parse_url(**kwargs)
        self.api = AmqpPubSub._api()
        self.connection = self._api().Connection(**kwargs)

    @staticmethod
    def parse_url(**kwargs):
        url = urlparse(kwargs['host'])
        if url.scheme != 'amqp':
            raise ConfigurationError('Invalid amqp uri scheme: %s' % url.scheme)
        kwargs.update({'host': url.netloc or 'localhost',
                       'userid': url.username or 'guest',
                       'password': url.password or 'guest'})
        return kwargs

    @staticmethod
    def _api():
        return __import__('amqp')

    @staticmethod
    def _declare_exchanges(chan, *exchanges):
        for exchange in exchanges:
            chan.exchange_declare(exchange, 'fanout')

    def _get_channel(self):
        return self.connection.channel()

    def subscribe(self, *channels):
        chan = self._get_channel()
        self._declare_exchanges(chan, *channels)
        return AmqpSubscriber(chan, channels)

    def publish(self, channel, message):
        chan = self._get_channel()
        self._declare_exchanges(chan, channel)
        msg = self.api.Message(message)
        chan.basic_publish(msg, channel)
        chan.close()


backend = AmqpPubSub