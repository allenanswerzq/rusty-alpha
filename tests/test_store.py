import unittest
import tempfile
import os
from llmcc.store import Store


class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store()

    def test_add_version(self):
        self.store.add_version({"data": "version 1"})
        self.assertEqual(self.store.current_version, 1)
        self.assertEqual(self.store.get_current_version(), {"data": "version 1"})

    def test_get_version(self):
        self.store.add_version({"data": "version 1"})
        self.store.add_version({"data": "version 2"})
        self.assertEqual(self.store.get_version(1), {"data": "version 1"})
        self.assertEqual(self.store.get_version(2), {"data": "version 2"})

    def test_rollback(self):
        self.store.add_version({"data": "version 1"})
        self.store.add_version({"data": "version 2"})
        self.store.rollback(1)
        self.assertEqual(self.store.current_version, 1)
        self.assertEqual(self.store.get_current_version(), {"data": "version 1"})

    def test_rollback_invalid_version(self):
        with self.assertRaises(ValueError):
            self.store.rollback(999)

    def test_list_versions(self):
        self.store.add_version({"data": "version 1"})
        self.store.add_version({"data": "version 2"})
        versions = self.store.list_versions()
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[1], {"data": "version 1"})
        self.assertEqual(versions[2], {"data": "version 2"})

    def test_save_and_load(self):
        self.store.add_version({"data": "version 1"})
        self.store.add_version({"data": "version 2"})

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            filename = tmp.name
            self.store.save_to_file(filename)

        loaded_store = Store.load_from_file(filename)
        self.assertEqual(loaded_store.current_version, 2)
        self.assertEqual(loaded_store.get_current_version(), {"data": "version 2"})
        self.assertEqual(loaded_store.get_version(1), {"data": "version 1"})

        os.unlink(filename)  # Clean up the temporary file


if __name__ == "__main__":
    unittest.main()
