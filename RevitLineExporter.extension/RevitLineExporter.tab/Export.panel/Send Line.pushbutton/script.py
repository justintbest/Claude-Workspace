import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib'))

from collector import get_selected_lines, chain_segments
from serializer import serialize_aline
from api_client import post_aline
from pyrevit import forms

config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.json')
session_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'session.json')

with open(config_path) as f:
    config = json.load(f)

try:
    if not os.path.exists(session_path):
        forms.alert("You are not signed in. Please click Sign In first.", title="Send Line")
        raise SystemExit

    with open(session_path) as f:
        session = json.load(f)

    token = session.get("token")
    if not token:
        forms.alert("Session invalid. Please click Sign In first.", title="Send Line")
        raise SystemExit

    segments = get_selected_lines()
    points = chain_segments(segments)
    closed = len(segments) > 1

    name = forms.ask_for_string(prompt="Enter a name for this A-Line:", title="Send Line")
    if not name or not name.strip():
        forms.alert("Name is required.", title="Send Line")
        raise SystemExit

    payload = serialize_aline(points, name.strip(), closed)
    result = post_aline(config["base_url"], token, payload)

    forms.alert(
        "A-Line created.\nid={0}  name={1}  points={2}".format(
            result.get("id"), result.get("name"), len(points)
        ),
        title="Send Line"
    )

except SystemExit:
    pass
except ValueError as e:
    forms.alert(str(e), title="Send Line")
except RuntimeError as e:
    if "401" in str(e):
        forms.alert("Session expired. Please click Sign In first.", title="Send Line")
    else:
        forms.alert(str(e), title="Send Line")
except Exception as e:
    forms.alert("Unexpected error:\n" + str(e), title="Send Line")
