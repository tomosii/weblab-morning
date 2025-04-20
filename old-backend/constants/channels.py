import os
from dotenv import load_dotenv

load_dotenv()

TARGET_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# dev
# DEV_CHANNEL_ID = "C0616PTQ6AF"

# test
# TEST_CHANNEL_ID = "C060S2Z6E15"

# prod
# PROD_CHANNEL_ID = "C05CMTDNZ89"
