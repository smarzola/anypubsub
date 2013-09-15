import unittest


class TestMongoPubSub(unittest.TestCase):
    def setUp(self):
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('mongodb')

    def test_subscriber_istance(self):
        from anypubsub.backends.mongodb import MongoSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, MongoSubscriber)

    def test_pubsub(self):
        subscriber = self.pubsub.subscribe('a_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('a_chan', 'hello universe!')
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'

    def test_subscribe_multiple_chan(self):
        subscriber = self.pubsub.subscribe('a_chan', 'b_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('b_chan', 'hello universe!')
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'