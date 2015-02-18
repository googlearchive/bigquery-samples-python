"""Tests for auth."""
import unittest
from samples import auth


class TestAuth(unittest.TestCase):

    def test_get_service(self):
        service = auth.get_service()
        self.assertIsNotNone(service)


if __name__ == 'main':
    unittest.main()
