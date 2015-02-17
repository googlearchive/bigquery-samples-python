import pprint
import time

from oauth2client.client import AccessTokenRefreshError
from apiclient.errors import HttpError


def printTableData():
    pass

# [START synchronous_call]
# Run a synchronous query, save the results to a table, overwriting the
# existing data, and print the first page of results.
# Default timeout is to wait until query finishes.


def runSyncQuery(service, projectId, datasetId, timeout=0):
    try:
        print('timeout:%d' % timeout)
        jobCollection = service.jobs()
        queryData = {'query': 'SELECT word,count(word) AS count'
                              'FROM publicdata:samples.shakespeare'
                              'GROUP BY word;',
                     'timeoutMs': timeout}

        queryReply = jobCollection.query(projectId=projectId,
                                         body=queryData).execute()

        jobReference = queryReply['jobReference']

        # Timeout exceeded: keep polling until the job is complete.
        while not queryReply['jobComplete']:
            print('Job not yet complete...')
            queryReply = jobCollection.getQueryResults(
                projectId=jobReference['projectId'],
                jobId=jobReference['jobId'],
                timeoutMs=timeout).execute()

        # If the result has rows, print the rows in the reply.
        if 'rows' in queryReply:
            print('has a rows attribute')
            printTableData(queryReply, 0)
            currentRow = len(queryReply['rows'])

            # Loop through each page of data
            while ('rows' in queryReply and
                    currentRow < queryReply['totalRows']):
                queryReply = jobCollection.getQueryResults(
                    projectId=jobReference['projectId'],
                    jobId=jobReference['jobId'],
                    startIndex=currentRow).execute()
                if ('rows' in queryReply):
                    printTableData(queryReply, currentRow)
                    currentRow += len(queryReply['rows'])

    except AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize')

    except HttpError as err:
        print('Error in runSyncQuery:', pprint.pprint(err.content))

    except Exception as err:
        print('Undefined error' % err)
# [END synchronous_call]


# [START asynchronous_call]
def runAsyncQuery(service, projectId):
    try:
        jobCollection = service.jobs()
        queryString = ('SELECT corpus FROM publicdata:samples.shakespeare'
                       'GROUP BY corpus;')
        jobData = {
            'configuration': {
                'query': {
                    'query': queryString,
                }
            }
        }

        insertResponse = jobCollection.insert(projectId=projectId,
                                              body=jobData).execute()

        # Get query results. Results will be available for about 24 hours.
        currentRow = 0
        queryReply = jobCollection.getQueryResults(
            projectId=projectId,
            jobId=insertResponse['jobReference']['jobId'],
            startIndex=currentRow).execute()

        while(('rows' in queryReply) and currentRow < queryReply['totalRows']):
            printTableData(queryReply, currentRow)
            currentRow += len(queryReply['rows'])
            queryReply = jobCollection.getQueryResults(
                projectId=projectId,
                jobId=queryReply['jobReference']['jobId'],
                startIndex=currentRow).execute()

    except HttpError as err:
        print('Error in runAsyncTempTable:', pprint.pprint(err.resp))

    except Exception as err:
        print('Undefined error' % err)
# [END asynchronous_call]


# [START batched_call]
def runBatchedCall(service, projectId):
    try:
        jobCollection = service.jobs()
        queryString = ('SELECT corpus FROM publicdata:samples.shakespeare'
                       'GROUP BY corpus;')
        jobData = {
            'configuration': {
                'query': {
                    'query': queryString,
                    'priority': 'BATCH'  # Set priority to BATCH
                }
            }
        }

        insertResponse = jobCollection.insert(projectId=projectId,
                                              body=jobData).execute()

        while True:
            status = jobCollection.get(
                projectId=projectId,
                jobId=insertResponse['jobReference']['jobId']).execute()
            currentStatus = status['status']['state']

            if 'DONE' == currentStatus:
                currentRow = 0
                queryReply = jobCollection.getQueryResults(
                    projectId=projectId,
                    jobId=insertResponse['jobReference']['jobId'],
                    startIndex=currentRow).execute()

                while ('rows' in queryReply and
                       currentRow < queryReply['totalRows']):
                    printTableData(queryReply, currentRow)
                    currentRow += len(queryReply['rows'])
                    queryReply = jobCollection.getQueryResults(
                        projectId=projectId,
                        jobId=queryReply['jobReference']['jobId'],
                        startIndex=currentRow).execute()
            else:
                print('Waiting for the query to complete...')
                print('Current status: ' + currentStatus)
                print(time.ctime())
                time.sleep(10)

    except HttpError as err:
        print('Error in runAsyncTempTable:', pprint.pprint(err.resp))

    except Exception as err:
        print('Undefined error: %s' % err)
# [END batched_call]


# [START batched_async_call]
def runAsyncQueryBatch(service, projectId):
  try:
    jobCollection = service.jobs()
    queryString = 'SELECT corpus FROM publicdata:samples.shakespeare GROUP BY corpus;'
    jobData = {
      'configuration': {
        'query': {
          'query': queryString,
          'priority': 'BATCH' # Set priority to BATCH
        }
      }
    }

    insertResponse = jobCollection.insert(projectId=projectId,
                                         body=jobData).execute()

    import time
    while True:
      status = jobCollection.get(projectId=projectId, jobId=insertResponse['jobReference']['jobId']).execute()
      currentStatus = status['status']['state']

      if 'DONE' == currentStatus:
        currentRow = 0
        queryReply = jobCollection.getQueryResults(
                       projectId=projectId,
                       jobId=insertResponse['jobReference']['jobId'],
                       startIndex=currentRow).execute()

        while(('rows' in queryReply) and currentRow &lt; queryReply['totalRows']):
          printTableData(queryReply, currentRow)
          currentRow += len(queryReply['rows'])
          queryReply = jobCollection.getQueryResults(
                         projectId=projectId,
                         jobId=queryReply['jobReference']['jobId'],
                         startIndex=currentRow).execute()
      else:
        print 'Waiting for the query to complete...'
        print 'Current status: ' + currentStatus
        print time.ctime()
        time.sleep(10)

  except HttpError as err:
    print 'Error in runAsyncTempTable:', pprint.pprint(err.resp)

  except Exception as err:
    print 'Undefined error: %s' % err
# [END batched_async_call]
