import os
import json

from pyrevit import forms

session_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'session.json')

try:
    if os.path.exists(session_path):
        os.remove(session_path)
        forms.alert("Signed out successfully.", title="Sign Out")
    else:
        forms.alert("You are not currently signed in.", title="Sign Out")
except Exception as e:
    forms.alert("Unexpected error:\n" + str(e), title="Sign Out")
