"""Tests for export_table_to_gcs."""
import unittest

from samples.utils import get_service, poll_job
from samples.export_data_to_cloud_storage import export_table
from test import constants


class TestExportTableToGCS(unittest.TestCase):

    def setUp(self):
        self.service = get_service()

    def test_export_table(self):
        resource = export_table(
                self.service, constants.GCS_OUTPUT_URI,
                constants.PROJECT_ID, constants.DATASET_ID,
                constants.CURRENT_TABLE_ID)
        self.assertIsNotNone(resource)

        resource = poll_job(self.service, **resource['jobReference'])

        self.assertEqual(resource['status']['state'], 'DONE')


if __name__ == '__main__':
    unittest.main()
