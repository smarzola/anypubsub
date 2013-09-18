try:
    from Queue import Queue
except ImportError:
    from queue import Queue

try:
    from weakref import WeakSet
except ImportError:
    from weakrefset import WeakSet

from anypubsub.interfaces import PubSub, Subscriber


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
        self.subscribers = {}

    def publish(self, channel, message):
        subscribers = self.subscribers.get(channel, [])
        for subscriber in subscribers:
            subscriber.put(message)
        return len(subscribers)

    def subscribe(self, *channels):
        subscriber = MemorySubscriber()
        for channel in channels:
            subscribers = self.subscribers.setdefault(channel, WeakSet())
            subscribers.add(subscriber)
        return subscriber

backend = MemoryPubSub