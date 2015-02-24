import time
# [START get_service]
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build

from socket import timeout as Timeout


def get_service():
    credentials = GoogleCredentials.get_application_default()
    return build('bigquery', 'v2', credentials=credentials)
# [END get_service]


# [START poll_job]
def poll_job(service, projectId, jobId, timeout=1, max_timeout=33):
    job_get = service.jobs().get(
            projectId=projectId,
            jobId=jobId)
    job_resource = job_get.execute()

    while not job_resource['status']['state'] == 'DONE':
        if timeout > max_timeout:
            raise StandardError(
                    'Timed out waiting for job {} to complete, '
                    'after {} seconds'
                    .format(jobId, timeout-1))

        print('Job is {}, waiting {} seconds...'
              .format(job_resource['status']['state'], timeout))

        time.sleep(timeout)
        timeout *= 2
        job_resource = job_get.execute()

    return job_resource
# [END poll_job]


# [START poll_query]
def poll_query(service, projectId, jobId, timeout=30, max_tries=1):
    query_get = service.jobs().getQueryResults(
                    projectId=projectId,
                    jobId=jobId,
                    timeoutMs=timeout*1000)

    tries = 0
    while True:
        try:
            return query_get.execute()
        except Timeout:
            tries += 1
            if tries >= max_tries:
                raise
            print('Waiting for query to complete, '
                  '{} tries remaining'.format(max_tries - tries))
# [END poll_query]


# [START query_paging]
def query_paging(service, query_response):
    while 'rows' in query_response:
        yield query_response['rows']
        if 'pageToken' in query_response:
            page_token = query_response['pageToken']
            query_response = service.jobs().getQueryResults(
                projectId=query_response['jobReference']['projectId'],
                jobId=query_response['jobReference']['jobId'],
                pageToken=page_token).execute()
        else:
            return
# [END query_paging]
