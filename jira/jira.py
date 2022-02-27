#!/bin/python3
from base64 import b64encode
import yaml
import requests
import json
from datetime import datetime


class JiraAPI:

    def __init__(self, username, password, config_file='jira.config.yaml'):

        self.auth_header = b64encode(str(
            username+":"+password).encode('ascii')).decode("ascii")
        self.config = self.__read_config(config_file)
        self.base_url = f'https://{self.config["domain"]}.atlassian.net'

    def __read_config(self, file_path):
        with open(file_path) as fp:
            config_dict = yaml.safe_load(fp)
        return config_dict

    def create_issue(self):

        url = f'{self.base_url}/rest/api/2/issue/'

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic " + self.auth_header
        }

        fields = {}
        for k, v in self.config["fields"].items():
            fields[k] = v

        body = {
            "fields": {
                "project":
                {
                    "key": self.config['projectKey'],
                },
                **fields,
                "issuetype": {
                    "name":  self.config['issueType']
                }
            }
        }
        payload = json.dumps(body)

        response = requests.post(url, data=payload, headers=headers)

        res = json.loads(response.text)

        res["jira_ticket_url"] = f"{self.base_url}/browse/{res['key']}"

        return json.dumps(res)

    def get_field_value_from_issue(self, field_names, ticket_number):

        url = f'{self.base_url}/rest/api/2/issue/{ticket_number}/'

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic " + self.auth_header
        }

        response = requests.get(url, headers=headers)


        fields = json.loads(response.text)["fields"]

        result = {}

        for each_field in field_names:

            field_name = each_field.split('.')
            if field_name[0] in fields:
                field_value = fields[field_name[0]]
                for field_part in field_name[1:]:
                    field_value = field_value[field_part]
                result[field_name[0]] = field_value
            else:
                result[field_name[0]] = None
        return json.dumps(result)
