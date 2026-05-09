import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'lib'))

from collector import get_selected_line
from serializer import serialize_line
from api_client import post_line
from pyrevit import forms

config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'config.json')
with open(config_path) as f:
    config = json.load(f)

try:
    element, curve = get_selected_line()
    payload = serialize_line(element, curve)
    post_line(payload, config["api_endpoint"], config["api_key"])
    forms.alert("Line sent successfully.", title="Send Line")
except ValueError as e:
    forms.alert(str(e), title="Send Line")
except Exception as e:
    forms.alert("Failed to send line:\n" + str(e), title="Send Line")
