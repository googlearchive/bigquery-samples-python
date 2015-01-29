from lib import bigquery_service

PROJECT_ID = ""
DATASET_ID = ""
TABLE_ID = ""
bigquery = bigquery_service.getBigQueryService()

# [START streaming_call]
body = {"rows": [
    {"json": {"column_name": 7.7}}
    ]}
response = bigquery.tabledata().insertAll(
    projectId=PROJECT_ID,
    datasetId=DATASET_ID,
    tableId=TABLE_ID,
    body=body).execute()
# [END streaming_call]
