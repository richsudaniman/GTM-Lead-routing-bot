import os

from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#leads")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")

# who gets leads for each company size
REPS = {
    "enterprise": {"name": "Avery Chen", "slack_id": "U0000000001"},
    "mid_market": {"name": "Riley Nguyen", "slack_id": "U0000000004"},
    "smb": {"name": "Jalal Abdelrahim", "slack_id": "U0BEA0YPSL9"},
}

# leads below this score don't get a rep, marketing handles them
MIN_SCORE = 50

# our ideal customer profile (used in the claude prompt)
ICP = """
We sell sales automation software to B2B companies.
Good fit: SaaS, Fintech or Logistics companies with 50 to 5000 employees.
Best contacts are in Sales, RevOps or Marketing leadership (Head of, VP, Director).
Bad fit: students, job seekers, agencies, people using personal emails.
"""
