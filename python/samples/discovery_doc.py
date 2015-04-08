import os
import json
import httplib2
import time

RESOURCE_PATH='..'
MAX_AGE = 86400 #update discovery docs older than a day

# A module that takes care of caching and updating discovery docs
# for google-api-python-clients (until such a feature is integrated)


# [START get_discovery_doc]
def get_discovery_doc(api, version):

    path = os.path.join(RESOURCE_PATH, '{}.{}'.format(api, version))
    try:
        age = time.time() - os.path.getmtime(path)
        if age > MAX_AGE:
            _update_discovery_doc(api, version, path)
    except os.error:
        _update_discovery_doc(api, version, path)

    with open(path, 'r') as discovery_doc:
        return discovery_doc.read()


def _update_discovery_doc(api, version, path):
    from apiclient.discovery import DISCOVERY_URI
    from apiclient.errors import HttpError
    from apiclient.errors import InvalidJsonError
    import uritemplate

    requested_url = uritemplate.expand(DISCOVERY_URI,
                                       {'api': api, 'apiVersion': version})
    resp, content = httplib2.Http().request(requested_url)
    if resp.status >= 400:
        raise HttpError(resp, content, uri=requested_url)
    try:
        with open(path, 'w') as discovery_doc:
            discovery_json = json.loads(content)
            json.dump(discovery_json, discovery_doc)
    except ValueError:
        raise InvalidJsonError(
                'Bad JSON: %s from %s.' % (content, requested_url))
# [END get_discovery_doc]

