import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib'))

from collector import get_selected_line
from serializer import serialize_aline
from api_client import login, post_aline
from pyrevit import forms

config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.json')
with open(config_path) as f:
    config = json.load(f)

try:
    element, curve = get_selected_line()

    name = forms.ask_for_string(prompt="Enter a name for this A-Line:", title="Send Line")
    if not name or not name.strip():
        forms.alert("Name is required.", title="Send Line")
        raise SystemExit

    token = login(config["base_url"], config["email"], config["password"])
    payload = serialize_aline(element, curve, name.strip())
    result = post_aline(config["base_url"], token, payload)

    forms.alert(
        "A-Line created.\nid={0}  name={1}".format(result.get("id"), result.get("name")),
        title="Send Line"
    )
except SystemExit:
    pass
except ValueError as e:
    forms.alert(str(e), title="Send Line")
except RuntimeError as e:
    forms.alert(str(e), title="Send Line")
except Exception as e:
    forms.alert("Unexpected error:\n" + str(e), title="Send Line")
