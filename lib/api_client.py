import json
import urllib2

def post_line(payload, endpoint, api_key):
    body = json.dumps(payload)
    request = urllib2.Request(endpoint, body, {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    })
    response = urllib2.urlopen(request)
    return response.read()
