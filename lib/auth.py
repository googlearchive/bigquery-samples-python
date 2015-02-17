"""[START auth]"""

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery

def auth():
    credentials = GoogleCredentials.get_application_default()
    return build('bigquery', 'v2', credentials)

"""[END auth]"""

