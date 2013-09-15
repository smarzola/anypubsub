anypubsub
=========

.. image:: https://travis-ci.org/simock85/anypubsub.png?branch=master
   :target: https://travis-ci.org/simock85/anypubsub

A generic interface wrapping multiple backends to provide a consistent pubsub API.


Usage
------

Create a pubsub object::

    from anypubsub import create_pubsub
    pubsub = create_pubsub('redis')

or create a pubsub object from settings::

    from anypubsub import create_pubsub_from_settings
    pubsub = create_pubsub_from_settings({'anypubsub.backend': 'redis'}, prefix='anypubsub.')

Subscribe to a channel::

    subscriber = pubsub.subscribe('a_channel')

you can also subscribe to multiple channels::

    subscriber = pubsub.subscribe('a_channel', 'b_channel')

the subscriber is an iterator object that returns the next published message at each loop increment, and blocks until
next message is published.

Publish a message to a channel::

    pubsub.publish('a_channel', 'hello world!')

    message = next(subscriber)
    assert message == 'hello world!'

Supported backends
---------------------

* redis
* mongodb