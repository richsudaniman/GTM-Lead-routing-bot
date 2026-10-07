REPS = {
    "enterprise": {"name": "Avery Chen", "slack_id": "U0000000001"},
    "mid_market": {"name": "Riley Nguyen", "slack_id": "U0000000004"},
    "smb": {"name": "Jalal Abdelrahim", "slack_id": "U0BEA0YPSL9"},
}

MIN_SCORE = 50


def pick_rep(company, score):
    """Pick a rep based on company size. Returns None if the lead isn't good enough."""
    if score < MIN_SCORE:
        return None

    employees = company["employees"]
    if employees >= 1000:
        return REPS["enterprise"]
    elif employees >= 200:
        return REPS["mid_market"]
    else:
        return REPS["smb"]
