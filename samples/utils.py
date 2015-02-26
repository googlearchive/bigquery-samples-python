from test import constants
# [START get_service]
import uritemplate
import httplib2
import time
import json
import os

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build_from_document
# Libraries used by or included with Google APIs Client Library for Python
from apiclient.discovery import DISCOVERY_URI
from apiclient.errors import HttpError
from apiclient.errors import InvalidJsonError


def get_discovery_doc(api, version):
    path = "".join([constants.DISCOVERY_DOC_PATH, api, version])
    try:
        age = time.time() - os.path.getmtime(path)
        if age > constants.DISCOVERY_DOC_MAX_AGE:
            update_discovery_doc(api, version, path)
    except os.error:
        update_discovery_doc(api, version, path)

    with open(path, 'r') as discovery_doc:
        return discovery_doc.read()


def update_discovery_doc(api, version, path):
    requested_url = uritemplate.expand(DISCOVERY_URI,
                                       {'api': api, 'apiVersion': version})
    resp, content = httplib2.Http().request(requested_url)
    if resp.status >= 400:
        raise HttpError(resp, content, uri=requested_url)
    try:
        with open(path, 'w') as discovery_doc:
            discovery_json = json.loads(content)
            json.dump(discovery_json, discovery_doc)
    except ValueError:
        raise InvalidJsonError(
                'Bad JSON: %s from %s.' % (content, requested_url))


def get_service():
    credentials = GoogleCredentials.get_application_default()
    return build_from_document(get_discovery_doc('bigquery', 'v2'),
                               http=httplib2.Http(),
                               credentials=credentials)
# [END get_service]


# [START poll_job]
def poll_job(service, projectId, jobId, interval=5, num_retries=5):

    job_get = service.jobs().get(
            projectId=projectId,
            jobId=jobId)
    job_resource = job_get.execute(num_retries=num_retries)

    while not job_resource['status']['state'] == 'DONE':
        print('Job is {}, waiting {} seconds...'
              .format(job_resource['status']['state'], interval))
        time.sleep(interval)
        job_resource = job_get.execute(num_retries=num_retries)

    return job_resource
# [END poll_job]


# [START query_paging]
def query_paging(service, query_response, num_retries=5):
    while 'rows' in query_response:
        yield query_response['rows']
        if 'pageToken' in query_response:
            page_token = query_response['pageToken']
            query_response = service.jobs().getQueryResults(
                projectId=query_response['jobReference']['projectId'],
                jobId=query_response['jobReference']['jobId'],
                pageToken=page_token).execute(num_retries)
        else:
            return
# [END query_paging]
