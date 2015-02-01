from apiclient import discovery
import httplib2


# Some blank API key. In the future, we should switch to an OAuth2 workflow.
API_KEY = ""


# Build and return the BigQuery service, initialized with our credentials.
def getBigQueryService():
    # Create a httplib2.Http object to handle the service's HTTP requests.
    # TODO: Authorize it with some OAuth credentials.
    http = httplib2.Http()
    return discovery.build('bigquery', 'v2', http=http, developerKey=API_KEY)
