from __future__ import print_function  # For python 2/3 interoperability
# [ START async_query ]

from samples import auth
from samples import poll_job


def async_batch_query(service, project_id, query):
    # [START query_job_data]
    job_data = {
        'configuration': {
            'query': {
                    'query': query,
                    'priority': 'BATCH',
                },
            }
        }
    # [END query_job_data]
    return service.jobs().insert(
            projectId=project_id,
            body=job_data).execute()


def async_query(service, project_id, query):
    # [START query_job_data]
    job_data = {
        'configuration': {
            'query': {
                    'query': query,
                },
            }
        }
    # [END query_job_data]
    return service.jobs().insert(
            projectId=project_id,
            body=job_data).execute()


def get_async_query_results(service, job_resource, output_data):
    # [START get_async_query_results]
    project_id = job_resource['jobReference']['projectId']
    job_id = job_resource['jobReference']['jobId']

    current_row = 0
    query_reply = service.jobs().getQueryResults(
            projectId=project_id,
            jobId=job_id,
            startIndex=current_row).execute()

    while ('rows' in query_reply) and current_row < query_reply['totalRows']:
        output_data(query_reply['rows'])
        current_row += len(query_reply['rows'])
        query_reply = service.jobs().getQueryResults(
            projectId=project_id,
            jobId=query_reply['jobReference']['jobId'],
            startIndex=current_row).execute()
    # [END get_async_query_results]


def main():
    service = auth.get_service()
    project_id = raw_input("Choose your project ID: ")
    query = raw_input("Enter your Bigquery SQL Query: ")
    batch = raw_input("Run query as batch?: ") in set(
            'True', 'true', 'y', 'Y', 'yes', 'Yes')

    if batch:
        query_job = async_batch_query(service, project_id, query)
    else:
        query_job = async_query(service, project_id, query)
    poll_job.poll_job(service, query_job)
    get_async_query_results(service, query_job, lambda x: print(x))

# [ END async_query ]
