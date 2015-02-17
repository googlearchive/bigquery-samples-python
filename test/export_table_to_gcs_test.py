"""Tests for export_table_to_gcs."""

import samples

def main(*arg, **kwargs):
    service = samples.get_service()
    job_resource = samples.export_table(
            service,
            kwargs['project_id'],
            kwargs['dataset_id'],
            kwargs['table_id'],
            kwargs['gcs_path'])
    samples.poll_job(service, job_resource)



if __name__ == '__main__':
    main()
