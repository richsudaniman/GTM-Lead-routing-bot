import requests

import config
from utils import retry


def build_message(lead, company, score, reason, rep):
    if rep:
        assigned = f"<@{rep['slack_id']}>"
    else:
        assigned = "no rep (sending to nurture)"

    return (
        f"*New lead: {lead['name']} @ {company['name']}* → {assigned}\n"
        f"*Score:* {score}/100 ({reason})\n"
        f"*Company:* {company['industry']}, {company['employees']} employees, {company['country']}\n"
        f"*Title:* {lead['title']}\n"
        f"*Email:* {lead['email']}"
    )


def send_to_slack(text):
    if not config.SLACK_BOT_TOKEN:
        print("no SLACK_BOT_TOKEN set, printing message instead:")
        print(text)
        return False

    def post():
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}"},
            json={"channel": config.SLACK_CHANNEL, "text": text},
            timeout=10,
        )
        data = response.json()
        if not data.get("ok"):
            raise Exception(f"slack error: {data.get('error')}")

    retry(post)
    return True
