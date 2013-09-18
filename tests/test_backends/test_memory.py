import unittest


class TestMemoryPubSub(unittest.TestCase):
    def setUp(self):
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('memory')

    def test_subscriber_istance(self):
        from anypubsub.backends.memory import MemorySubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, MemorySubscriber)

    def test_pubsub(self):
        subscriber = self.pubsub.subscribe('a_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('a_chan', 'hello universe!')
        assert subscriber.messages.qsize() == 2, subscriber.messages.qsize()
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'

    def test_subscribe_multiple_chan(self):
        subscriber = self.pubsub.subscribe('a_chan', 'b_chan')
        self.pubsub.publish('a_chan', 'hello world!')
        self.pubsub.publish('b_chan', 'hello universe!')
        assert next(subscriber) == 'hello world!'
        assert next(subscriber) == 'hello universe!'

    def test_dispose_subscriber(self):
        subscriber = self.pubsub.subscribe('a_chan')
        assert self.pubsub.publish('a_chan', 'hello world!') == 1
        del subscriber
        assert self.pubsub.publish('a_chan', 'hello world!') == 0
