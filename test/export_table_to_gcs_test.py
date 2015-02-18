"""Tests for export_table_to_gcs."""

from samples import auth, export_table_to_gcs, poll_job

def main(*arg, **kwargs):
    service = auth.get_service()
    job_resource = export_table_to_gcs.export_table(
            service,
            service.projects().list()['projects'][0]['projectReference']['projectId'],
            kwargs['dataset_id'],
            kwargs['table_id'],
            kwargs['gcs_path'])
    poll_job.poll_job(service, job_resource)

if __name__ == '__main__':
    main()
