"""[START auth]"""
import httplib2
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
<<<<<<< HEAD
=======

>>>>>>> ccccfe9b549a493001478b0fcd8c4df1cf123ec6

def get_service():
    credentials = GoogleCredentials.get_application_default()
    http = credentials.authorize(httplib2.Http())
    return build('bigquery', 'v2', http=http)

"""[END auth]"""
