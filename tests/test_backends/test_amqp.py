import unittest


class TestAmqpPubSub(unittest.TestCase):
    def setUp(self):
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('amqp')

    def test_subscriber_istance(self):
        from anypubsub.backends.amqp import AmqpSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, AmqpSubscriber)

    def test_amqp_from_url(self):
        self.pubsub = None
        from anypubsub import create_pubsub
        self.pubsub = create_pubsub('amqp', host='amqp://')
        from anypubsub.backends.amqp import AmqpSubscriber
        subscriber = self.pubsub.subscribe('a_chan')
        assert isinstance(subscriber, AmqpSubscriber)

    def test_pubsub(self):
        from anypubsub import create_pubsub
        self.pubsub2 = create_pubsub('amqp')
        subscriber = self.pubsub2.subscribe('a_chan')
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
