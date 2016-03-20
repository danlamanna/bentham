import json


def notify(event):
    print(json.dumps(event, indent=2))
