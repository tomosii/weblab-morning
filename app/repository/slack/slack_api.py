import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()


class SlackRepository:
    def __init__(self):
        self.client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
