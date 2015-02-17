"""Tests for export_table_to_gcs."""


def main(*arg, **kwargs):
    service = lib.get_service()
    job_resource = lib.export_table(
            service,
            kwargs['project_id'],
            kwargs['dataset_id'],
            kwargs['table_id'],
            kwargs['gcs_path']



if __name__ == '__main__':
    main()
