import json
import urllib2


def _post_json(url, data, token=None):
    body = json.dumps(data)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib2.Request(url, body, headers)
    try:
        resp = urllib2.urlopen(req, timeout=30)
        return json.loads(resp.read())
    except urllib2.HTTPError as e:
        text = e.read()
        raise RuntimeError("HTTP {0}: {1}".format(e.code, text))
    except urllib2.URLError as e:
        raise RuntimeError("Network error: {0}".format(e.reason))


def login(base_url, email, password):
    data = _post_json(base_url + "/api/v1/auth/login", {"email": email, "password": password})
    token = data.get("token")
    if not token:
        raise RuntimeError("Login succeeded but no token returned")
    return token


def post_aline(base_url, token, payload):
    return _post_json(base_url + "/api/v1/alines", payload, token=token)
