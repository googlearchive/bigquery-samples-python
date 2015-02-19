import time


def poll_job(service, job_resource, timeout=2, max_timeout=33):
    # [START poll_job]
    job_status = job_resource['status']['state']
    while job_status != 'DONE' and timeout < max_timeout:
        job_status = job_resource['status']['state']
        job_resource = service.jobs().get(
            projectId=job_resource['jobReference']['projectId'],
            jobId=job_resource['jobReference']['jobId']).execute()
        print 'Waiting %d seconds for job to complete...' % timeout
        time.sleep(timeout)
        timeout = timeout * 2
    # [END poll_job]
