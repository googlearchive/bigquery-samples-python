from test.base_test import BaseBigqueryTest
from samples.async_query import run
import json


class TestAsyncQuery(BaseBigqueryTest):

    def test_async_query(self):
        with open('test_async_query_output.json', 'w+') as test_file:
            run(self.constants['projectId'],
                self.constants['query'],
                False,
                5,
                5,
                test_file)


        with open('stream_test.json', 'r') as test_file:
            self.assertIsNotNone(json.load(test_file.read()))



if __name__ == '__main__':
    unittest.main()
