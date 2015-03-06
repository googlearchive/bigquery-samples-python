import unittest

from samples.sync_query import run
from test.base_test import BaseBigqueryTest
import json


class TestSyncQuery(BaseBigqueryTest):

    def test_sync_query(self):
        with open('stream_test.json', 'w+') as test_file:
            run(self.constants['projectId'],
                self.constants['query'],
                5000,
                5,
                test_file)

        with open('stream_test.json', 'r') as test_file:
            self.assertIsNotNone(json.load(test_file.read()))


if __name__ == '__main__':
    unittest.main()
