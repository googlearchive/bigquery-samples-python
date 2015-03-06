from __future__ import print_function  # For python 2/3 interoperability
from samples.utils import get_service, query_paging
import json

# [START sync_query]
def sync_query(service, project_id, query, timeout=10000, num_retries=5):
    query_data = {
                    'query': query,
                    'timeoutMs': timeout,
                 }
    return service.jobs().query(
            projectId=project_id,
            body=query_data).execute(num_retries=num_retries)
# [END sync_query]


# [START run]
def run(project_id, query, timeout, num_retries, out):
    service = get_service()
    response = sync_query(service,
                          project_id,
                          query,
                          timeout,
                          num_retries)

    for page in query_paging(service, response, num_retries):
        json.dump(page, out)
# [END run]


# [START main]
def main():
    project_id = raw_input("Choose your project ID: ")
    query_string = raw_input("Enter your Bigquery SQL Query: ")
    timeout = raw_input(
            "Enter how long to wait for you query to complete in milliseconds\n"
            "(if longer than 10 seconds, use an asynchronous query): ")
    out_path = raw_input(
            "Enter the path to write the results to (blank for stdout): ")
    if out_path == "":
        out = sys.stdout
    else:
        out = open(out_path, 'w')

    run(project_id, query_string, timeout, num_retries, out)
# [END main]
