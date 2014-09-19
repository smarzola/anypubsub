from collections import defaultdict
from anypubsub.interfaces import PubSub, Subscriber
from six.moves.queue import Queue

try:
    from weakref import WeakSet
except ImportError:  # pragma: nocover
    from weakrefset import WeakSet


class MemorySubscriber(Subscriber):
    def __init__(self):
        self.messages = Queue(maxsize=0)

    def __iter__(self):
        return self

    def next(self):
        return self.messages.get(block=True, timeout=None)

    __next__ = next   # PY3

    def put(self, message):
        self.messages.put_nowait(message)


class MemoryPubSub(PubSub):
    def __init__(self):
        self.subscribers = defaultdict(lambda: WeakSet())

    def publish(self, channel, message):
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.put(message)
        return len(subscribers)

    def subscribe(self, *channels):
        subscriber = MemorySubscriber()
        for channel in channels:
            self.subscribers[channel].add(subscriber)
        return subscriber

backend = MemoryPubSub