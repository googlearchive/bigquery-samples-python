from __future__ import print_function

# [START streaming_call]
from samples import auth
import ast


def stream_to_bigquery(service,
                       project_id,
                       dataset_id,
                       table_id,
                       row_generator):
    for row in row_generator:
        insert_all_data = {
                "rows": [{"json": row}]
                }
        yield service.tabledata().insertAll(
                        projectId=project_id,
                        datasetId=dataset_id,
                        tableId=table_id,
                        body=insert_all_data).execute()


def get_input():
    line = raw_input("Stream a line into your bigquery table:")
    while line:
        yield ast.literal_eval(line)
        line = raw_input(
                "Stream another line into your bigquery table \n" +
                "[hit enter to quit]:")


def main():
    service = auth.get_service()
    project_id = raw_input("Choose your project ID: ")
    dataset_id = raw_input("Choose a dataset ID: ")
    table_id = raw_input("Choose a table ID : ")

    for response in stream_to_bigquery(
            service,
            project_id,
            dataset_id,
            table_id,
            get_input()):
        print(response)
# [END streaming_call]
