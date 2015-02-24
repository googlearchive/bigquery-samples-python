from __future__ import print_function  # For python 2/3 interoperability
from samples.utils import get_service, query_paging, poll_query


# [START async_query]
def async_query(service, project_id, query, batch=False):
    job_data = {
        'configuration': {
            'query': {
                    'query': query,
                    'priority': 'BATCH' if batch else 'INTERACTIVE',
                },
            }
        }
    return service.jobs().insert(
            projectId=project_id,
            body=job_data).execute()
# [END async_query]


# [START main]
def main():
    service = get_service()
    project_id = raw_input("Choose your project ID: ")
    query_string = raw_input("Enter your Bigquery SQL Query: ")
    batch = raw_input("Run query as batch?: ") in set(
            'True', 'true', 'y', 'Y', 'yes', 'Yes')

    query_job = async_query(service, project_id, query_string, batch)

    for page in query_paging(
            service, poll_query(service, **query_job['jobReference'])):
        print(page)
# [END main]
