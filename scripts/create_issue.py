#!/bin/python3
import os
import sys
sys.path.append('.')

from jira.jira import JiraAPI


USERNAME = os.getenv('JIRA_USERNAME')
API_TOKEN = os.getenv("JIRA_API_TOKEN")


jira = JiraAPI(
    USERNAME, API_TOKEN, "config/jira.config.yaml")

print(jira.create_issue())
