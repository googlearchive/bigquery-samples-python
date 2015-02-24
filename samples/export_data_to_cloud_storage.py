from samples.utils import get_service, poll_job


# [START export_table]
def export_table(service, cloud_storage_path,
                 projectId, datasetId, tableId):
    job_data = {
        'configuration': {
            'extract': {
                'sourceTable': {
                    'projectId': projectId,
                    'datasetId': datasetId,
                    'tableId': tableId,
                },
                'destinationUris': [cloud_storage_path],
            }
        }
    }
    return service.jobs().insert(
        projectId=projectId,
        body=job_data).execute()
# [END export_table]


# [START main]
def main():
    projectId = raw_input("Choose your project ID: ")
    datasetId = raw_input("Choose a dataset ID: ")
    tableId = raw_input("Choose a table name to copy: ")
    cloud_storage_path = raw_input("Enter a Google Cloud Storage URI: ")

    bigquery = get_service()
    resource = export_table(bigquery, cloud_storage_path,
                            projectId, datasetId, tableId)
    poll_job(bigquery, **resource['jobReference'])
    print 'Done exporting!'
# [END main]
