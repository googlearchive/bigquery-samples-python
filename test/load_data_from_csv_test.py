"""Tests for load_data_from_csv."""

import samples

def main(*arg, **kwargs)
    service = samples.get_service()
    job_resource = samples.export_table(
            service,
            kwargs['project_id'],
            kwargs['dataset_id'],
            kwargs['table_id'],
            kwargs['source_csv'])
    samples.poll_job(service, job_resource)


if __name__ == '__main__':
  googletest.main()
