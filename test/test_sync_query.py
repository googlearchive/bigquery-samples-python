
import unittest

from samples.utils import get_service
from samples.sync_query import sync_query
from test import constants


class TestSyncQuery(unittest.TestCase):

    def setUp(self):
        self.service = get_service()

    def test_sync_query(self):
        resource = sync_query(
            self.service, constants.PROJECT_ID, constants.QUERY)
        self.assertIsNotNone(resource)

if __name__ == '__main__':
    unittest.main()
