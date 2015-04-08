
# [START get_service]
def get_service():
    from oauth2client.client import GoogleCredentials
    from googleapiclient.discovery import build_from_document
    from discovery_doc import get_discovery_doc
    import httplib2

    credentials = GoogleCredentials.get_application_default()

    return build_from_document(get_discovery_doc('bigquery', 'v2'),
                               http=httplib2.Http(),
                               credentials=credentials)
# [END get_service]


# [START poll_job]
def poll_job(service, projectId, jobId, interval=5, num_retries=5):
    import time

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
