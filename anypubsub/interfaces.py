class Subscriber(object):
    def __iter__(self):
        raise NotImplementedError


class PubSub(object):
    def publish(self, channel, message):
        raise NotImplementedError

    def subscribe(self, *channels):
        raise NotImplementedError