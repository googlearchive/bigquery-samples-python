"""
This example shows how to do an async BigQuery query.
The 'create_bigquery_client' function assumes that this code is running on a GCE
instance set up with the BigQuery scope.  See the BigQuery documentation for
more information on client authorization.
"""
import httplib2
import sys
import time

import oauth2client.gce as gce_oauth2client
from apiclient import discovery

BIGQUERY_SCOPES = ['https://www.googleapis.com/auth/bigquery']
## change this to your project
PROJECT_ID = xxxxxxxxxx

def create_bigquery_client():
  credentials = gce_oauth2client.AppAssertionCredentials(
      scope=BIGQUERY_SCOPES)
  http = httplib2.Http()
  credentials.authorize(http)
  return discovery.build('bigquery', 'v2', http=http)


def insert_query(query, service):
  job_data = {'configuration': {'query': {'query': query}}}
  return service.jobs().insert(
      projectId=PROJECT_ID,body=job_data).execute()

def job_status(job_id, service):
  return service.jobs().get(
      projectId=PROJECT_ID, jobId=job_id).execute()

def get_query_results(job_id, service, start_row):
  return service.jobs().getQueryResults(
      projectId=PROJECT_ID, jobId=job_id,
      startIndex=start_row).execute()

def main(argv):

  client = create_bigquery_client()
  # Insert the query
  res = insert_query(
      'SELECT corpus FROM publicdata:samples.shakespeare GROUP BY corpus;',
      client)
  # Get the job id
  job_id = res['jobReference']['jobId']
  print "job id: %s" % job_id
  # Wait until the job status is 'DONE'
  status = job_status(job_id, client)
  print "job status is: %s" % status['status']['state']
  while status['status']['state'] != 'DONE':
    print "..."
    time.sleep(1)
    status = job_status(job_id, client)
    print "job status is: %s" % status['status']['state']

  # Then get the query results.  Start from row 0.  With a larger result set,
  # you can page through.
  res = get_query_results(job_id, client, 0)
  print "query response rows: %s" % res['rows']



if __name__ == '__main__':
    main(sys.argv)
