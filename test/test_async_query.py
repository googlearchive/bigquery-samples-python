
import unittest

from samples import auth
from samples import async_query
from test import constants


class TestAsyncQuery(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()
        self.results = []

    def test_async_query(self):
        resource = async_query.async_query(
            self.service, constants.PROJECT_ID, constants.QUERY)
        self.assertIsNotNone(resource)

    def test_async_batch_query(self):
        resource = async_query.async_batch_query(
            self.service, constants.PROJECT_ID, constants.QUERY)
        self.assertIsNotNone(resource)

    def test_get_async_query_results(self):
        resource = async_query.async_query(
                self.service, constants.PROJECT_ID, constants.QUERY)
        async_query.get_async_query_results(
                self.service,
                resource,
                lambda x: self.results.extend(x))
        self.assertNotEqual(self.results, [])

    def tearDown(self):
        self.results = None

if __name__ == '__main__':
    unittest.main()
