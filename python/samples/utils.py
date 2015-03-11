import os
import json
import httplib2
import time

RESOURCE_PATH='..'
MAX_AGE = 86400

# [START get_discovery_doc]
def get_discovery_doc(api, version):

    path = os.path.join(RESOURCE_PATH, '{}.{}'.format(api, version))
    try:
        age = time.time() - os.path.getmtime(path)
        if age > MAX_AGE:
            update_discovery_doc(api, version, path)
    except os.error:
        update_discovery_doc(api, version, path)

    with open(path, 'r') as discovery_doc:
        return discovery_doc.read()


def update_discovery_doc(api, version, path):
    from apiclient.discovery import DISCOVERY_URI
    from apiclient.errors import HttpError
    from apiclient.errors import InvalidJsonError
    import uritemplate

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
# [END get_discovery_doc]


# [START get_service]
def get_service():
    from oauth2client.client import GoogleCredentials
    from googleapiclient.discovery import build_from_document

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


# [START paging]
def paging(service, request_func, num_retries=5, **kwargs):
    has_next = True
    while has_next:
        response = request_func(**kwargs).execute(num_retries=num_retries)
        if 'pageToken' in response:
            kwargs['pageToken'] = response['pageToken']
        else:
            has_next = False
        yield response
# [END paging]
