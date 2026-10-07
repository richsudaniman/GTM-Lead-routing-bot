from flask import Flask, jsonify, request

from enrichment import get_company

app = Flask(__name__)


def parse_form(data):
    # hubspot sends the form fields as a list of {"name": ..., "value": ...}
    fields = {}
    for field in data.get("fields", []):
        fields[field["name"]] = field["value"]

    email = fields.get("email", "").strip().lower()
    return {
        "email": email,
        "name": (fields.get("firstname", "") + " " + fields.get("lastname", "")).strip(),
        "title": fields.get("jobtitle", ""),
        "domain": email.split("@")[1],
        "message": fields.get("message", ""),
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    lead = parse_form(data)
    company = get_company(lead["domain"])
    print(lead, company)
    return jsonify({"lead": lead, "company": company})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
