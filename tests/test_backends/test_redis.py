import unittest


class TestRedisPubSub(unittest.TestCase):
    def setUp(self):
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('redis')

    def test_subscriber_istance(self):
        from anypubsub.backends.redis import RedisSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, RedisSubscriber)

    def test_iteration_protocol(self):
        subscriber = self.pubsub.subscribe('a_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        subscriber = iter(subscriber)
        assert next(subscriber) == b'hello world!'

    def test_redis_from_url(self):
        self.pubsub = None
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('redis', host='redis://localhost:6379/0')
        from anypubsub.backends.redis import RedisSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, RedisSubscriber)

    def test_pubsub(self):
        subscriber = self.pubsub.subscribe('a_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('a_chan', 'hello universe!')
        assert next(subscriber) == b'hello world!'
        assert next(subscriber) == b'hello universe!'

    def test_subscribe_multiple_chan(self):
        subscriber = self.pubsub.subscribe('a_chan', 'b_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('b_chan', 'hello universe!')
        assert next(subscriber) == b'hello world!'
        assert next(subscriber) == b'hello universe!'

    def test_not_subscribed_chan(self):
        subscriber = self.pubsub.subscribe('a_chan', 'c_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('b_chan', 'junk message')
        self.pubsub.publish('c_chan', 'hello universe!')
        assert next(subscriber) == b'hello world!'
        assert next(subscriber) == b'hello universe!'