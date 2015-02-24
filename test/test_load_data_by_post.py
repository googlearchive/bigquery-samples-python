import unittest
from oauth2client.client import GoogleCredentials
import httplib2
from test import constants
import json
# from samples.load_data_by_post import make_post


class TestLoadDataByPost(unittest.TestCase):

    def setUp(self):
        with open(constants.SCHEMA_PATH, 'r') as schema_file:
            self.schema = json.load(schema_file)

        with open(constants.DATA_PATH, 'r') as data_file:
            self.data = data_file.read()

        credentials = GoogleCredentials.get_application_default()
        self.http = credentials.authorize(httplib2.Http())

"""
    DEBUGGING
    def test_load_data_by_post(self):
        resource = make_post(self.http,
                             self.schema,
                             self.data,
                             constants.PROJECT_ID,
                             constants.DATASET_ID,
                             constants.CURRENT_TABLE_ID)
        self.assertIsNotNone(resource)
"""

if __name__ == '__main__':
    unittest.main()
