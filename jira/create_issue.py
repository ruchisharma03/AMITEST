from requests import post
from json import dumps, loads
from os import getenv
from yaml import safe_load
from base64 import b64encode

api_token = getenv('API_TOKEN')

with open('jira/jira.config.yaml') as fp:

    config = safe_load(fp)

    url = f'https://{config["DOMAIN"]}.atlassian.net/rest/api/2/issue/'

    username = config['USERNAME']

    #api_token = config['API_TOKEN']

    auth_header = b64encode(str(
        username+":"+api_token).encode('ascii')).decode("ascii")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic " + auth_header
    }

    body = {
        "fields": {
            "project":
            {
                "key": config['PROJECT_KEY'],
            },
            "customfield_11699": [{"value": "Conversations"},],
            "customfield_12252": {"value": "Conversations Submission"},
            "summary": config['SUMMARY'],
            "description": config["DESCRIPTION"],
            "issuetype": {
                "name": config['ISSUETYPE']
            }
        }
    }

    payload = dumps(body)

    response = post(url, data=payload, headers=headers)

    print(dumps(loads(response.text),
          sort_keys=True, indent=4, separators=(",", ": ")))
