import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib'))

from api_client import login
from pyrevit import forms

config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.json')
session_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'session.json')

with open(config_path) as f:
    config = json.load(f)

try:
    email = forms.ask_for_string(prompt="Email:", title="Sign In")
    if not email or not email.strip():
        raise SystemExit

    password = forms.ask_for_string(prompt="Password:", title="Sign In")
    if not password:
        raise SystemExit

    token = login(config["base_url"], email.strip(), password)

    with open(session_path, 'w') as f:
        json.dump({"token": token}, f)

    forms.alert("Signed in successfully.", title="Sign In")

except SystemExit:
    pass
except RuntimeError as e:
    forms.alert("Sign in failed:\n" + str(e), title="Sign In")
except Exception as e:
    forms.alert("Unexpected error:\n" + str(e), title="Sign In")
