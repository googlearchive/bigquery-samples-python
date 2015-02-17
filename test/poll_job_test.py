from bigquery-getting-started-python import lib

def main(*arg, **kwargs):
    service = lib.get_service()
    job_resource = lib.export_table(
            service,
            kwargs['project_id'],
            kwargs['dataset_id'],
            kwargs['table_id'],
            kwargs['gcs_path']

    lib.poll_job(service, job_resource, 2, 33)

if __name__ == '__main__':
    main()
