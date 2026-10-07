def score_lead(lead, company):
    """Returns (score from 0-100, reason)"""
    score = 30
    reasons = []

    if company["industry"] in ["SaaS", "Software", "Fintech", "Logistics"]:
        score += 30
        reasons.append("good industry")

    if 50 <= company["employees"] <= 5000:
        score += 20
        reasons.append("good company size")

    title = lead["title"].lower()
    for word in ["head", "vp", "director", "chief", "founder"]:
        if word in title:
            score += 20
            reasons.append("senior title")
            break

    if not reasons:
        reasons.append("no strong signals")

    return min(score, 100), ", ".join(reasons)
