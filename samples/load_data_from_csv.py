#[START load_table_from_csv]
def load_table(service, project_id, dataset_id, table_id, source_csv):
    job_collection = service.jobs()
    job_data = {
            'projectId': project_id,
            'configuration': {
                    'load': {
                            'sourceUris': [source_csv],
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
                                    'projectId': project_id,
                                    'datasetId': dataset_id,
                                    'tableId': table_id
                                    },
                            }
                    }
            }

    job_resource = jobCollection.insert(
            projectId=project_id,
            body=job_data).execute()
#[END load_table_from_csv]
    return job_resource
