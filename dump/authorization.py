# [START installed_apps]

import httplib2
import pprint
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

# Enter your Google Developer Project number
PROJECT_NUMBER = 'XXXXXXXXXXXXX'
FLOW = flow_from_clientsecrets('client_secrets.json',
                               scope='https://www.googleapis.com/auth/bigquery')


def main():
  storage = Storage('bigquery_credentials.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  http = httplib2.Http()
  http = credentials.authorize(http)

  bigquery_service = build('bigquery', 'v2', http=http)

  try:
    datasets = bigquery_service.datasets()
    listReply = datasets.list(projectId=PROJECT_NUMBER).execute()
    print 'Dataset list:'
    pprint.pprint(listReply)

  except HttpError as err:
    print 'Error in listDatasets:', pprint.pprint(err.content)

  except AccessTokenRefreshError:
    print ("Credentials have been revoked or expired, please re-run"
           "the application to re-authorize")

if __name__ == '__main__':
  main()

# [END installed_apps]


# [START service_accounts]
import httplib2

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# REPLACE WITH YOUR Project ID
PROJECT_NUMBER = 'XXXXXXXXXXX'
# REPLACE WITH THE SERVICE ACCOUNT EMAIL FROM GOOGLE DEV CONSOLE
SERVICE_ACCOUNT_EMAIL = 'XXXXX@developer.gserviceaccount.com'

f = file('key.p12', 'rb')
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(
    SERVICE_ACCOUNT_EMAIL,
    key,
    scope='https://www.googleapis.com/auth/bigquery')

http = httplib2.Http()
http = credentials.authorize(http)

service = build('bigquery', 'v2')
datasets = service.datasets()
response = datasets.list(projectId=PROJECT_NUMBER).execute(http)

print('Dataset list:\n')
for dataset in response['datasets']:
  print("%s\n" % dataset['id'])

# [END service_accounts]

# [START appengine_service_accounts]
import httplib2

from apiclient.discovery import build
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from oauth2client.appengine import AppAssertionCredentials

# BigQuery API Settings
SCOPE = 'https://www.googleapis.com/auth/bigquery'
PROJECT_NUMBER = 'XXXXXXXXXX' # REPLACE WITH YOUR Project ID

# Create a new API service for interacting with BigQuery
credentials = AppAssertionCredentials(scope=SCOPE)
http = credentials.authorize(httplib2.Http())
bigquery_service = build('bigquery', 'v2', http=http)


class ListDatasets(webapp.RequestHandler):
  def get(self):
    datasets = bigquery_service.datasets()
    listReply = datasets.list(projectId=PROJECT_NUMBER).execute()
    self.response.out.write('Dataset list:')
    self.response.out.write(listReply)


application = webapp.WSGIApplication(
                                     [('/listdatasets(.*)', ListDatasets)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
  
# [END appengine_service_accounts]