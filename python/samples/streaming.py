from __future__ import print_function

from samples.utils import get_service
import ast
import uuid
import json
import sys

# [START stream_row_to_bigquery]
def stream_row_to_bigquery(service,
                           project_id,
                           dataset_id,
                           table_id,
                           row,
                           num_retries=5):
    # Generate a unique row id so retries
    # don't accidentally duplicate insert
    insert_all_data = {
            'insertId': str(uuid.uuid4()),
            'rows': [{'json': row}]
            }
    return service.tabledata().insertAll(
                    projectId=project_id,
                    datasetId=dataset_id,
                    tableId=table_id,
                    body=insert_all_data).execute(num_retries=num_retries)
# [END stream_row_to_bigquery]


# [START run]
def run(project_id, dataset_id, table_id, rows, num_retries, out):
    service = get_service()
    for row in rows:
        response = stream_row_to_bigquery(service,
                                     project_id,
                                     dataset_id,
                                     table_id,
                                     row,
                                     num_retries)
        out.write(json.dumps(response))
        out.flush()


# [END run]


# [START main]
def get_rows():
    line = raw_input("Stream a row (python dict) into your bigquery table: ")
    while line:
        yield ast.literal_eval(line)
        line = raw_input(
                "Stream another row into your bigquery table \n" +
                "[hit enter to stop]: ")


def main():
    project_id = raw_input("Choose your project ID: ")
    dataset_id = raw_input("Choose a dataset ID: ")
    table_id = raw_input("Choose a table ID : ")
    num_retries = int(raw_input(
            "Enter number of times to retry in case of 500 error: "))
    out_path = raw_input(
            "Enter the path to write the results to (blank for stdout): ")

    with (sys.stdout if out_path=="" else open(out_path, 'w')) as out:
        run(project_id, dataset_id, table_id, get_rows(), num_retries, out)

# [END main]
