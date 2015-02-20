# [START export_table_to_gcs]
from samples import auth
from samples import poll_job


def export_table(service, project_id, dataset_id, table_id, gcs_path):
    """starts a job which exports data from the specified table,
    to the specified Google Cloud Storage file, returns a job resource"""
    job_collection = service.jobs()
    # [START job_data]
    job_data = {
        'projectId': project_id,
        'configuration': {
            'extract': {
                'sourceTable': {
                    'projectId': project_id,
                    'datasetId': dataset_id,
                    'tableId': table_id,
                },
                'destinationUris': [gcs_path],
            }
        }
    }
    # [END job_data]
    job_resource = job_collection.insert(
        projectId=project_id,
        body=job_data).execute()
    return job_resource


def main():
    project_id = raw_input("Choose your project ID: ")
    dataset_id = raw_input("Choose a dataset ID: ")
    table_id = raw_input("Choose a table name to copy: ")
    gcs_path = raw_input("Enter a Google Cloud Storage URI: ")

    bigquery = auth.get_service()
    resource = export_table(bigquery, project_id, dataset_id, table_id,
                            gcs_path)
    poll_job.poll_job(bigquery, resource)
    print 'Done exporting!'
# [END export_table_to_gcs]
