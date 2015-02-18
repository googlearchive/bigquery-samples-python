"""Tests for export_table_to_gcs."""
import unittest
from samples import auth
from samples import export_table_to_gcs


class TestExportTableToGCS(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_export_table(self):
        resource = export_table_to_gcs.export_table(
            self.service, 'foo', 'bar', 'baz', 'qux')
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
