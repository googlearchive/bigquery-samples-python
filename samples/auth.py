"""[START auth]"""
import httplib2
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build

def get_service():
    credentials = GoogleCredentials.get_application_default()
    http = credentials.authorize(httplib2.Http())
    return build('bigquery', 'v2', http=http)

"""[END auth]"""

