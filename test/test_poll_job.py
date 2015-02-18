import unittest
from samples import auth
from samples import export_table_to_gcs
from samples import poll_job


class TestPollJob(unittest.TestCase):

    def setUp(self):
        self.service = auth.get_service()

    def test_poll_job(self):
        resource = export_table_to_gcs.export_table(
            self.service, 'foo', 'bar', 'baz', 'qux')
        poll_job.poll_job(self.service, resource, 1, 17)


if __name__ == '__main__':
    unittest.main()
