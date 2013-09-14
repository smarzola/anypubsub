import unittest


class TestRedisPubSub(unittest.TestCase):
    def setUp(self):
        from anypubsub.pubsub import create_pubsub
        self.pubsub = create_pubsub('redis')

    def test_subscriber_istance(self):
        from anypubsub.backends.redis import RedisSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, RedisSubscriber)

    def test_pubsub(self):
        subscriber = self.pubsub.subscribe('a_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('a_chan', 'hello universe!')
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'

    def test_subscribe_multiple_chan(self):
        subscriber = self.pubsub.subscribe(['a_chan', 'b_chan'])
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('b_chan', 'hello universe!')
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'