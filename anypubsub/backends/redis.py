from anypubsub.interfaces import Subscriber, PubSub


class RedisSubscriber(Subscriber):
    def __init__(self, connection, channels):
        self.pubsub = connection.pubsub()
        self.pubsub.subscribe(channels)

    def __iter__(self):
        return self

    def next(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                return message['data']

    __next__ = next  # PY3


class RedisPubSub(PubSub):
    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 connection_pool=None, charset='utf-8',
                 errors='strict', decode_responses=False):
        self.api = RedisPubSub._api()
        if connection_pool is None:
            kwargs = {
                'host': host,
                'port': port,
                'db': db,
                'password': password,
                'socket_timeout': socket_timeout,
                'encoding': charset,
                'encoding_errors': errors,
                'decode_responses': decode_responses
            }
            connection_pool = self.api.ConnectionPool(**kwargs)
        self.connection_pool = connection_pool

    @staticmethod
    def _api():
        return __import__('redis')

    def _get_connection(self):
        return self.api.Redis(connection_pool=self.connection_pool)

    def publish(self, channel, message):
        return self._get_connection().publish(channel, message)

    def subscribe(self, *channels):
        return RedisSubscriber(self._get_connection(), channels)

backend = RedisPubSub