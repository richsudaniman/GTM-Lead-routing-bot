import os

from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#leads")

# who gets leads for each company size
REPS = {
    "enterprise": {"name": "Avery Chen", "slack_id": "U0000000001"},
    "mid_market": {"name": "Riley Nguyen", "slack_id": "U0000000004"},
    "smb": {"name": "Jalal Abdelrahim", "slack_id": "U0BEA0YPSL9"},
}

# leads below this score don't get a rep, marketing handles them
MIN_SCORE = 50
