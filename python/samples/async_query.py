from __future__ import print_function  # For python 2/3 interoperability
from samples.utils import get_service, query_paging, poll_job
import uuid
import json


# [START async_query]
def async_query(service, project_id, query, batch=False, num_retries=5):
    # Generate a unique job_id so retries
    # don't accidentally duplicate query
    job_data = {
        'jobReference': {
                'projectId': project_id,
                'job_id': str(uuid.uuid4())
                },
        'configuration': {
                'query': {
                        'query': query,
                        'priority': 'BATCH' if batch else 'INTERACTIVE',
                        },
                }
        }
    return service.jobs().insert(
            projectId=project_id,
            body=job_data).execute(num_retries=num_retries)
# [END async_query]


# [START run]
def run(project_id, query_string, batch, num_retries, interval):
    service = get_service()

    query_job = async_query(service,
                            project_id,
                            query_string,
                            batch,
                            num_retries)

    poll_job(service,
             query_job['jobReference']['projectId'],
             query_job['jobReference']['jobId'],
             interval,
             num_retries)

    response = service.jobs().getQueryResults(
            **query_job['jobReference']).execute(num_retries=num_retries)

    for page in query_paging(service, response, num_retries):
        yield json.dumps(page)
# [END run]


# [START main]
def main():
    project_id = raw_input("Choose your project ID: ")
    query_string = raw_input("Enter your Bigquery SQL Query: ")
    batch = raw_input("Run query as batch?: ") in set(
            'True', 'true', 'y', 'Y', 'yes', 'Yes')
    num_retries = raw_input(
            "Enter number of times to retry in case of 500 error: ")
    interval = raw_input(
            "Enter how often to poll your query for completion (seconds): ")

    for result in run(project_id, query_string, batch, num_retries, interval):
        print(result)
# [END main]
