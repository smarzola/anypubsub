from datetime import datetime
import time
from anypubsub.interfaces import PubSub, Subscriber


class MongoSubscriber(Subscriber):
    def __init__(self, collection, channels):
        self.cursor = collection.find({'channel': {'$in': channels}, 'when': {'$gte': datetime.utcnow()}},
                                      tailable=True, await_data=True)

    def __iter__(self):
        return self

    def next(self):
        while self.cursor.alive:
            try:
                message = next(self.cursor)
                if message['type'] == 'message':
                    return message['message']
            except StopIteration:
                time.sleep(1)

    __next__ = next  # PY3


class MongoPubSub(PubSub):
    def __init__(self, host=None, port=None, max_pool_size=100,
                 client=None, database='anypubsub', collection='anyps_messages',
                 collection_size=10 * 2 ** 20):
        self.api = MongoPubSub._api()
        if client is None:
            client = self.api.MongoClient(host=host, port=port, max_pool_size=max_pool_size)
        db = client[database]
        try:
            db.create_collection(collection, size=collection_size, capped=True)
        except self.api.errors.CollectionInvalid:
            pass
        self.collection = db[collection]

    @staticmethod
    def _api():
        return __import__('pymongo')

    def publish(self, channel, message):
        self.collection.insert({'type': 'message', 'channel': channel, 'message': message, 'when': datetime.utcnow()})

    def subscribe(self, *channels):
        return MongoSubscriber(self.collection, channels)


backend = MongoPubSub




