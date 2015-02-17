"""[START loadTable]"""

def loadTable(service, projectId, datasetId, targetTableId, sourceCSV):
    try:
        jobCollection = service.jobs()
        jobData = {
                'projectId': projectId,
                'configuration': {
                        'load': {
                                'sourceUris': [sourceCSV],
                                'schema': {
                                        'fields': [
                                                {
                                                        'name': 'Name',
                                                        'type': 'STRING'
                                                        },
                                                {
                                                        'name': 'Age',
                                                        'type': 'INTEGER'
                                                        },
                                                {
                                                        'name': 'Weight',
                                                        'type': 'FLOAT'
                                                        },
                                                {
                                                        'name': 'IsMagic',
                                                        'type': 'BOOLEAN'
                                                        }
                                                ]
                                        },
                                'destinationTable': {
                                        'projectId': projectId,
                                        'datasetId': datasetId,
                                        'tableId': targetTableId
                                        },
                                }
                        }
                }

        insertResponse = jobCollection.insert(projectId=projectId,
                                              body=jobData).execute()

        # Ping for status until it is done, with a short pause between calls.
        import time
        while True:
            job = jobCollection.get(projectId=projectId,
                                    jobId=insertResponse['jobReference']['jobId']).execute()
            if 'DONE' == job['status']['state']:
                print 'Done Loading!'
        return

        print 'Waiting for loading to complete...'
        time.sleep(10)

        if 'errorResult' in job['status']:
            print 'Error loading table: ', pprint.pprint(job)
        return

    except HttpError as err:
        print 'Error in loadTable: ', pprint.pprint(err.resp)

"""[END loadTable]"""
