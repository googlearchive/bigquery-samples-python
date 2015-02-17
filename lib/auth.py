import httplib2
import pprint
import sys
import os

from apiclient.discovery import build
from apiclient.errors import HttpError


from oauth2client.client import SignedJwtAssertionCredentials

def bq_service_init():
    """[START auth]"""
    """id for the project (e.g. my-app-000)"""
    project_id = os.environ['PROJECT_ID']
    """email address for your project's service account"""
    account = os.environ['ACCOUNT']
    """json private key file"""
    with open('credentials.json','r') as cred_file:
        credentials_json = cred_file.read()

    credentials = SignedJwtAssertionCredentials(
            account,
            credentials_json,
            scope='https://www.googleapis.com/auth/bigquery')


    http = httplib2.Http()
    http = credentials.authorize(http)
    bigquery_service = build('bigquery', 'v2', http=http)

    """[END auth]"""

    return bigquery_service
