import config


def pick_rep(company, score):
    """Pick a rep based on company size. Returns None if the lead isn't good enough."""
    if score < config.MIN_SCORE:
        return None

    employees = company["employees"]
    if employees >= 1000:
        return config.REPS["enterprise"]
    elif employees >= 200:
        return config.REPS["mid_market"]
    else:
        return config.REPS["smb"]
