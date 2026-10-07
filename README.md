# GTM Lead Routing Bot

A small Flask app that takes new leads from a HubSpot form, scores them, and posts them in Slack tagged to the right sales rep.

## The problem

At a lot of B2B companies, inbound leads get routed by hand. Someone in sales ops checks HubSpot, decides whether the lead is any good, figures out who should own it, and messages that rep. That causes a few problems:

- **Leads wait.** If nobody checks HubSpot for a few hours, or over a weekend, a person who just asked for a demo sits there with no reply. The longer a lead waits, the less likely it is to turn into a meeting, and by then they may have talked to a competitor.
- **Reps waste time on bad leads.** Students, job seekers and people with gmail addresses come through the same form as real buyers. Reps either sort through them by hand or ignore the inbox.
- **Routing isn't fair or consistent.** Whoever grabs the lead first gets it, or it depends on who did the routing that day. Big accounts can land with the wrong team.
- **No record of why.** When a rep asks "why did I get this lead?" or a good lead slipped through, there's nothing to look back at.

## How this solves it

| Problem | What the bot does |
|---|---|
| Leads wait for someone to route them | Routes every lead the moment the form is submitted and posts it straight to Slack, where reps already are |
| Reps waste time on bad leads | Scores each lead against the ideal customer profile (Claude, or simple rules), so personal emails and bad fits get no rep and go to marketing nurture instead |
| Routing isn't consistent | Uses the same rules every time: enterprise, mid-market or SMB rep based on company size |
| The right rep doesn't notice | @mentions the assigned rep in the Slack post, with the score and the reason, so they know why it's worth their time |
| No record of why | Logs every decision (score, reason, rep) to `decisions.log` |
| HubSpot sends the same form twice | Skips duplicates so a lead is never routed twice |
| Slack or Claude has a hiccup | Retries the call so leads don't get dropped |

## Screenshots

The Slack message a rep gets (the rep is @mentioned):

<img src="screenshots/slack-message.png" alt="Slack message for a new lead with the score, company info, and the assigned rep tagged" width="450">

Running the sample lead with no API keys set, and the decision that got logged:

<img src="screenshots/run-sample-lead.png" alt="Terminal output from python app.py sample_lead.json and the decisions.log entry" width="700">

Tests:

<img src="screenshots/tests.png" alt="pytest output with 10 tests passing" width="700">

## How it works

1. HubSpot sends the form submission to `/webhook`.
2. We look up the company from the email domain (`enrichment.py`).
3. The lead gets a score from 0 to 100 (`scoring.py`):
   - If `ANTHROPIC_API_KEY` is set, Claude scores it against our ideal customer profile (ICP).
   - Otherwise, or if Claude fails, it uses simple rules: industry, company size and job title.
   - Personal emails (gmail etc.) always get 0.
4. We pick a rep based on company size (`routing.py`):
   - 1000+ employees: enterprise rep
   - 200 to 999 employees: mid-market rep
   - Under 200 employees: SMB rep
   - Score under 50: no rep, the lead goes to marketing for nurture
5. We post the lead in Slack and @ the rep (`slack.py`).

The app also:
- Retries Slack and Claude calls up to 3 times if they fail.
- Skips duplicate submissions (HubSpot sometimes sends the same one twice).
- Logs every decision to `decisions.log`.

## Setup

```
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:
- `SLACK_BOT_TOKEN`: from a Slack app with the `chat:write` scope. Invite the bot to your channel.
- `SLACK_CHANNEL`: where leads get posted (default `#leads`).
- `ANTHROPIC_API_KEY`: optional. Without it, the rules-based scoring is used.

Reps and the ICP are set in `config.py`.

## Running it

Test with the sample lead (no HubSpot needed):

```
python app.py sample_lead.json
```

Output:

```
no SLACK_BOT_TOKEN set, printing message instead:
*New lead: Nora Weiss @ Routewise* → <@U0BEA0YPSL9>
*Score:* 80/100 (good industry, senior title)
*Company:* Fintech, 45 employees, DE
*Title:* Head of Sales
*Email:* nora.weiss@routewise.io
{'status': 'done', 'score': 80, 'rep': 'Jalal Abdelrahim'}
```

Run the server:

```
python app.py
```

Then in HubSpot, make a workflow with a "Send a webhook" action pointing to `https://<your-server>/webhook`.

## Tests

```
pytest
```

## TODO

- Use a real enrichment API instead of the fake company data.
- Verify the HubSpot webhook signature.
- Use a database instead of text files for duplicates and logs.
