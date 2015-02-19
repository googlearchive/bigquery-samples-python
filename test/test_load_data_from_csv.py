"""Tests for load_data_from_csv."""
import unittest

from samples import auth
from samples import load_data_from_csv
from test import constants


class TestLoadDataFromCSV(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_load_table(self):
        resource = load_data_from_csv.load_table(
            self.service, constants.PROJECT_ID, constants.DATASET_ID,
            constants.NEW_TABLE_ID, constants.GCS_INPUT_URI)
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
