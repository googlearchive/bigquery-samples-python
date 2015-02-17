# [START export_table_to_gcs]
def export_table(service, project_id, dataset_id, table_id, gcs_path):
    """starts a job which exports data from the specified table,
    to the specified Google Cloud Storage file, returns a job resource"""
    job_collection = service.jobs()
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
    job_resource = job_collection.insert(
        projectId=project_id,
        body=job_data).execute()
# [END export_table_to_gcs]
    return job_resource


