from mock import patch
import unittest


class TestPubSub(unittest.TestCase):
    def test_create_pubsub(self):
        from anypubsub import create_pubsub
        from anypubsub.backends.memory import MemoryPubSub
        pubsub = create_pubsub('memory')
        assert isinstance(pubsub, MemoryPubSub)

    def test_create_pubsub_from_settings(self):
        from anypubsub import create_pubsub_from_settings
        from anypubsub.backends.memory import MemoryPubSub
        pubsub = create_pubsub_from_settings({'backend': 'memory'})
        assert isinstance(pubsub, MemoryPubSub)

    def test_create_pubsub_from_settings_with_prefix(self):
        from anypubsub import create_pubsub_from_settings
        from anypubsub.backends.memory import MemoryPubSub
        pubsub = create_pubsub_from_settings({'foo.backend': 'memory'}, prefix='foo.')
        assert isinstance(pubsub, MemoryPubSub)

    @patch('anypubsub.pubsub._load_entry_point')
    def test_create_nonexistent_pubsub(self, load_entry_point):
        from anypubsub.pubsub import create_pubsub, ConfigurationError
        load_entry_point.return_value = None
        self.assertRaises(ConfigurationError, create_pubsub, 'foobar')
        load_entry_point.assert_called_with('foobar')

    @patch('anypubsub.pubsub._load_entry_point')
    def test_create_pubsub_from_entrypoint(self, load_entry_point):
        from anypubsub.pubsub import _load_backend
        load_entry_point.return_value = 'foobar_module'
        result = _load_backend('foobar')
        load_entry_point.assert_called_with('foobar')
        assert result == 'foobar_module'