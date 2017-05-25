from collections import defaultdict
from anypubsub.interfaces import PubSub, Subscriber
from six.moves.queue import Queue
from weakref import WeakSet


class MemorySubscriber(Subscriber):
    def __init__(self, queue_factory):
        self.messages = queue_factory(maxsize=0)

    def __iter__(self):
        return self

    def next(self):
        return self.messages.get(block=True, timeout=None)

    __next__ = next   # PY3

    def put(self, message):
        self.messages.put_nowait(message)


class MemoryPubSub(PubSub):
    def __init__(self, queue_factory=Queue):
        self.subscribers = defaultdict(WeakSet)
        self.queue_factory = queue_factory

    def publish(self, channel, message):
        subscribers = self.subscribers[channel]
        for subscriber in subscribers:
            subscriber.put(message)
        return len(subscribers)

    def subscribe(self, *channels):
        subscriber = MemorySubscriber(self.queue_factory)
        for channel in channels:
            self.subscribers[channel].add(subscriber)
        return subscriber


backend = MemoryPubSub
