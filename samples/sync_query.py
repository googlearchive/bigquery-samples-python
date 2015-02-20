from __future__ import print_function  # For python 2/3 interoperability

# [START sync_query]

from samples import auth
from samples import query


def sync_query(service, project_id, query, timeout=0):
    """ Run a synchronous query"""

    # [START query_data]
    query_data = {
                    'query': query,
                    'timeoutMs': timeout,
                 }
    # [END query_data]

    return service.jobs().query(
            projectId=project_id,
            body=query_data).execute()


def main():
    service = auth.get_service()
    project_id = raw_input("Choose your project ID: ")
    query_string = raw_input("Enter your Bigquery SQL Query: ")

    for page in query.query_paging(service, query.query_polling(
            service, sync_query(service, project_id, query_string))):
        print(page)
# [END sync_query]
