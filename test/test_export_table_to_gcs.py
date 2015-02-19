"""Tests for export_table_to_gcs."""
import unittest

from samples import auth
from samples import export_table_to_gcs
from test import constants


class TestExportTableToGCS(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_export_table(self):
        resource = export_table_to_gcs.export_table(
            self.service, constants.PROJECT_ID, constants.DATASET_ID,
            constants.CURRENT_TABLE_ID, constants.GCS_OUTPUT_URI)
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
