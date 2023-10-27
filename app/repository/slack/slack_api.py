import os
from slack_sdk import WebClient


class SlackRepository:
    def __init__(self):
        self.client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
