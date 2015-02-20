"""Tests for export_table_to_gcs."""
import unittest

from samples import auth
from samples import streaming
from test import constants


class TestStreaming(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()
        self.generator = ({
                'Name': 'test',
                'Age': age,
                'Weight': 199.9,
                'IsMagic': False
                } for age in range(0, 2))

    def test_export_table(self):
        resource = [resource for resource in streaming.stream_to_bigquery(
                self.service,
                constants.PROJECT_ID,
                constants.DATASET_ID,
                constants.NEW_TABLE_ID,
                self.generator)]
        self.assertNotEqual(resource, [])

if __name__ == '__main__':
    unittest.main()
