from __future__ import print_function  # For python 2/3 interoperability
# [ START async_query ]
from samples import auth
from samples import query


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


def main():
    service = auth.get_service()
    project_id = raw_input("Choose your project ID: ")
    query_string = raw_input("Enter your Bigquery SQL Query: ")
    batch = raw_input("Run query as batch?: ") in set(
            'True', 'true', 'y', 'Y', 'yes', 'Yes')

    if batch:
        query_job = async_batch_query(service, project_id, query_string)
    else:
        query_job = async_query(service, project_id, query_string)

    query_response = service.jobs().getQueryResults(
            projectId=project_id,
            jobId=query_job['jobReference']['jobId']).execute()

    query.query_paging(
            service,
            query.polling(service, query_response),
            lambda x: print(x))
# [ END async_query ]
