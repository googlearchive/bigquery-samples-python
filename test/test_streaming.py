"""Tests for export_table_to_gcs."""
import unittest

from samples import auth
from samples import streaming
from test import constants


class TestStreaming(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_stream_row_to_bigquery(self):
        for age in range(0, 2):
            row = {
                    'Name': 'test',
                    'Age': age,
                    'Weight': 199.9,
                    'IsMagic': False
                    }
            resource = streaming.stream_row_to_bigquery(
                    self.service,
                    constants.PROJECT_ID,
                    constants.DATASET_ID,
                    constants.NEW_TABLE_ID,
                    row)
            self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
