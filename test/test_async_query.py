
import unittest

from samples.utils import get_service
from samples.async_query import async_query
from test import constants


class TestAsyncQuery(unittest.TestCase):

    def setUp(self):
        self.service = get_service()

    def test_async_query(self):
        resource = async_query(
                self.service, constants.PROJECT_ID, constants.QUERY)
        self.assertIsNotNone(resource)

    def test_async_batch_query(self):
        resource = async_query(
                self.service, constants.PROJECT_ID,
                constants.QUERY, batch=True)
        self.assertIsNotNone(resource)


if __name__ == '__main__':
    unittest.main()
