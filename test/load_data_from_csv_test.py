"""Tests for load_data_from_csv."""
import unittest
from samples import auth
from samples import load_data_from_csv


class TestLoadDataFromCSV(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_load_table(self):
        resource = load_data_from_csv.load_table(
            self.service, 'foo', 'bar', 'baz', 'qux')
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
