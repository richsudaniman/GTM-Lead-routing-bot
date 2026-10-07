import os

import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#leads"


def build_message(lead, company, score, reason):
    return (
        f"*New lead: {lead['name']} @ {company['name']}*\n"
        f"*Score:* {score}/100 ({reason})\n"
        f"*Company:* {company['industry']}, {company['employees']} employees, {company['country']}\n"
        f"*Title:* {lead['title']}\n"
        f"*Email:* {lead['email']}"
    )


def send_to_slack(text):
    if not SLACK_BOT_TOKEN:
        print("no SLACK_BOT_TOKEN set, printing message instead:")
        print(text)
        return False

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={"channel": SLACK_CHANNEL, "text": text},
    )
    print(response.json())
    return True
