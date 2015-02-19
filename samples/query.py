from __future__ import print_function  # python 2/3 interoperability


# [START query_polling]
def query_polling(service, query_response, timeout=1, max_timeout=33):

    while not query_response['jobComplete'] and timeout < max_timeout:
        print("waiting {} seconds for query to complete".format(timeout))
        query_response = service.jobs().getQueryResults(
                projectId=query_response['jobReference']['projectId'],
                jobId=query_response['jobReference']['jobId'],
                timeoutMs=timeout*1000).execute()
        timeout = timeout * 2

    return query_response
# [END query_polling]


# [START query_paging]
def query_paging(service, query_response, output_data):
    while 'rows' in query_response:
        output_data(query_response['rows'])
        if 'pageToken' in query_response:
            page_token = query_response['pageToken']
            query_response = service.jobs().getQueryResults(
                projectId=query_response['jobReference']['projectId'],
                jobId=query_response['jobReference']['jobId'],
                pageToken=page_token).execute()
        else:
            query_response = {}
# [END query_paging]
