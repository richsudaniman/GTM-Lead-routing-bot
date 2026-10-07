import os

from flask import Flask, jsonify, request

from enrichment import get_company
from routing import pick_rep
from scoring import score_lead
from slack import build_message, send_to_slack

app = Flask(__name__)

PROCESSED_FILE = "processed_leads.txt"


def parse_form(data):
    # hubspot sends the form fields as a list of {"name": ..., "value": ...}
    fields = {}
    for field in data.get("fields", []):
        fields[field["name"]] = field["value"]

    email = fields.get("email", "").strip().lower()
    return {
        "id": data.get("conversionId") or email,
        "email": email,
        "name": (fields.get("firstname", "") + " " + fields.get("lastname", "")).strip(),
        "title": fields.get("jobtitle", ""),
        "domain": email.split("@")[-1] if "@" in email else "",
        "message": fields.get("message", ""),
    }


def already_processed(lead_id):
    if not os.path.exists(PROCESSED_FILE):
        return False
    with open(PROCESSED_FILE) as f:
        return lead_id in f.read().splitlines()


def mark_processed(lead_id):
    with open(PROCESSED_FILE, "a") as f:
        f.write(lead_id + "\n")


def handle_lead(data):
    lead = parse_form(data)

    if not lead["domain"]:
        return {"status": "skipped", "reason": "no valid email"}

    if already_processed(lead["id"]):
        print("already handled this lead, skipping:", lead["id"])
        return {"status": "duplicate"}

    company = get_company(lead["domain"])
    score, reason = score_lead(lead, company)
    rep = pick_rep(company, score)

    message = build_message(lead, company, score, reason, rep)
    send_to_slack(message)

    mark_processed(lead["id"])

    return {"status": "done", "score": score, "rep": rep["name"] if rep else None}


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    try:
        result = handle_lead(data)
        return jsonify(result)
    except Exception as e:
        print("error handling lead:", e)
        # returning 500 makes hubspot retry the webhook later
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
