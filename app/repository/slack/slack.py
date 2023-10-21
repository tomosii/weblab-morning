import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
