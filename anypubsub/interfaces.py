from abc import ABCMeta, abstractmethod
import six


@six.add_metaclass(ABCMeta)
class Subscriber(object):
    @abstractmethod
    def __iter__(self):
        """The subscriber iterable"""


@six.add_metaclass(ABCMeta)
class PubSub(object):
    @abstractmethod
    def publish(self, channel, message):
        """Publish a message to channel"""

    @abstractmethod
    def subscribe(self, *channels):
        """Subscribe to one or many channels and return a `Subscriber` object"""