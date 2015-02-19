
import unittest

from samples import auth
from samples import sync_query
from samples import query
from test import constants


class TestSyncQuery(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()
        self.results = []

    def test_sync_query(self):
        resource = sync_query.sync_query(
            self.service, constants.PROJECT_ID, constants.QUERY)
        self.assertIsNotNone(resource)

    def test_get_results(self):
        resource = sync_query.sync_query(
                self.service, constants.PROJECT_ID, constants.QUERY)
        query.query_paging(
                self.service,
                query.query_polling(self.service, resource),
                lambda x: self.results.extend(x))
        self.assertNotEqual(self.results, [])

    def tearDown(self):
        self.results = None

if __name__ == '__main__':
    unittest.main()
