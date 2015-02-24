"""Tests for load_data_from_csv."""
import unittest

from test import constants
from samples.utils import get_service
from samples.load_data_from_csv import load_table
import json


class TestLoadDataFromCSV(unittest.TestCase):

    def setUp(self):
        self.service = get_service()
        with open(constants.SCHEMA_PATH, 'r') as schema_file:
            self.schema = json.load(schema_file)

    def test_load_table(self):
        resource = load_table(
                self.service,
                self.schema,
                constants.GCS_INPUT_URI,
                constants.PROJECT_ID,
                constants.DATASET_ID,
                constants.NEW_TABLE_ID)
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
